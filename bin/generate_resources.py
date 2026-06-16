#!/usr/bin/env python3
"""
This script generates Python resource files from Qt .qrc files using pyside6-rcc.
"""

import os
import subprocess
import sys


def main():
    qrc_file = "src/basebender/rebaser/resources/app_resources.qrc"
    output_dir = "src/basebender/rebaser/generated"
    output_file = os.path.join(output_dir, "app_resources_rc.py")

    print(f"Starting resource generation from: {qrc_file}")
    print(f"Output will be saved to: {output_file}")

    os.makedirs(output_dir, exist_ok=True)

    try:
        command = ["uv", "run", "pyside6-rcc", qrc_file, "-o", output_file]

        print(f"Executing command: {' '.join(command)}")

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        if result.stdout:
            print("pyside6-rcc stdout:")
            print(result.stdout)
        if result.stderr:
            print("pyside6-rcc stderr:")
            print(result.stderr)

        print(f"Successfully generated {output_file}")

    except FileNotFoundError:
        print(
            "'pyside6-rcc' command not found. Skipping the re-generation of the icons",
            file=sys.stdout,
        )
        print("You can install it with: uv add pyside6", file=sys.stderr)
    except subprocess.CalledProcessError as process_error:
        print(
            "Skipping the re-generation of the icons",
            file=sys.stdout,
        )
        print(f"Command: {' '.join(process_error.cmd)}", file=sys.stderr)
        print(f"Stderr: {process_error.stderr}", file=sys.stderr)
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
