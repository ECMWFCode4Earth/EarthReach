# EarthReach Agent: Dual-LLM Framework for Validated Meteorological Chart Descriptions

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3120/">
    <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  </a>
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

- [uv](https://docs.astral.sh/uv/): Python package and project manager (will automatically install Python 3.12+ if needed)
- [Climate Data Store ](https://cds.climate.copernicus.eu/how-to-api): API key configured for accessing meteorological data
- API key for a supported LLM provider (OpenAI, Google Gemini, Anthropic Claude, Groq, or any OpenAI-compatible API provider)

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

## Basic Usage

```python
from earth_reach import EarthReachAgent
import earthkit.plots as ekp
import earthkit.data as ekd

# Load your data with earthkit-data
data = ekd.from_source("file", "your_data.grib")

# Create a weather chart with earthkit-plots
figure = ekp.quickplot(data, mode="overlay")

# Generate description
agent = EarthReachAgent(provider="openai")
description = agent.generate_alt_description(figure, data)
print(description)
```

See `notebooks/example.ipynb` for a practical usage example.

## CLI Interface

EarthReach includes a standalone CLI that works on image files only, producing less detailed descriptions than the full library integration.

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
## VLLM Inference Server

EarthReach supports any OpenAI-compatible API endpoint for self-hosted LLMs. See `vllm/` directory for a VLLM setup example.

**Warning**: Self-hosting requires advanced system administration skills and significant GPU resources. Recommended only for experienced users.

## Development

### Development Tooling

This project uses the following development tools:

- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checker for Python
- **Pre-commit**: Git hooks for code quality checks
- **Pytest**: Testing framework

### Code Quality

The project is configured with pre-commit hooks that run automatically before each commit to ensure code quality:

- **Ruff linting**: Checks for common Python issues and enforces coding standards
- **Ruff formatting**: Automatically formats code for consistency
- **mypy type checking**: Validates type hints and catches import errors
- **Basic checks**: Trailing whitespace, file endings, YAML/TOML syntax, merge conflicts

### Running Tools Manually

You can run the development tools manually:

```sh
# Run ruff linter
uv run ruff check .

# Run ruff formatter
uv run ruff format .

# Run mypy type checker
uv run mypy .

# Run pre-commit hooks on all files
uv run pre-commit run --all-files
```

### Configuration

- Ruff configuration is in `pyproject.toml` under `[tool.ruff]`
- mypy configuration is in `pyproject.toml` under `[tool.mypy]`
- Pre-commit configuration is in `.pre-commit-config.yaml`

## License

See [LICENSE](LICENSE)

## Copyright

© 2025 ECMWFCode4Earth. All rights reserved.
