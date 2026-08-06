from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_STATE_PATH = ROOT / "sprite-state.json"


def is_sprite_key(key: str) -> bool:
    known_exact = {
        "batman",
        "ironmouse",
        "llama",
        "peely",
        "pollo",
        "vini-jr",
        "john-wick",
        "holofoil-duck",
        "holofoil-demon",
    }
    known_prefixes = (
        "mat",
        "v4110-",
        "gold-",
        "gummy-",
        "galaxy-",
        "gem-",
        "holofoil-",
        "cube-",
        "quack-",
    )
    return key in known_exact or key.startswith(known_prefixes)


def normalize_state(raw: Any) -> dict[str, dict[str, bool]]:
    if not isinstance(raw, dict):
        return {}

    state: dict[str, dict[str, bool]] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not is_sprite_key(key):
            continue
        if not isinstance(value, dict):
            continue
        mastered = bool(value.get("mastered"))
        state[key] = {
            "collected": bool(value.get("collected")) or mastered,
            "mastered": mastered,
        }
    return state


def read_state(path: Path = DEFAULT_STATE_PATH) -> dict[str, dict[str, bool]]:
    try:
        return normalize_state(json.loads(path.read_text()))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def write_state(path: Path, state: dict[str, dict[str, bool]]) -> None:
    normalized = normalize_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(f"{path.suffix}.tmp")
    tmp_path.write_text(json.dumps(normalized, indent=2, sort_keys=True))
    tmp_path.replace(path)


def route_path(path: str) -> str:
    route = path.split("?", 1)[0]
    if route in {"/sprites", "/sprites/", "/sprites/index.html"}:
        return "/index.html"
    if route in {"/sprites/compare", "/sprites/compare/"}:
        return "/compare.html"
    return path


class SpriteRequestHandler(SimpleHTTPRequestHandler):
    state_path = DEFAULT_STATE_PATH

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory or str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/api/state":
            self._send_json(read_state(self.state_path))
            return
        self.path = route_path(self.path)
        super().do_GET()

    def do_POST(self) -> None:
        self._save_state()

    def do_PUT(self) -> None:
        self._save_state()

    def _save_state(self) -> None:
        if self.path != "/api/state":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            state = normalize_state(json.loads(raw or "{}"))
        except (ValueError, json.JSONDecodeError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        write_state(self.state_path, state)
        self._send_json(state)

    def _send_json(self, payload: Any) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Sprite Tracker server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH))
    args = parser.parse_args()

    SpriteRequestHandler.state_path = Path(args.state)
    server = ThreadingHTTPServer((args.host, args.port), SpriteRequestHandler)
    print(f"Sprite Tracker running at http://{args.host}:{args.port}/")
    print(f"Saving progress to {SpriteRequestHandler.state_path}")
    server.serve_forever()


if __name__ == "__main__":
    main()
