Usage
=====

EarthReach provides a command-line interface for generating and evaluating weather chart descriptions.

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
