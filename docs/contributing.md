# Contributing & Development Guide

Thank you for contributing to `pyjsonparser`! This guide provides everything you need to set up your environment, run tests, and release new versions.

---

## 🛠️ Development Setup

### Prerequisites

- **Python**: 3.12 or later
- **Poetry**: 2.0+ (recommended for dependency management) or standard `pip`/`venv`
- **Git**

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexprodan99/pyjsonparser.git
   cd pyjsonparser/pyjsonparser
   ```

2. **Install dependencies**:
   ```bash
   poetry install --with test
   ```
   Or using pip in a virtual environment:
   ```bash
   pip install -e . pytest build
   ```

---

## 🧪 Running Tests

We use `pytest` for unit testing:

```bash
# Using poetry
poetry run pytest

# Or directly in your activated virtual environment
pytest
```

All test cases are located under `pyjsonparser/tests/`. Ensure all tests pass before opening a Pull Request.

---

## 📦 Building the Package

To build the wheel and source distribution locally:

```bash
python -m build
```

This will produce the binary wheel (`.whl`) and source tarball (`.tar.gz`) under `pyjsonparser/dist/`.

---

## 🚀 Release & Publishing Pipeline

The project uses GitHub Actions with **PyPI Trusted Publishing (OIDC)** to securely publish distributions to PyPI without long-lived API tokens.

### How to Release a New Version

1. **Update the version**:
   Update the `version` field in `pyjsonparser/pyproject.toml` (e.g. `0.2.0`).

2. **Commit and Tag**:
   ```bash
   git commit -am "chore: bump version to 0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```

3. **Automated Publishing**:
   Pushing a tag starting with `v*` automatically triggers the `.github/workflows/publish.yml` workflow, which:
   - Builds the wheel and source tarball.
   - Installs the distribution and executes the test suite.
   - Exchanges GitHub's OIDC token with PyPI using Trusted Publishing.
   - Uploads the package to [PyPI](https://pypi.org/project/pyjsonparser/).
