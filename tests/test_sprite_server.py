import json
from pathlib import Path

from server import normalize_state, read_state, write_state


def test_normalize_state_keeps_only_sprite_statuses():
    raw = {
        "mat1": {"collected": True, "mastered": False, "extra": "ignored"},
        "mat2": {"collected": False, "mastered": True},
        "custom-striker": {"collected": True, "mastered": False},
        "v4110-aura": {"collected": True, "mastered": True},
        "bad": "ignored",
    }

    assert normalize_state(raw) == {
        "mat1": {"collected": True, "mastered": False},
        "mat2": {"collected": True, "mastered": True},
        "v4110-aura": {"collected": True, "mastered": True},
    }


def test_state_round_trips_to_json_file(tmp_path: Path):
    path = tmp_path / "sprite-state.json"
    state = {"mat1": {"collected": True, "mastered": False}}

    write_state(path, state)

    assert json.loads(path.read_text()) == state
    assert read_state(path) == state


def test_missing_or_invalid_state_file_reads_as_empty(tmp_path: Path):
    missing = tmp_path / "missing.json"
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{")

    assert read_state(missing) == {}
    assert read_state(invalid) == {}
