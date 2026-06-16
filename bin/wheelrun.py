"""
Simplified wheel test script.

Installs a built wheel in a temporary venv and runs import + CLI smoke tests.
"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile


def test_local_wheel(project_root_dir):
    dist_dir = os.path.join(project_root_dir, "dist")
    wheel_files = glob.glob(os.path.join(dist_dir, "*.whl"))
    if not wheel_files:
        print(f"Error: No .whl files found in '{dist_dir}'. Run 'uv build' first.")
        sys.exit(1)

    latest_wheel = max(wheel_files, key=os.path.getmtime)
    print(f"Testing wheel: {os.path.basename(latest_wheel)}")

    temp_dir = tempfile.mkdtemp(prefix="wheel_test_")
    try:
        print(f"Creating temporary venv in {temp_dir}")
        subprocess.run(
            [sys.executable, "-m", "venv", os.path.join(temp_dir, "venv")],
            check=True,
            capture_output=True,
            text=True,
        )

        pip = os.path.join(temp_dir, "venv", "bin", "pip")
        python = os.path.join(temp_dir, "venv", "bin", "python")
        if os.name == "nt":
            pip = os.path.join(temp_dir, "venv", "Scripts", "pip")
            python = os.path.join(temp_dir, "venv", "Scripts", "python")

        print("Installing wheel...")
        subprocess.run(
            [pip, "install", latest_wheel],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Wheel installed successfully.")

        print("Running import test...")
        subprocess.run(
            [
                python,
                "-c",
                "import basebender; print(f'OK version {basebender.VERSION}')",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Import test passed.")

        print("Running CLI smoke test...")
        result = subprocess.run(
            [python, "-m", "basebender.cli", "111", "01234", "01"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"CLI test passed. Output: {result.stdout.strip()}")

        print("\nAll tests PASSED!")

    except subprocess.CalledProcessError as e:
        print(f"\nFAILED: {e.stderr or e.stdout}")
        sys.exit(1)
    finally:
        shutil.rmtree(temp_dir)
        print(f"Cleaned up {temp_dir}")


if __name__ == "__main__":
    test_local_wheel(os.getcwd())
