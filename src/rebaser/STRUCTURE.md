# `src/rebaser/` Directory Structure

This directory contains the core rebase logic and related modules.

## Folders:

*   [`resources/`](src/rebaser/resources/STRUCTURE.md): Contains resources such as data files and icons.

## Files:

*   [`__init__.py`](src/rebaser/__init__.py): Initializes the `rebaser` package.
*   [`config_loader.py`](src/rebaser/config_loader.py): Handles tiered configuration loading for digit sets.
*   [`digit_set_rebaser.py`](src/rebaser/digit_set_rebaser.py): Implements the core rebase logic.
*   [`digit_sets.py`](src/rebaser/digit_sets.py): Provides access to pre-defined digit sets and discovery mechanisms.
*   [`generated/app_resources_rc.py`](src/rebaser/generated/app_resources_rc.py): Python module generated from `app_resources.qrc` for Qt resources.
*   [`models.py`](src/rebaser/models.py): Defines data models used within the rebaser module.
