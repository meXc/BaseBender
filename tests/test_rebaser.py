# pylint: disable=invalid-name
"""
This module contains unit tests for the `rebaser` package,
specifically for the `DigitSetRebaser` class.
"""

import pytest

from rebaser.digit_set_rebaser import DigitSetRebaser
from rebaser.models import DigitSet

# Define some common DigitSet instances for testing
DECIMAL_DIGIT_SET = DigitSet(name="Decimal", digits="0123456789", source="test")
BINARY_DIGIT_SET = DigitSet(name="Binary", digits="01", source="test")
HEX_DIGIT_SET = DigitSet(
    name="Hexadecimal", digits="0123456789ABCDEF", source="test"
)
OCTAL_DIGIT_SET = DigitSet(name="Octal", digits="01234567", source="test")
BASE62_DIGIT_SET = DigitSet(
    name="Base62",
    digits=("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    source="test",
)
SINGLE_CHAR_DIGIT_SET = DigitSet(name="Single", digits="X", source="test")
EMPTY_DIGIT_SET = DigitSet(name="Empty", digits="", source="test")


# Test cases for DigitSetRebaser.__init__
def test_rebaser_init_with_both_digit_sets():
    """
    Tests that the DigitSetRebaser initializes correctly when both input and
    output digit sets are provided. It verifies that the internal lists and maps
    are populated as expected and that the initial digit sets are stored.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.input_digit_set_list == list(DECIMAL_DIGIT_SET.digits)
    assert rebaser.output_digit_set_list == list(HEX_DIGIT_SET.digits)
    assert rebaser.initial_input_digit_set == DECIMAL_DIGIT_SET
    assert rebaser.initial_output_digit_set == HEX_DIGIT_SET


def test_rebaser_init_with_only_input_digit_set():
    """
    Tests that the DigitSetRebaser initializes correctly when only the input digit set is provided.
    It verifies that the input digit set is set, and the output digit set is not.
    """
    rebaser = DigitSetRebaser(in_digit_set=DECIMAL_DIGIT_SET)
    assert rebaser.input_digit_set_list == list(DECIMAL_DIGIT_SET.digits)
    assert not rebaser.output_digit_set_list
    assert rebaser.initial_input_digit_set == DECIMAL_DIGIT_SET
    assert rebaser.initial_output_digit_set is None


def test_rebaser_init_with_only_output_digit_set():
    """
    Tests that the DigitSetRebaser initializes correctly when only the output digit set is provided.
    It verifies that the output digit set is set, and the input digit set is not.
    """
    rebaser = DigitSetRebaser(out_digit_set=HEX_DIGIT_SET)
    assert not rebaser.input_digit_set_list
    assert rebaser.output_digit_set_list == list(HEX_DIGIT_SET.digits)
    assert rebaser.initial_input_digit_set is None
    assert rebaser.initial_output_digit_set == HEX_DIGIT_SET


def test_rebaser_init_with_no_digit_sets():
    """
    Tests that the DigitSetRebaser initializes correctly when no digit sets are provided.
    It verifies that both input and output digit sets are not set.
    """
    rebaser = DigitSetRebaser()
    assert not rebaser.input_digit_set_list
    assert not rebaser.output_digit_set_list
    assert rebaser.initial_input_digit_set is None
    assert rebaser.initial_output_digit_set is None


def test_rebaser_init_single_char_digit_set():
    """
    Tests the initialization of DigitSetRebaser with single-character digit sets.
    It verifies that the input and output digit set lists are correctly
    populated with single characters.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=SINGLE_CHAR_DIGIT_SET,
        in_digit_set=DigitSet(name="A", digits="a", source="test"),
    )
    assert rebaser.input_digit_set_list == ["a"]
    assert rebaser.output_digit_set_list == ["X"]


# Test cases for char_to_position
def test_char_to_position_found():
    """
    Tests the `char_to_position` method when the character is found in the digit set map.
    It verifies that the correct numerical position is returned for valid characters.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.char_to_position("0", rebaser.input_digit_set_map) == 0
    assert rebaser.char_to_position("9", rebaser.input_digit_set_map) == 9
    assert rebaser.char_to_position("F", rebaser.output_digit_set_map) == 15


def test_char_to_position_not_found_raises_error():
    """
    Tests that `char_to_position` raises a ValueError when the character is not
    found in the digit set map. It verifies that an appropriate error message is
    provided.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    with pytest.raises(
        ValueError, match="Character 'd' not found in the digit set."
    ):
        rebaser.char_to_position("d", rebaser.input_digit_set_map)


# Test cases for position_to_char
def test_position_to_char_valid():
    """
    Tests the `position_to_char` method when the position is valid.
    It verifies that the correct character is returned for valid positions.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.position_to_char(0, rebaser.input_digit_set_list) == "0"
    assert rebaser.position_to_char(9, rebaser.input_digit_set_list) == "9"
    assert rebaser.position_to_char(15, rebaser.output_digit_set_list) == "F"


def test_position_to_char_out_of_bounds_raises_error():
    """
    Tests that `position_to_char` raises an IndexError when the position is out
    of bounds. It verifies that an appropriate error message is provided for both
    positive and negative out-of-bounds positions.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    with pytest.raises(
        IndexError, match="Position 10 is out of bounds for the digit set."
    ):
        rebaser.position_to_char(10, rebaser.input_digit_set_list)
    with pytest.raises(
        IndexError, match="Position -1 is out of bounds for the digit set."
    ):
        rebaser.position_to_char(-1, rebaser.input_digit_set_list)


# Test cases for string_to_int_from_base
def test_string_to_int_from_base_simple():
    """
    Tests `string_to_int_from_base` with a simple decimal string.
    It verifies that a decimal string is correctly converted to its integer equivalent.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.string_to_int_from_base("123", rebaser.input_digit_set_map, 10)
        == 123
    )


def test_string_to_int_from_base_binary():
    """
    Tests `string_to_int_from_base` with a binary string.
    It verifies that a binary string is correctly converted to its integer equivalent.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=BINARY_DIGIT_SET
    )
    assert (
        rebaser.string_to_int_from_base("101", rebaser.input_digit_set_map, 2)
        == 5
    )


def test_string_to_int_from_base_hex():
    """
    Tests `string_to_int_from_base` with hexadecimal strings.
    It verifies that hexadecimal strings are correctly converted to their integer equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=HEX_DIGIT_SET
    )
    assert (
        rebaser.string_to_int_from_base("F", rebaser.input_digit_set_map, 16)
        == 15
    )
    assert (
        rebaser.string_to_int_from_base("1A", rebaser.input_digit_set_map, 16)
        == 26
    )


def test_string_to_int_from_base_empty_string():
    """
    Tests `string_to_int_from_base` with an empty input string.
    It verifies that an empty string correctly converts to an integer value of 0.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.string_to_int_from_base("", rebaser.input_digit_set_map, 10)
        == 0
    )


# Test cases for int_to_string_in_base
def test_int_to_string_in_base_simple():
    """
    Tests `int_to_string_in_base` with a simple integer and decimal base.
    It verifies that an integer is correctly converted to its decimal string representation.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.int_to_string_in_base(123, rebaser.output_digit_set_list, 10)
        == "123"
    )


def test_int_to_string_in_base_binary():
    """
    Tests `int_to_string_in_base` with an integer and binary base.
    It verifies that an integer is correctly converted to its binary string representation.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=DECIMAL_DIGIT_SET, out_digit_set=BINARY_DIGIT_SET
    )
    assert (
        rebaser.int_to_string_in_base(5, rebaser.output_digit_set_list, 2)
        == "101"
    )


def test_int_to_string_in_base_hex():
    """
    Tests `int_to_string_in_base` with integers and hexadecimal base.
    It verifies that integers are correctly converted to their hexadecimal string representations.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=HEX_DIGIT_SET
    )
    assert (
        rebaser.int_to_string_in_base(15, rebaser.output_digit_set_list, 16)
        == "F"
    )
    assert (
        rebaser.int_to_string_in_base(26, rebaser.output_digit_set_list, 16)
        == "1A"
    )


def test_int_to_string_in_base_zero():
    """
    Tests `int_to_string_in_base` with an integer value of zero. It verifies that
    zero is correctly converted to its string representation using the first
    digit of the output set.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.int_to_string_in_base(0, rebaser.output_digit_set_list, 10)
        == "0"
    )


def test_int_to_string_in_base_length_1_output_digit_set():
    """
    Tests `int_to_string_in_base` when the output digit set has only one
    character. It verifies that the method returns an empty string when the base
    is 1, as there's no meaningful conversion.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=DECIMAL_DIGIT_SET, out_digit_set=SINGLE_CHAR_DIGIT_SET
    )
    assert (
        rebaser.int_to_string_in_base(10, rebaser.output_digit_set_list, 1)
        == ""
    )
    assert (
        rebaser.int_to_string_in_base(0, rebaser.output_digit_set_list, 1) == ""
    )


def test_int_to_string_in_base_invalid_base_raises_error():
    """
    Tests that `int_to_string_in_base` raises a ValueError when the base is invalid (e.g., 0).
    It verifies that an appropriate error message is provided.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=DECIMAL_DIGIT_SET
    )
    with pytest.raises(
        ValueError,
        match="Base must be greater than 0 for integer to string rebase.",
    ):
        rebaser.int_to_string_in_base(10, rebaser.output_digit_set_list, 0)


# Test cases for string_to_integer_and_bytes
def test_string_to_integer_and_bytes_simple_number():
    """
    Tests `string_to_integer_and_bytes` with a simple decimal number. It
    verifies that the decimal string is correctly converted to its integer
    representation as bytes and its bit length.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.string_to_integer_and_bytes(
        "10", rebaser.input_digit_set_map, rebaser.input_digit_set_list
    ) == (
        b"\x0a",
        4,
    )


def test_string_to_integer_and_bytes_binary_input():
    """
    Tests `string_to_integer_and_bytes` with a binary input string. It verifies
    that the binary string is correctly converted to its integer representation
    as bytes and its bit length.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=BINARY_DIGIT_SET
    )
    assert rebaser.string_to_integer_and_bytes(
        "101", rebaser.input_digit_set_map, rebaser.input_digit_set_list
    ) == (
        b"\x05",
        3,
    )


def test_string_to_integer_and_bytes_hex_input():
    """
    Tests `string_to_integer_and_bytes` with a hexadecimal input string. It
    verifies that the hexadecimal string is correctly converted to its integer
    representation as bytes and its bit length.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=HEX_DIGIT_SET
    )
    assert rebaser.string_to_integer_and_bytes(
        "F", rebaser.input_digit_set_map, rebaser.input_digit_set_list
    ) == (
        b"\x0f",
        4,
    )


def test_string_to_integer_and_bytes_empty_string_input():
    """
    Tests `string_to_integer_and_bytes` with an empty input string. It verifies
    that an empty string results in a byte array of `b"\x00"` and a bit length
    of 0.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.string_to_integer_and_bytes(
        "", rebaser.input_digit_set_map, rebaser.input_digit_set_list
    ) == (b"\x00", 0)


# Test cases for integer_bytes_to_string
def test_integer_bytes_to_string_simple_number():
    """
    Tests `integer_bytes_to_string` with a simple byte array representing a
    decimal number. It verifies that the byte array is correctly converted back
    to its decimal string representation.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.integer_bytes_to_string(b"\x0a", rebaser.output_digit_set_list)
        == "10"
    )


def test_integer_bytes_to_string_binary_output():
    """
    Tests `integer_bytes_to_string` with a byte array and a binary output digit
    set. It verifies that the byte array is correctly converted to its binary
    string representation.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=DECIMAL_DIGIT_SET, out_digit_set=BINARY_DIGIT_SET
    )
    assert (
        rebaser.integer_bytes_to_string(b"\x05", rebaser.output_digit_set_list)
        == "101"
    )


def test_integer_bytes_to_string_hex_output():
    """
    Tests `integer_bytes_to_string` with a byte array and a hexadecimal output
    digit set. It verifies that the byte array is correctly converted to its
    hexadecimal string representation.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=HEX_DIGIT_SET
    )
    assert (
        rebaser.integer_bytes_to_string(b"\x0f", rebaser.output_digit_set_list)
        == "F"
    )


def test_integer_bytes_to_string_empty_bytes_input():
    """
    Tests `integer_bytes_to_string` with an empty byte array input. It verifies
    that an empty byte array correctly results in the string representation of 0.
    """
    rebaser = DigitSetRebaser(
        in_digit_set=BINARY_DIGIT_SET, out_digit_set=DECIMAL_DIGIT_SET
    )
    assert (
        rebaser.integer_bytes_to_string(b"", rebaser.output_digit_set_list)
        == "0"
    )


# Test cases for rebase method (end-to-end) - now for number system rebasees
def test_rebase_binary_to_decimal() -> None:
    """
    Tests the end-to-end rebase functionality from binary to decimal.
    It verifies that binary strings are correctly converted to their decimal equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=BINARY_DIGIT_SET
    )
    assert rebaser.rebase("101") == "5"
    assert rebaser.rebase("1111") == "15"
    assert rebaser.rebase("0") == "0"


def test_rebase_decimal_to_hexadecimal() -> None:
    """
    Tests the end-to-end rebase functionality from decimal to hexadecimal.
    It verifies that decimal strings are correctly converted to their hexadecimal equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.rebase("255") == "FF"
    assert rebaser.rebase("10") == "A"
    assert rebaser.rebase("0") == "0"


def test_rebase_hexadecimal_to_binary() -> None:
    """
    Tests the end-to-end rebase functionality from hexadecimal to binary.
    It verifies that hexadecimal strings are correctly converted to their binary equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=HEX_DIGIT_SET
    )
    assert rebaser.rebase("F") == "1111"
    assert rebaser.rebase("A") == "1010"
    assert rebaser.rebase("10") == "10000"
    assert rebaser.rebase("0") == "0"


def test_rebase_octal_to_decimal() -> None:
    """
    Tests the end-to-end rebase functionality from octal to decimal.
    It verifies that octal strings are correctly converted to their decimal equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=OCTAL_DIGIT_SET
    )
    assert rebaser.rebase("10") == "8"
    assert rebaser.rebase("77") == "63"
    assert rebaser.rebase("0") == "0"


def test_rebase_custom_base_62_to_decimal() -> None:
    """
    Tests the end-to-end rebase functionality from a custom Base62 digit set to decimal.
    It verifies that Base62 strings are correctly converted to their decimal equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=BASE62_DIGIT_SET
    )
    assert rebaser.rebase("Z") == "61"
    assert rebaser.rebase("10") == "62"
    assert rebaser.rebase("g") == "16"
    assert rebaser.rebase("G") == "42"
    assert rebaser.rebase("0") == "0"


def test_rebase_decimal_to_custom_base_62() -> None:
    """
    Tests the end-to-end rebase functionality from decimal to a custom Base62 digit set.
    It verifies that decimal strings are correctly converted to their Base62 equivalents.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=BASE62_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.rebase("61") == "Z"
    assert rebaser.rebase("62") == "10"
    assert rebaser.rebase("42") == "G"
    assert rebaser.rebase("0") == "0"


def test_rebase_different_bases_large_number() -> None:
    """
    Tests the end-to-end rebase functionality for large numbers between different
    bases (hexadecimal to binary and vice-versa). It verifies that large numbers
    are correctly converted and re-converted, maintaining their value.
    """
    rebaser_hex_to_bin = DigitSetRebaser(
        out_digit_set=BINARY_DIGIT_SET, in_digit_set=HEX_DIGIT_SET
    )
    assert rebaser_hex_to_bin.rebase("FFFF") == "1111111111111111"

    rebaser_bin_to_hex = DigitSetRebaser(
        out_digit_set=HEX_DIGIT_SET, in_digit_set=BINARY_DIGIT_SET
    )
    assert rebaser_bin_to_hex.rebase("1111111111111111") == "FFFF"


def test_rebase_with_no_digit_sets_in_init() -> None:
    """
    Tests the `rebase` method when no digit sets are provided during
    `DigitSetRebaser` initialization. It verifies that the input string is
    returned as-is if no explicit digit sets are configured.
    """
    rebaser = DigitSetRebaser()
    assert rebaser.rebase("hello") == "hello"
    assert rebaser.rebase("") == ""


def test_rebase_with_only_input_digit_set_in_init_filters_chars() -> None:
    """
    Tests the `rebase` method when only an input digit set is provided during
    initialization. It verifies that the input string is filtered to include only
    characters present in the specified input digit set.
    """
    rebaser = DigitSetRebaser(in_digit_set=DECIMAL_DIGIT_SET)
    assert rebaser.rebase("123abc") == "123"
    assert rebaser.rebase("hello world") == ""
    assert rebaser.rebase("1a2b3c") == "123"
    assert rebaser.rebase("") == ""


def test_rebase_with_empty_or_invalid_input_string() -> None:
    """
    Tests the `rebase` method with empty or invalid input strings when both input
    and output digit sets are defined. It verifies that the method returns the
    first character of the output digit set (or an empty string if output set is
    empty) when the input string is empty or contains no valid characters from
    the input digit set.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DigitSet(name="ABC", digits="ABC", source="test"),
        in_digit_set=DECIMAL_DIGIT_SET,
    )
    assert rebaser.rebase("") == "A"
    assert rebaser.rebase("XYZ") == "A"


def test_rebase_with_single_char_output_digit_set() -> None:
    """
    Tests the `rebase` method when the output digit set contains only a single
    character. It verifies that the rebased string is empty, as a
    single-character output set cannot represent numbers greater than 0.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=SINGLE_CHAR_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.rebase("123") == ""
    assert rebaser.rebase("0") == ""


def test_rebase_with_explicitly_empty_input_digit_set() -> None:
    """
    Tests the `rebase` method when the input digit set is explicitly empty. It
    verifies that the rebased string is the first character of the output digit
    set (representing 0), as no valid input characters can be processed.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=DECIMAL_DIGIT_SET, in_digit_set=EMPTY_DIGIT_SET
    )
    assert rebaser.rebase("123") == "0"
    assert rebaser.rebase("abc") == "0"
    assert rebaser.rebase("") == "0"


def test_rebase_with_explicitly_empty_output_digit_set() -> None:
    """
    Tests the `rebase` method when the output digit set is explicitly empty. It
    verifies that the rebased string is always empty, as there are no characters
    to represent the output.
    """
    rebaser = DigitSetRebaser(
        out_digit_set=EMPTY_DIGIT_SET, in_digit_set=DECIMAL_DIGIT_SET
    )
    assert rebaser.rebase("123") == ""
    assert rebaser.rebase("0") == ""
    assert rebaser.rebase("") == ""
