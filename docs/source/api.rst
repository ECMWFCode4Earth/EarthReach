API Reference
=============

This section provides detailed documentation of the EarthReach API.

Core Components
---------------

The dual-LLM framework comprises three main components:
- The GeneratorAgent: creating weather chart descriptions
- The EvaluatorAgent: evaluating the generated chart descriptions
- The Orchestrator: driving the successive interactions between the generator and evaluator

GeneratorAgent
~~~~~~~~~~~~~~

.. autoclass:: earth_reach.core.generator.GeneratorAgent
   :members:
   :show-inheritance:

.. autoclass:: earth_reach.core.generator.GeneratorOutput
   :members:
   :show-inheritance:

EvaluatorAgent
~~~~~~~~~~~~~~

.. autoclass:: earth_reach.core.evaluator.EvaluatorAgent
   :members:
   :show-inheritance:

.. autoclass:: earth_reach.core.evaluator.CriterionEvaluatorOutput
   :members:
   :show-inheritance:

Orchestrator
~~~~~~~~~~~~

.. autoclass:: earth_reach.core.orchestrator.Orchestrator
   :members:
   :show-inheritance:

Data Extractors
---------------

Data extractors analyze GRIB file metadata to extract relevant meteorological information, which is then used to enhance prompts for both the generator and evaluator agents.

Base Extractor
~~~~~~~~~~~~~~

.. automodule:: earth_reach.core.extractors.base_extractor
   :members:
   :show-inheritance:

Temperature Extractor
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: earth_reach.core.extractors.temperature_extractor
   :members:
   :show-inheritance:

Pressure Extractor
~~~~~~~~~~~~~~~~~~

.. automodule:: earth_reach.core.extractors.pressure_extractor
   :members:
   :show-inheritance:

Configuration
-------------

LLM Interface
~~~~~~~~~~~~~

.. autoclass:: earth_reach.core.llm.LLMInterface
   :members:
   :show-inheritance:

Evaluation Criteria
~~~~~~~~~~~~~~~~~~~

.. automodule:: earth_reach.config.criteria
   :members:
   :show-inheritance:

Logging Configuration
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: earth_reach.config.logging
   :members:
   :show-inheritance:

Command Line Interface
----------------------

The CLI provides convenient access to EarthReach's core functionality through command-line commands. However, as it operates solely on image files without access to underlying GRIB metadata, the CLI generates less detailed descriptions compared to the full *earthkit-plots* library integration.

.. automodule:: earth_reach.cli
   :members:
   :show-inheritance:

Utilities
---------

.. automodule:: earth_reach.core.utils
   :members:
   :show-inheritance:
