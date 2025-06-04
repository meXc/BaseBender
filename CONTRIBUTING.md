# Contribution Guidelines

We welcome contributions to this project! To ensure a smooth and collaborative experience for everyone, please follow these guidelines.

## How to Contribute

We follow the standard GitHub flow for contributions:

1.  **Fork the repository:** Create a copy of the repository under your GitHub account.
2.  **Clone your fork:** Download your forked repository to your local machine.
3.  **Create a topic branch:** Create a new branch for your feature or bug fix (e.g., `feature/add-new-feature` or `bugfix/fix-issue-123`).
4.  **Commit your changes:** Make your changes and commit them with clear, concise messages.
5.  **Push to your fork:** Push your new branch and commits to your forked repository on GitHub.
6.  **Open a Pull Request (PR):** Open a pull request from your topic branch to the `main` branch of the upstream repository.

**Environment Setup:**
Please use [Poetry](https://python-poetry.org/) for dependency management and virtual environment setup. After cloning the repository, navigate to the project root and run:

```bash
poetry install
```

This will install all project dependencies and set up a virtual environment. You can then activate the environment using `poetry shell`.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report any unacceptable behavior to the project's owner.

## Reporting Bugs

When reporting a bug, please provide as much detail as possible to help us reproduce and fix the issue quickly. Bug reports should include:

*   **Steps to reproduce:** A clear, numbered list of steps that consistently lead to the bug.
*   **Expected behavior:** What you expected to happen.
*   **Actual behavior:** What actually happened.
*   **Environment details:** Your operating system, Python version, and any relevant library versions.
*   **Screenshots/Logs:** If applicable, include screenshots or relevant log output.

Please use the provided GitHub Issues template for bug reports.

## Suggesting Enhancements/Features

If you have an idea for an enhancement or a new feature, please open a feature request. Include the following details:

*   **Problem Description:** Clearly describe the problem your enhancement/feature aims to solve.
*   **Proposed Solution:** Explain your proposed solution in detail.
*   **Use Cases:** Describe how this enhancement/feature would be used.
*   **Alternatives Considered:** Briefly mention any other solutions you considered and why you chose this one.

Please use the provided GitHub Issues template for feature requests.

## Pull Request Guidelines

To ensure your pull request can be reviewed and merged efficiently, please adhere to the following:

*   **Pass Basic Tests:** Ensure your changes pass all existing tests.
*   **Commit Messages:** While informal commit messages are acceptable, strive for clarity and conciseness.
*   **Reviewers:** There is no specific number of required reviewers; however, your PR will be reviewed by a project maintainer.
*   **Merging:** We prefer a fast-forward merge strategy when integrating changes.

## Development Setup

To set up your local development environment, run the setup script:

```bash
./bin/setup_project.sh
```

## Testing

*   **Running Tests:** Contributors should run tests using `pytest`. From the project root, with your Poetry environment activated, run:
    ```bash
    pytest
    ```
*   **New Tests:** New features and bug fixes should include new tests to cover the added or modified functionality.
*   **Test Coverage:** While new tests are encouraged, there are no strict test coverage requirements.

## Documentation Guidelines

*   **In-Code Documentation:**
    *   Provide clear docstrings for all functions, classes, and methods.
    *   Use inline comments where necessary to explain complex logic or non-obvious code sections.
*   **External Documentation:**
    *   Any external documentation in the `docs/` directory should be updated using Markdown.

## Style Guides

*   **Coding Style:** Adhere to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). We use automated tools to enforce this:
    *   **Black:** An opinionated code formatter that ensures consistent code style.
    *   **isort:** A tool to sort Python imports alphabetically and by type.
    *   **Pylint:** A static code analyzer that checks for errors, enforces a coding standard, and looks for bad smells.
*   **Automated Checks (pre-commit):** We use `pre-commit` hooks to automatically run `black`, `isort`, and `pylint` before each commit. To set up these hooks, run the following commands after `poetry install`:
    ```bash
    poetry run pre-commit install
    ```
    You can also manually run all hooks on all files with:
    ```bash
    poetry run pre-commit run --all-files
    ```
    Please ensure your code passes all these checks before submitting a pull request.

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE). Please ensure your contributions are compatible with this license.
