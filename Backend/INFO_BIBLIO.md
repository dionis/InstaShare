
## UV Pytest

uv is a fast Python package and project manager written in Rust, designed as a drop-in replacement for pip and pip-compile. pytest is a popular Python testing framework.
To use pytest with uv, you typically follow these steps: Add pytest as a development dependency.
Código

    uv add --dev pytest

If you also want test coverage reporting, you can add pytest-cov:
Código

    uv add --dev pytest-cov

run your tests.
Use uv run to execute pytest within the project's virtual environment:
Código

    uv run pytest

For more detailed output during test execution, you can add the verbose flag:
Código

    uv run pytest -v

    Run tests with coverage (if pytest-cov is installed):

Código

    uv run pytest --cov=<your_module_name>

To generate a more detailed coverage report, you can add the --cov-report flag:
Código

    uv run pytest --cov=<your_module_name> --cov-report=term-missing