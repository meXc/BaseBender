"""
This script tests the locally built Python wheel file.

It performs the following steps:
1. Extracts Python requirements from the main project's pyproject.toml.
2. Finds the latest .whl file in the 'dist' directory.
3. Creates a temporary Poetry environment.
4. Installs the local .whl file into the temporary environment.
5. Runs a basic import test of the installed package.
6. Runs a CLI command test using the installed package.
7. Cleans up the temporary directory.
"""

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import toml

# You'll need to install this if you don't have it: pip install toml


def _get_project_metadata(project_data: dict):
    """
    Extracts Python requirements from pyproject.toml and finds the latest wheel.
    Updates project_data dictionary in place.
    """
    main_pyproject_path = project_data["main_pyproject_path"]
    if not os.path.exists(main_pyproject_path):
        print(f"Error: pyproject.toml not found at '{main_pyproject_path}'.")
        sys.exit(1)

    try:
        main_pyproject_data = toml.load(main_pyproject_path)
        project_data["requires_python_range"] = main_pyproject_data[
            "project"
        ].get("requires-python", project_data["requires_python_range"])
        print(
            "Detected main project's requires-python: "
            f"{project_data['requires_python_range']}"
        )
    except (toml.TomlDecodeError, FileNotFoundError) as exc:
        print(f"Error reading pyproject.toml: {exc}")
        sys.exit(1)

    wheel_files = glob.glob(os.path.join(project_data["dist_dir"], "*.whl"))
    if not wheel_files:
        print(
            f"Error: No .whl files found in '{project_data['dist_dir']}'. "
            "Please run 'poetry build' or similar first."
        )
        sys.exit(1)

    project_data["latest_wheel"] = max(wheel_files, key=os.path.getmtime)
    print(
        f"Found latest wheel: {os.path.basename(project_data['latest_wheel'])}"
    )

    try:
        # Assuming format basebender-0.1.1-cp313-cp313-manylinux_2_39_x86_64.whl
        python_abi_tag = project_data["latest_wheel"].split("-")[-3]
        if python_abi_tag.startswith("cp"):
            python_version_from_wheel = python_abi_tag[2:]
            project_data["python_version_for_env"] = (
                f"{python_version_from_wheel[0]}."
                f"{python_version_from_wheel[1:]}"
            )
        else:
            print(
                "Warning: ABI tag not 'cp'. "
                "Attempting to parse from requires-python range."
            )
            match = re.search(
                r">=(\d+\.\d+)", project_data["requires_python_range"]
            )
            if match:
                project_data["python_version_for_env"] = match.group(1)
            else:
                raise ValueError(
                    "Could not determine Python version from wheel or "
                    "requires-python."
                )

        print(
            "Detected wheel/project target Python version for testing: "
            f"{project_data['python_version_for_env']}"
        )
    except ValueError as exc:
        print(
            "Warning: Could not reliably determine Python version from wheel filename "
            f"or requires-python. Defaulting to {project_data['python_version_for_env']}. "
            f"Error: {exc}"
        )


def _setup_poetry_environment(project_data: dict):
    """
    Creates and initializes a temporary Poetry environment.
    Updates project_data dictionary with the temporary directory path.
    """
    project_data["temp_test_dir"] = tempfile.mkdtemp(
        prefix="poetry_test_install_"
    )
    print(f"Created temporary test directory: {project_data['temp_test_dir']}")

    print(
        "Initializing temporary Poetry project with specific Python requirement..."
    )
    subprocess.run(
        [
            "poetry",
            "init",
            "--no-interaction",
            "--name",
            "temp-test-project",
            "--python",
            project_data["requires_python_range"],
        ],
        cwd=project_data["temp_test_dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    print("Poetry project initialized.")

    print(
        "Configuring Poetry environment to use Python "
        f"{project_data['python_version_for_env']}..."
    )
    subprocess.run(
        ["poetry", "env", "use", project_data["python_version_for_env"]],
        cwd=project_data["temp_test_dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(
        "Poetry environment configured for Python "
        f"{project_data['python_version_for_env']}."
    )


def _install_and_run_tests(project_data: dict):
    """
    Installs the local wheel and runs import and CLI tests.
    """
    install_cmd = ["poetry", "add", project_data["latest_wheel"]]
    print(f"Installing local wheel: {' '.join(install_cmd)}")
    subprocess.run(
        install_cmd,
        cwd=project_data["temp_test_dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    print("Local wheel installed successfully.")

    print(f"Running import test for '{project_data['package_name']}'...")
    test_script_import = (
        f"import {project_data['package_name']}; "
        f"print(f'{project_data['package_name']} imported successfully. "
        f"Version: {{ {project_data['package_name']}.VERSION }}')"
    )
    subprocess.run(
        ["poetry", "run", "python", "-c", test_script_import],
        cwd=project_data["temp_test_dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"'{project_data['package_name']}' import test passed!")

    # 6. Run the primary CLI command test
    # <--- IMPORTANT: Customize the CLI command here if your project's CLI changes
    cli_command = ["poetry", "run", "basebender", "111", "01234", "01"]
    print(f"\nRunning primary CLI command: '{' '.join(cli_command[2:])}'")
    cli_output = subprocess.run(
        cli_command,
        cwd=project_data["temp_test_dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    print("CLI command executed successfully.")
    print("CLI STDOUT:")
    print(cli_output.stdout)
    if cli_output.stderr:
        print("CLI STDERR:")
        print(cli_output.stderr)

    # Run additional CLI commands from the dictionary
    if project_data["additional_cli_tests"]:
        print("\nRunning additional CLI tests...")
        for test_name, command_args in project_data[
            "additional_cli_tests"
        ].items():
            full_command = ["poetry", "run"] + command_args
            print(
                f"\n--- Running additional test: '{test_name}' ({' '.join(command_args)}) ---"
            )
            additional_cli_output = subprocess.run(
                full_command,
                cwd=project_data["temp_test_dir"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"Test '{test_name}' executed successfully.")
            print("STDOUT:")
            print(additional_cli_output.stdout)
            if additional_cli_output.stderr:
                print("STDERR:")
                print(additional_cli_output.stderr)
            print(f"--- Test '{test_name}' completed ---")


def test_local_wheel(project_root_dir):
    """
    Tests the locally built wheel file by installing it in a temporary Poetry
    environment and performing a basic import test and a CLI test.

    Args:
        project_root_dir (str): The path to your main project directory
                                (e.g., where pyproject.toml and dist/ are).
    """
    print(f"Starting local wheel test for project at: {project_root_dir}")

    # Initialize a dictionary to hold all project-related data
    project_data = {
        "project_root_dir": project_root_dir,
        "main_pyproject_path": os.path.join(project_root_dir, "pyproject.toml"),
        "dist_dir": os.path.join(project_root_dir, "dist"),
        "requires_python_range": ">=3.8",  # Default value
        "latest_wheel": None,
        "python_version_for_env": "3.13",  # Robust fallback default
        "temp_test_dir": None,
        "package_name": "basebender",  # <--- IMPORTANT: Customize this if your project name changes
        # Dictionary for additional CLI commands to run
        "additional_cli_tests": {
            # Example: Add your additional commands here.
            # The value should be a list of strings, just like for subprocess.run.
            # These commands will be run using 'poetry run' implicitly.
            # "test_version_command": ["your-cli-command", "--version"],
            # "test_help_command": ["your-cli-command", "--help"],
        },
    }

    try:
        _get_project_metadata(project_data)
        _setup_poetry_environment(project_data)
        _install_and_run_tests(project_data)

        print("\nLocal wheel test COMPLETED SUCCESSFULLY!")

    except subprocess.CalledProcessError as sub_exc:
        print("\nError during testing:")
        print(f"Command: {' '.join(sub_exc.cmd)}")
        print(f"Return Code: {sub_exc.returncode}")
        print(f"STDOUT:\n{sub_exc.stdout}")
        print(f"STDERR:\n{sub_exc.stderr}")
        print("\nLocal wheel test FAILED.")
        sys.exit(1)
    finally:
        # 7. Clean up the temporary directory
        if project_data["temp_test_dir"] and os.path.exists(
            project_data["temp_test_dir"]
        ):
            print(
                f"\nCleaning up temporary directory: {project_data['temp_test_dir']}"
            )
            shutil.rmtree(project_data["temp_test_dir"])
            print("Cleanup complete.")


if __name__ == "__main__":
    project_root = os.getcwd()
    test_local_wheel(project_root)
