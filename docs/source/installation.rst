Installation
============

Prerequisites
-------------

- `uv <https://docs.astral.sh/uv/>`: Python package and project manager (will automatically install Python 3.12+ if needed)
- API key for a supported LLM provider (OpenAI, Google Gemini, Anthropic Claude, or Groq)

Dependencies
-----

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/ECMWFCode4Earth/EarthReach.git
      cd EarthReach

2. **Create a virtual environment and install dependencies**

   .. code-block:: bash

      uv sync

   This command will automatically:

   - Create a .venv virtual environment
   - Install all project dependencies from pyproject.toml

3. **Activate the virtual environment**

   .. code-block:: bash

      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

LLM Provider Configuration
--------------------------

EarthReach requires an external LLM provider to function. The system supports multiple providers in a bring-your-own-key fashion. Set the appropriate environment variable for your chosen provider:

**OpenAI**

.. code-block:: bash

   export OPENAI_API_KEY="your-openai-api-key"

**Google Gemini**

.. code-block:: bash

   export GEMINI_API_KEY="your-gemini-api-key"

**Anthropic Claude**

.. code-block:: bash

   export ANTHROPIC_API_KEY="your-claude-api-key"

**Groq**

.. code-block:: bash

   export GROQ_API_KEY="your-groq-api-key"

.. note::
   You only need to configure one provider.

Self-hosted LLM Server (Advanced)
----------------------------------

For users who prefer to host their own LLM inference server, EarthReach can work with any OpenAI-compatible API endpoint. An example setup using VLLM on Rocky Linux/RHEL is available in the ``vllm/`` directory of this repository.

.. warning::
   Setting up a self-hosted inference server requires advanced system administration knowledge and significant computational resources. This approach is recommended only for users with experience in server deployment and GPU management.
