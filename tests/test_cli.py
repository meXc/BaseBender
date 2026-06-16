import sys
from unittest.mock import patch

import pytest

from basebender.cli import (
    list_digit_sets_cli,
    perform_rebase_cli,
    suggest_digit_sets_cli,
)


def test_list_digit_sets_cli_returns_zero():
    exit_code = list_digit_sets_cli()
    assert exit_code == 0


def test_suggest_digit_sets_cli_with_match():
    exit_code = suggest_digit_sets_cli("101")
    assert exit_code == 0


def test_suggest_digit_sets_cli_no_match():
    exit_code = suggest_digit_sets_cli("\U0001f600")
    assert exit_code == 0


def test_perform_rebase_cli_empty_input():
    exit_code = perform_rebase_cli("", None, None)
    assert exit_code == 0


def test_perform_rebase_cli_full_rebase():
    exit_code = perform_rebase_cli("101", "0123456789", "01")
    assert exit_code == 0


def test_perform_rebase_cli_invalid_digit_set():
    exit_code = perform_rebase_cli("hello", "", "")
    assert exit_code == 0


def test_main_help():
    with patch.object(sys, "argv", ["basebender", "--help"]):
        with pytest.raises(SystemExit) as exc:
            from basebender.cli import main

            main()
        assert exc.value.code == 0
