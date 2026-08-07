#!/usr/bin/env python3
"""
Local dev server for the Practice Hub UI.

Serves a small JSON API over this repo (file tree with real self-check
status, real file contents, running a file's self-check for real, and
invoking the refine-questions skill via the Claude Code CLI) plus the
static frontend in static/index.html.

Stdlib only - no third-party dependencies, matching the rest of this
repo's philosophy (uv + ruff for exercises, nothing else).

Run from anywhere:
    python tools/practice_hub/server.py
Then open http://localhost:8

See tools/practice_hub/README.md for what's real vs. still mocked, and
for the permission-mode caveat on the refine-questions button.
"""
from __future__ import annotations

import json
import mimetypes
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

REPO_ROOT = Path(__file__).resolve().parents[2]  # tools/practice_hub/server.py -> repo root
STATIC_DIR = Path(__file__).resolve().parent / "static"
PORT = 8787

EXERCISE_ROOT = "exercises"
PROJECT_ROOT = "projects"

# path (str) -> (mtime, passed) - avoids re-running every file's self-check
# on every tree refresh when nothing changed.
_self_check_cache: dict[str, tuple[float, bool]] = {}


def resolve_python() -> str:
    """Prefer this repo's own venv so exercises run in the environment
    you actually set up (uv venv), falling back to whatever's running
    this server."""
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable or "python3"


def safe_repo_path(rel_path: str) -> Path:
    """Resolve a repo-relative path and refuse anything outside
    exercises/ or projects/ - in particular, solutions/ is never served
    by this API, mirroring the "don't casually browse the answer key"
    rule in CLAUDE.md."""
    if not rel_path:
        raise ValueError("missing path")
    candidate = (REPO_ROOT / rel_path).resolve()
    allowed_roots = [REPO_ROOT / EXERCISE_ROOT, REPO_ROOT / PROJECT_ROOT]
    if not any(root == candidate or root in candidate.parents for root in allowed_roots):
        raise ValueError("path is outside exercises/ or projects/")
    if not candidate.is_file():
        raise ValueError("not a file")
    return candidate


def run_self_check(path: Path) -> bool:
    mtime = path.stat().st_mtime
    key = str(path)
    cached = _self_check_cache.get(key)
    if cached and cached[0] == mtime:
        return cached[1]
    try:
        result = subprocess.run(
            [resolve_python(), str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            timeout=10,
        )
        passed = result.returncode == 0
    except Exception:
        passed = False
    _self_check_cache[key] = (mtime, passed)
    return passed


def build_tree() -> dict:
    tree: dict = {"exercises": [], "projects": []}

    exercises_root = REPO_ROOT / EXERCISE_ROOT
    if exercises_root.exists():
        for topic_dir in sorted(p for p in exercises_root.iterdir() if p.is_dir()):
            files = []
            for f in sorted(topic_dir.glob("*.py")):
                files.append(
                    {
                        "name": f.name,
                        "path": str(f.relative_to(REPO_ROOT)),
                        "status": "done" if run_self_check(f) else "todo",
                        "mtime": f.stat().st_mtime,
                    }
                )
            if files:
                tree["exercises"].append({"topic": topic_dir.name, "files": files})

    projects_root = REPO_ROOT / PROJECT_ROOT
    if projects_root.exists():
        for proj_dir in sorted(p for p in projects_root.iterdir() if p.is_dir()):
            files = []
            for f in sorted(proj_dir.glob("*.py")):
                files.append(
                    {
                        "name": f.name,
                        "path": str(f.relative_to(REPO_ROOT)),
                        # projects have no fixed pass/fail contract (CLAUDE.md) -
                        # always "in progress", never "done".
                        "status": "progress",
                        "mtime": f.stat().st_mtime,
                    }
                )
            if files:
                tree["projects"].append({"project": proj_dir.name, "files": files})

    return tree


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass  # quiet; comment out to debug requests

    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message, status=400):
        self._send_json({"error": message}, status)

    def _serve_static(self, name: str):
        path = STATIC_DIR / name
        if not path.exists():
            return self._send_error_json("not found", 404)
        content = path.read_bytes()
        mime, _ = mimetypes.guess_type(str(path))
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path in ("/", "/index.html"):
            return self._serve_static("index.html")

        if parsed.path == "/api/tree":
            return self._send_json(build_tree())

        if parsed.path == "/api/file":
            qs = parse_qs(parsed.query)
            rel = qs.get("path", [""])[0]
            try:
                p = safe_repo_path(rel)
            except ValueError as e:
                return self._send_error_json(str(e), 403)
            return self._send_json({"path": rel, "content": p.read_text()})

        return self._send_error_json("not found", 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            body = {}

        if parsed.path == "/api/run":
            rel = body.get("path", "")
            try:
                p = safe_repo_path(rel)
            except ValueError as e:
                return self._send_error_json(str(e), 403)
            try:
                result = subprocess.run(
                    [resolve_python(), str(p)],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
            except subprocess.TimeoutExpired:
                return self._send_error_json("timed out after 15s", 500)
            _self_check_cache.pop(str(p), None)  # force a fresh check next tree fetch
            return self._send_json(
                {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
            )

        if parsed.path == "/api/refine-questions":
            claude_bin = shutil.which("claude")
            if not claude_bin:
                return self._send_error_json(
                    "claude CLI not found on PATH - install Claude Code to use this button",
                    500,
                )
            prompt = (
                "Use the refine-questions skill to generate my next exercise. "
                "Follow CLAUDE.md and the skill file exactly, including verifying "
                "the new exercise before handing it over."
            )
            try:
                result = subprocess.run(
                    [claude_bin, "--dangerously-skip-permissions", "-p", prompt],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=240,
                )
            except subprocess.TimeoutExpired:
                return self._send_error_json("claude -p timed out after 240s", 500)
            return self._send_json(
                {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "tree": build_tree(),
                }
            )

        return self._send_error_json("not found", 404)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Practice Hub running at http://localhost:{PORT}")
    print(f"Repo root: {REPO_ROOT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
