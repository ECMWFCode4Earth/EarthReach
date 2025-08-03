# EarthReach Agent: Dual-LLM Framework for Validated Meteorological Chart Descriptions

<p align="center">
  <a href="https://opensource.org/licenses/apache-2-0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0">
  </a>
  <a href="https://github.com/ECMWFCode4Earth/earthreach/releases">
    <img src="https://img.shields.io/github/v/release/ECMWFCode4Earth/earthreach?color=blue&label=Release&style=flat-square" alt="Latest Release">
  </a>
  <a href="https://earthreach.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/earthreach/badge/?version=latest" alt="Documentation Status">
  </a>
</p>

## EarthReach

EarthReach is a challenge from the 2025 edition dedicated to enhancing the accessibility of meteorological data visualisations produced by Earthkit, by equipping the plots module with LLM-powered alternative text generation capabilities.

## Installation

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package and project manager (will automatically install Python 3.12+ if needed)

### Setup

1. **Clone the repository**
  ```sh
   git clone https://github.com/ECMWFCode4Earth/EarthReach.git
   cd EarthReach
  ```
2. **Create a virtual environment and install dependencies**
  ```sh
  uv sync --group dev
  ```
This command will automatically:
- Create a .venv virtual environment
- Install all project dependencies from pyproject.toml
- Install development dependencies

3. **Activate the virtual environment**
  ```sh
  source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
  ```

4. **Set up pre-commit hooks (recommended for development)**
  ```sh
  uv run pre-commit install
  ```

You're now ready to use the project.

## Project Structure

```sh
.
├── docs/                     # Project documentation
├── notebooks/                # Tutorials & experiments
├── src/
│   ├── earth_reach/    # Main package
│   └── tests/                # Unit and integration tests (to come)
├── vllm/                     # VLLM inference server setup
├── pyproject.toml            # Project dependencies and metadata
└── uv.lock                   # Locked dependency versions
```

## VLLM Inference Server

To run this project, you will need to have an openAI-compatible LLM inference server.

We provide instructions on how to setup your own secured inference server using [VLLM](./vllm/setup.md).

## Usage

The project provides a command-line interface (CLI) accessible through `earth-reach-agent` or its shorter alias `era`.

### Available Commands

View all commands and options:
```sh
uv run era --help
```

### Generate weather chart descriptions

Generate a natural language description from a weather chart image:
```sh
uv run era generate --image-path <path_to_image>
```

### Evaluate descriptions

Evaluate the accuracy of a description against a weather chart:

```sh
uv run era evaluate --image-path <path_to_image> --description "<description_string>"
```

## Development

### Development Tooling

This project uses the following development tools:

- **Ruff**: Fast Python linter and formatter
- **Pre-commit**: Git hooks for code quality checks
- **Pytest**: Testing framework

### Code Quality

The project is configured with pre-commit hooks that run automatically before each commit to ensure code quality:

- **Ruff linting**: Checks for common Python issues and enforces coding standards
- **Ruff formatting**: Automatically formats code for consistency
- **Basic checks**: Trailing whitespace, file endings, YAML/TOML syntax, merge conflicts

### Running Tools Manually

You can run the development tools manually:

```sh
# Run ruff linter
uv run ruff check .

# Run ruff formatter
uv run ruff format .

# Run pre-commit hooks on all files
pre-commit run --all-files
```

### Configuration

- Ruff configuration is in `pyproject.toml` under `[tool.ruff]`
- Pre-commit configuration is in `.pre-commit-config.yaml`

## License

See [LICENSE](LICENSE)

## Copyright

© 2025 ECMWFCode4Earth. All rights reserved.
