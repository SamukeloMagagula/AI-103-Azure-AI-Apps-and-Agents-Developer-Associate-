"""Shared helpers: env loading, mock/live switch, pretty printing."""
from __future__ import annotations
import json
import os
from pathlib import Path

_ENV_FILE = Path(__file__).with_name(".env")


def _load_env() -> None:
    if not _ENV_FILE.exists():
        return
    for raw in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()

USE_MOCK = os.environ.get("USE_MOCK", "1") == "1"


def need(key: str) -> str:
    val = os.environ.get(key, "")
    if not val and not USE_MOCK:
        raise RuntimeError(f"Missing env var {key}. Set it in .env or USE_MOCK=1.")
    return val or f"<mock:{key}>"


def show(title: str, payload) -> None:
    print(f"\n=== {title} ===")
    if isinstance(payload, (dict, list)):
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload)
