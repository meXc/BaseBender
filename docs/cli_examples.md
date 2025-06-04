# CLI Usage Examples

This document provides detailed examples for using the BaseBender command-line interface (CLI).

## Rebase Scenarios

The `DigitSetRebaser` class offers flexible rebaseing based on the provided digit sets during initialization.

### CLI Argument Order: `[input_string] [output_digit_set_string (optional)] [input_digit_set_string (optional)]`

#### 1. Full Rebase (Input and Output Digit Sets Defined)

Rebase `input_string` from `input_digit_set` to `output_digit_set`. This is the standard base rebaseing behavior.

```bash
poetry run python cli.py "input_string_to_rebase" "output_digit_set_string" "input_digit_set_string"
```

**Example**: Rebase "hello" from standard alphabet to a custom alphabet.

```bash
poetry run python cli.py "hello" "zyxwuvtsrqponmlkjihgfedcba" "abcdefghijklmnopqrstuvwxyz"
```

#### 2. Output Digit Set Only (Input Digit Set Derived from Input String)

If only the `output_digit_set` is provided (and `input_digit_set` is omitted), the input digit set will be dynamically derived from the unique digits present in the `input_string` itself.

```bash
poetry run python cli.py "input_string_to_rebase" "output_digit_set_string"
```

**Example**: Rebase "101" (binary, derived from input) to decimal.

```bash
poetry run python cli.py "101" "0123456789"
# Output: Rebased string: 5
```

#### 3. Input Digit Set Only (Output Digit Set Filters Input)

If only the `input_digit_set` is provided (and `output_digit_set` is omitted), the `rebase` method will return the `input_string` with any digits not present in the `input_digit_set` removed.

```bash
poetry run python cli.py "input_string_to_rebase" "" "input_digit_set_string"
```

**Example**: Rebase "hello world!" using only the "abcdefghijklmnopqrstuvwxyz" digit set.
```bash
poetry run python cli.py "hello world!" "" "abcdefghijklmnopqrstuvwxyz"
# Output: Rebased string: helloworld
```

#### 4. No Digit Sets Defined (Input String Returned Directly / Echo)

If neither `output_digit_set` nor `input_digit_set` is provided, the `rebase` method will simply return the `input_string` as is.

```bash
poetry run python cli.py "input_string_to_rebase"
```

**Example**:
```bash
poetry run python cli.py "test"
# Output: Rebased string: test
