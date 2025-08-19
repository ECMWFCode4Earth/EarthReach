Usage
=====

Library Integration
-------------------

The primary way to use EarthReach is through the ``EarthReachAgent`` class, designed for integration with earthkit-plots and other Python applications.

Basic Usage
~~~~~~~~~~~

.. code-block:: python

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

Input Requirements
~~~~~~~~~~~~~~~~~~

The ``generate_alt_description`` method requires:

- **figure**: An ``earthkit.plots.Figure`` object containing the weather chart
- **data**: An ``earthkit.data.FieldList`` containing GRIB meteorological data

**Required Variables**: The data must contain both:

- ``2t``: 2-meter temperature fields
- ``msl``: Mean sea level pressure fields

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

Customize the agent behavior with initialization parameters:

.. code-block:: python

   agent = EarthReachAgent(
       provider="openai",           # Required: LLM provider
       model_name="gpt-4",          # Optional: specific model (uses provider default)
       max_iterations=5,            # Maximum evaluation iterations (default: 3)
       criteria_threshold=3         # Minimum quality score to pass (default: 4)
   )

**Supported Providers**:

- ``"openai"``: OpenAI models (GPT-3.5, GPT-4, etc.)
- ``"gemini"``: Google Gemini models
- ``"anthropic"``: Anthropic Claude models
- ``"groq"``: Groq models

.. note::
   Ensure you have configured the API key for your chosen provider as an environment variable (e.g., ``OPENAI_API_KEY``, ``GEMINI_API_KEY``, etc.). See the :doc:`installation` section for details.

Command Line Interface
----------------------

EarthReach also provides a command-line interface for convenient standalone usage. However, as it operates solely on image files without access to underlying GRIB metadata, the CLI generates less detailed descriptions compared to the full earthkit-plots library integration.

Getting Started
---------------

The CLI is accessible through the ``era`` command (short for earth-reach-agent). View all available commands:

.. code-block:: bash

   uv run era --help

Generate Descriptions
---------------------

Generate a natural language description from a weather chart image:

.. code-block:: bash

   uv run era generate --image-path <path_to_image>

**Options:**

- ``--image-path``: Path to the weather chart image file
- ``--simple``: Use simple mode (generator only, no evaluation loop)
- ``--prompt-path``: Path to a custom prompt file (optional)

**Example:**

.. code-block:: bash

   uv run era generate --image-path ./charts/temperature_map.png

Evaluate Descriptions
---------------------

Evaluate the quality of a description against a weather chart:

.. code-block:: bash

   uv run era evaluate --image-path <path_to_image> --description "<description_string>"

**Options:**

- ``--image-path``: Path to the weather chart image file
- ``--description``: The description text to evaluate
- ``--prompt-path``: Path to a custom prompt file (optional)

**Example:**

.. code-block:: bash

   uv run era evaluate --image-path ./charts/temperature_map.png --description "Temperature ranges from 10C to 25C across the region"

Output Format
-------------

The CLI outputs structured information including:

- Generated descriptions with metadata
- Evaluation scores across multiple criteria (coherence, fluency, consistency, relevance)
- Processing time and iteration counts
- Quality metrics and feedback

Environment Variables
---------------------

Ensure you have configured the appropriate LLM provider as described in the :doc:`installation` section.
