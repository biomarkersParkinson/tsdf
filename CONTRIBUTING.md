# Contributing guidelines

We welcome any kind of contribution to our software, from simple comment or question to a full fledged [pull request](https://help.github.com/articles/about-pull-requests/). Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Types of Contributions

### Report Bugs

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Feel free to contribute to any part of the documentation, including official docs, docstrings, or web content like blog posts, articles, etc.

### Submit Feedback

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and contributions are welcome :)

## General Python Practices

When contributing to this project, please adhere to the following Python practices:

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for style guide recommendations.
- Ensure your code is clean, efficient, and well-documented. All methods must include documentation that follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), clearly describing the method's purpose, its arguments, return values, and any exceptions raised.

## Get Started!

Ready to contribute? Here's how to set up `tsdf` for local development.

1. Download a copy of `tsdf` locally.
2. Install `tsdf` using `poetry`:

    ```console
    $ poetry install
    ```

3. Create a branch for local development:

    ```console
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

4. Make your changes and ensure they meet the code formatting and documentation standards.

5. Check that your changes pass all tests.

6. Commit your changes and push to the branch:

    ```console
    $ git push origin name-of-your-bugfix-or-feature
    ```

7. Submit a pull request through GitHub.

## Pull Request Guidelines

Before you submit a pull request, ensure it meets these guidelines:

1. The pull request should include tests that prove any new functionality works as expected.
2. If the pull request adds functionality, the documentation should be updated accordingly.
3. The pull request should work for Python's currently supported versions and major operating systems.

## Code Style Guide

Please follow the coding standards and conventions outlined below when contributing to this project.

1. **Use PEP 8 for Python code**: We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. You can use tools like `black` to help enforce this.

2. **Naming Conventions**:
   * Function names: `snake_case`.
   * Class names: `PascalCase`.
   * Constants: `UPPER_CASE_WITH_UNDERSCORES`.

3. **Docstrings**: All public methods, functions, and classes should have clear and complete docstrings. We use the [NumPy docstring style guide](https://numpydoc.readthedocs.io/en/latest/format.html) for consistency. Here is an example:

    ```python
    def my_function(param1: int, param2: str) -> None:
        """
        Brief summary of the function.

        Parameters
        ----------
        param1 : int
            Description of `param1`.
        param2 : str
            Description of `param2`.

        Returns
        -------
        None
        """
        print(f"{param1}, {param2}")
    ```

4. **Type Annotations**: We use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints throughout the codebase. Please ensure that all functions and methods are properly annotated.

5. **Testing**: Ensure that your code is covered by unit tests. We use `pytest` for testing. Add new tests for any added functionality.

We appreciate your contributions and adherence to the style guide. This helps maintain the quality and readability of the codebase.

## Code of Conduct

Please note that the `tsdf` project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.
