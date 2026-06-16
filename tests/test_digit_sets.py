from basebender.rebaser.digit_sets import (
    get_predefined_digit_sets,
    suggest_digit_sets,
)


def test_get_predefined_digit_sets_returns_all():
    result = get_predefined_digit_sets()
    assert len(result) > 0
    assert "package:Binary" in result
    assert "package:Decimal" in result
    assert "package:Hexadecimal" in result
    assert "package:Base64" in result
    assert "package:ASCII Printable" in result


def test_get_predefined_digit_sets_caching():
    first = get_predefined_digit_sets()
    second = get_predefined_digit_sets()
    assert first is second


def test_suggest_digit_sets_binary():
    suggestions = suggest_digit_sets("101")
    assert "package:Binary" in suggestions


def test_suggest_digit_sets_decimal():
    suggestions = suggest_digit_sets("12345")
    assert "package:Decimal" in suggestions


def test_suggest_digit_sets_hex():
    suggestions = suggest_digit_sets("DEADBEEF")
    assert "package:Hexadecimal" in suggestions


def test_suggest_digit_sets_no_match():
    suggestions = suggest_digit_sets("\U0001f600\U0001f601")
    assert len(suggestions) == 0


def test_suggest_digit_sets_empty_string():
    suggestions = suggest_digit_sets("")
    assert len(suggestions) == 0
