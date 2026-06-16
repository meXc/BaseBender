"""
This module provides the core logic for rebasing strings between different
digit sets.

It includes the `DigitSetRebaser` class, which handles the conversion of
strings from an input digit set to an output digit set, supporting dynamic
derivation of the input digit set and various rebase operations.
"""

from .models import DigitSet


class DigitSetRebaser:
    """
    A class to rebase strings between different digit sets (positional number
    systems).

    It supports explicit input and output digit sets, or dynamic derivation of
    the input digit set based on the input string.
    """

    def __init__(
        self,
        out_digit_set: DigitSet | None = None,
        in_digit_set: DigitSet | None = None,
    ) -> None:
        self._initial_input_digit_set: DigitSet | None = in_digit_set
        self._initial_output_digit_set: DigitSet | None = out_digit_set
        self._in_digit_set_map: dict[str, int] = {}
        self._in_digit_set_list: list[str] = []
        self._out_digit_set_map: dict[str, int] = {}
        self._out_digit_set_list: list[str] = []

        # Output digit set is always explicitly set or None;
        # not dynamically determined in __init__
        if out_digit_set:
            out_digits = DigitSet.deduplicate_digits(out_digit_set.digits)
            self._out_digit_set_map = {char: i for i, char in enumerate(out_digits)}
            self._out_digit_set_list = list(out_digits)

        # Input digit set is dynamically determined in rebase
        # if _initial_input_digit_set is None
        if in_digit_set:
            in_digits = DigitSet.deduplicate_digits(in_digit_set.digits)
            self._in_digit_set_map = {char: i for i, char in enumerate(in_digits)}
            self._in_digit_set_list = list(in_digits)

    @property
    def initial_input_digit_set(
        self,
    ) -> DigitSet | None:
        """
        The initial input digit set provided during initialization.

        Examples:
            >>> rebaser = DigitSetRebaser(in_digit_set=DigitSet("0123456789"))
            >>> rebaser.initial_input_digit_set.digits
            '0123456789'
        """
        return self._initial_input_digit_set

    @property
    def initial_output_digit_set(
        self,
    ) -> DigitSet | None:
        """
        The initial output digit set provided during initialization.

        Examples:
            >>> rebaser = DigitSetRebaser(out_digit_set=DigitSet("abc"))
            >>> rebaser.initial_output_digit_set.digits
            'abc'
        """
        return self._initial_output_digit_set

    @property
    def input_digit_set_map(
        self,
    ) -> dict[str, int]:
        """
        A dictionary mapping characters to their integer positions for the input digit set.

        Examples:
            >>> rebaser = DigitSetRebaser(in_digit_set=DigitSet("012"))
            >>> rebaser.input_digit_set_map
            {'0': 0, '1': 1, '2': 2}
        """
        return self._in_digit_set_map

    @property
    def input_digit_set_list(
        self,
    ) -> list[str]:
        """
        An ordered list of characters representing the input digit set.

        Examples:
            >>> rebaser = DigitSetRebaser(in_digit_set=DigitSet("abc"))
            >>> rebaser.input_digit_set_list
            ['a', 'b', 'c']
        """
        return self._in_digit_set_list

    @property
    def output_digit_set_map(
        self,
    ) -> dict[str, int]:
        """
        A dictionary mapping characters to their integer positions for the output digit set.

        Examples:
            >>> rebaser = DigitSetRebaser(out_digit_set=DigitSet("xyz"))
            >>> rebaser.output_digit_set_map
            {'x': 0, 'y': 1, 'z': 2}
        """
        return self._out_digit_set_map

    @property
    def output_digit_set_list(
        self,
    ) -> list[str]:
        """
        An ordered list of characters representing the output digit set.

        Examples:
            >>> rebaser = DigitSetRebaser(out_digit_set=DigitSet("789"))
            >>> rebaser.output_digit_set_list
            ['7', '8', '9']
        """
        return self._out_digit_set_list

    @staticmethod
    def char_to_position(char: str, digit_set_map: dict[str, int]) -> int:
        """
        Converts a character to its numerical position within a given digit set map.

        Args:
            char: The character to convert.
            digit_set_map: A dictionary mapping characters to their integer positions.

        Returns:
            The integer position of the character.

        Raises:
            ValueError: If the character is not found in the digit set.
        """
        if char not in digit_set_map:
            raise ValueError(f"Character '{char}' not found in the digit set.")
        return digit_set_map[char]

    @staticmethod
    def position_to_char(position: int, digit_set_list: list[str]) -> str:
        """
        Converts a numerical position to its corresponding character in a digit set list.

        Args:
            position: The integer position to convert.
            digit_set_list: An ordered list of characters representing the digit set.

        Returns:
            The character at the specified position.

        Raises:
            IndexError: If the position is out of bounds for the digit set.
        """
        if not 0 <= position < len(digit_set_list):
            raise IndexError(f"Position {position} is out of bounds for the digit set.")
        return digit_set_list[position]

    @staticmethod
    def string_to_int_from_base(input_str: str, digit_set_map: dict[str, int], base: int) -> int:
        """
        Converts a string representation of a number from a given base to an integer.

        Characters not present in the `digit_set_map` are ignored.

        Args:
            input_str: The input string to convert.
            digit_set_map: A dictionary mapping characters to their integer positions
                           in the source digit set.
            base: The base of the input string's number system (length of the source digit set).

        Returns:
            The integer representation of the input string.
        """
        filtered_input_str = [char for char in input_str if char in digit_set_map]

        if not filtered_input_str:
            return 0

        integer_value = 0
        power = 0
        for char in reversed(filtered_input_str):
            position = digit_set_map[char]
            integer_value += position * (base**power)
            power += 1
        return integer_value

    @staticmethod
    def int_to_string_in_base(integer_value: int, digit_set_list: list[str], base: int) -> str:
        """
        Converts an integer to its string representation in a given base.

        Args:
            integer_value: The integer to convert.
            digit_set_list: An ordered list of characters representing the target digit set.
            base: The base of the target number system (length of the target digit set).

        Returns:
            The string representation of the integer in the target base.

        Raises:
            ValueError: If the base is not greater than 0.
        """
        if base <= 0:
            raise ValueError("Base must be greater than 0 for integer to string rebase.")

        if base == 1:
            return ""

        if integer_value == 0:
            return digit_set_list[0]

        result_chars: list[str] = []
        while integer_value > 0:
            remainder = integer_value % base
            result_chars.append(digit_set_list[remainder])
            integer_value //= base

        return "".join(reversed(result_chars))

    def rebase(self, input_string: str) -> str:
        """
        Rebases the input string from its determined input digit set to the
        specified output digit set.

        This method handles various scenarios:
        - If `input_string` is empty, returns the first character of the output
          digit set if available, otherwise an empty string.
        - If neither input nor output digit sets are explicitly provided,
          returns the input string as-is.
        - If only the output digit set is provided, the input digit set is
          dynamically derived from the `input_string`.
        - If only the input digit set is provided, the input string is filtered
          to include only characters present in the input digit set.
        - If both are provided or derived, performs the full rebase operation.

        Args:
            input_string: The string to be rebased.

        Returns:
            The rebased string.
        """
        if not input_string:
            return self._out_digit_set_list[0] if self._out_digit_set_list else ""

        effective_input_digit_set_map: dict[str, int]
        effective_input_digit_set_list: list[str]

        if self._initial_input_digit_set:
            effective_input_digit_set_map = self._in_digit_set_map
            effective_input_digit_set_list = self._in_digit_set_list
        else:
            # Dynamically derive input digit set from input_string
            derived_digits = DigitSet.deduplicate_digits(input_string)
            effective_input_digit_set_map = {char: i for i, char in enumerate(derived_digits)}
            effective_input_digit_set_list = list(derived_digits)

        # Scenario 1: No explicit output digit set, and no initial input digit set
        # (meaning input digit set was dynamically derived).
        # In this case, just return the input string as is.
        if self._initial_output_digit_set is None and self._initial_input_digit_set is None:
            return input_string

        # Scenario 2: No explicit output digit set, but an initial input digit set
        # was provided. Filter the input string based on the provided input digit set.
        if self._initial_output_digit_set is None and self._initial_input_digit_set is not None:
            filtered_string = "".join(
                char for char in input_string if char in effective_input_digit_set_map
            )
            return filtered_string

        # If the effective input digit set is empty or has only one character,
        # and we are supposed to rebase, return the first char of output or empty.
        if not effective_input_digit_set_list or len(effective_input_digit_set_list) <= 1:
            return self._out_digit_set_list[0] if self._out_digit_set_list else ""

        # If the output digit set is empty, return an empty string
        if not self._out_digit_set_list:
            return ""

        # Perform the full rebase
        integer_value = self.string_to_int_from_base(
            input_string,
            effective_input_digit_set_map,
            len(effective_input_digit_set_list),
        )
        final_rebased_string = self.int_to_string_in_base(
            integer_value,
            self._out_digit_set_list,
            len(self._out_digit_set_list),
        )
        return final_rebased_string
