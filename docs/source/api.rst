API Reference
=============

This section provides detailed documentation of the EarthReach API.

Core Components
---------------

These are the main classes that implement the dual-LLM framework:

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

LLM Interface
~~~~~~~~~~~~~

.. autoclass:: earth_reach.core.llm.LLMInterface
   :members:
   :show-inheritance:

Data Extractors
---------------

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

.. automodule:: earth_reach.cli
   :members:
   :show-inheritance:

Utilities
---------

.. automodule:: earth_reach.core.utils
   :members:
   :show-inheritance:
