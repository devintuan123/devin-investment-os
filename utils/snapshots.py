from __future__ import annotations

from pathlib import Path

from utils.snapshot_store import create_snapshot, load_snapshot_history, save_snapshot


def build_snapshot() -> dict:
    return create_snapshot()


def save_daily_snapshot() -> Path:
    return save_snapshot()


def load_snapshots() -> list[dict]:
    return load_snapshot_history()
