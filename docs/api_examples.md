# API Usage Examples

This document provides detailed examples for using the BaseBender FastAPI.

## Running the FastAPI Server

To start the FastAPI server, use the `--api` flag with the CLI:

```bash
poetry run python cli.py --api
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Usage (API)

The API provides two main endpoints: `/digitsets` and `/rebase`.

### `GET /digitsets`

*   **Description**: Retrieves a list of all available digit sets.
*   **Response**: A JSON array of objects, each representing a digit set with its `id` (e.g., "package:ASCII"), `name`, `digits`, and `source` (e.g., "package", "system", "user").

**Example Request (using `curl`)**:
```bash
curl http://127.0.0.1:8000/digitsets
```

**Example Response**:
```json
[
  {
    "id": "package:Binary",
    "name": "Binary",
    "digits": "01",
    "source": "package"
  },
  {
    "id": "package:Decimal",
    "name": "Decimal",
    "digits": "0123456789",
    "source": "package"
  }
]
```

### `POST /rebase`

*   **Description**: Rebasees input text from a source digit set to a target digit set.
*   **Request Body**: JSON object with optional fields:
    *   `input_text` (string, optional): The text to be rebased. Defaults to an empty string.
    *   `source_digit_set` (string, optional): The direct string representation of the source digit set. Takes precedence over `source_digit_set_id`.
    *   `source_digit_set_id` (string, optional): The unique ID of the source digit set (e.g., "package:Binary"). If `source_digit_set` is omitted, this is used. If both are omitted, the source digit set is dynamically derived from `input_text`.
    *   `target_digit_set` (string, optional): The direct string representation of the target digit set. Takes precedence over `target_digit_set_id`.
    *   `target_digit_set_id` (string, optional): The unique ID of the target digit set. If `target_digit_set` is omitted, this is used. If both are omitted, the input string is returned with digits not in the derived/provided source digit set removed. If the target digit set has a length of 1, an empty string will be returned.
*   **Response**: A JSON object containing `rebased_text`, `source_digit_set_used`, `target_digit_set_used`, and an optional `error` object with `message` and `detail` fields.

**Example Request (using `curl`)**: Rebase "101" (Binary) to Decimal using IDs.
```bash
curl -X POST "http://127.0.0.1:8000/rebase" -H "Content-Type: application/json" -d '{
  "input_text": "101",
  "source_digit_set_id": "package:Binary",
  "target_digit_set_id": "package:Decimal"
}'
```

**Example Response**:
```json
{
  "rebased_text": "5",
  "source_digit_set_used": "Binary",
  "target_digit_set_used": "Decimal",
  "error": null
}
```

**Example Request (using `curl`)**: Rebase "hello" to "01" using direct digit set strings.
```bash
curl -X POST "http://127.0.0.1:8000/rebase" -H "Content-Type: application/json" -d '{
  "input_text": "hello",
  "source_digit_set": "abcdefghijklmnopqrstuvwxyz",
  "target_digit_set": "01"
}'
```

**Example Response**:
```json
{
  "rebased_text": "100101100000",
  "source_digit_set_used": "Provided: 'abcdefghijklmnopqrstuvwxyz'",
  "target_digit_set_used": "Provided: '01'",
  "error": null
}
```

**Example Request (using `curl`)**: Filter "hello world!" with "abcdefghijklmnopqrstuvwxyz" digit set.
```bash
curl -X POST "http://127.0.0.1:8000/rebase" -H "Content-Type: application/json" -d '{
  "input_text": "hello world!",
  "source_digit_set_id": "package:ASCII Printable"
}'
```

**Example Response**:
```json
{
  "rebased_text": "hello world",
  "source_digit_set_used": "ASCII Printable",
  "target_digit_set_used": "Echo Input",
  "error": null
}
```

**Example Request (using `curl`)**: Rebase "123" to a single-character digit set.
```bash
curl -X POST "http://127.0.0.1:8000/rebase" -H "Content-Type: application/json" -d '{
  "input_text": "123",
  "source_digit_set_id": "package:Decimal",
  "target_digit_set_id": "package:Binary" # Assuming Binary is defined as "0" or "1" for this example
}'
```

**Example Response**:
```json
{
  "rebased_text": "",
  "source_digit_set_used": "Decimal",
  "target_digit_set_used": "Binary",
  "error": null
}
```

**Example Error Response (Invalid Digit Set ID)**:
```json
{
  "rebased_text": "",
  "source_digit_set_used": "Dynamically Derived",
  "target_digit_set_used": "Echo Input",
  "error": {
    "message": "Invalid Source Digit Set ID",
    "detail": "Source digit set with ID 'package:NonExistent' not found."
  }
}
```

**Example Error Response (Rebase Error)**:
```json
{
  "rebased_text": "",
  "source_digit_set_used": "Provided: '01'",
  "target_digit_set_used": "Provided: '0'",
  "error": {
    "message": "Rebase Error",
    "detail": "A value error occurred during rebase: Base must be greater than 0 for integer to string rebase."
  }
}
