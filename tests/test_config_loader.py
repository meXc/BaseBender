from pathlib import Path

from basebender.rebaser.config_loader import (
    get_all_digit_sets,
    load_digit_sets_from_toml,
    load_ui_state,
    save_ui_state,
)


def test_load_digit_sets_from_toml_file_not_found():
    result = load_digit_sets_from_toml(Path("/nonexistent/file.toml"), "test")
    assert result == []


def test_load_digit_sets_from_toml_valid(tmp_path):
    toml_file = tmp_path / "test.toml"
    toml_file.write_text('[[digit_sets]]\nname = "Test"\ndigits = "abc"\n')
    result = load_digit_sets_from_toml(toml_file, "test")
    assert len(result) == 1
    assert result[0].name == "Test"
    assert result[0].digits == "abc"
    assert result[0].source == "test"


def test_load_digit_sets_from_toml_malformed(tmp_path):
    toml_file = tmp_path / "malformed.toml"
    toml_file.write_text("[[digit_sets]]\nname = 123\ndigits = 'abc'\n")
    result = load_digit_sets_from_toml(toml_file, "test")
    assert result == []


def test_get_all_digit_sets_returns_package_sets():
    result = get_all_digit_sets()
    assert len(result) > 0
    assert any("package:Binary" in key for key in result)
    assert any("package:Decimal" in key for key in result)
    assert any("package:Hexadecimal" in key for key in result)


def test_get_all_digit_sets_precedence(tmp_path, monkeypatch):
    missing_path = tmp_path / "nonexistent" / "default_digit_sets.toml"
    user_toml = tmp_path / "digit_sets.toml"
    user_toml.parent.mkdir(parents=True, exist_ok=True)
    user_toml.write_text('[[digit_sets]]\nname = "Decimal"\ndigits = "9876543210"\n')
    monkeypatch.setattr(
        "basebender.rebaser.config_loader._get_config_paths",
        lambda: (missing_path, None, user_toml, None),
    )
    result = get_all_digit_sets()
    assert "user:Decimal" in result


def test_ui_state_save_and_load(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "basebender.rebaser.config_loader.get_ui_state_path",
        lambda: tmp_path / "ui_state.toml",
    )
    state = {"last_input": "hello", "realtime_enabled": True}
    save_ui_state(state)
    loaded = load_ui_state()
    assert loaded == state


def test_load_ui_state_missing_file(tmp_path, monkeypatch):
    nonexistent = tmp_path / "nonexistent" / "ui_state.toml"
    monkeypatch.setattr(
        "basebender.rebaser.config_loader.get_ui_state_path",
        lambda: nonexistent,
    )
    result = load_ui_state()
    assert result == {}
