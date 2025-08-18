EarthReach documentation
========================

|License: Apache 2.0|

.. |License: Apache 2.0| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2-0


EarthReach is a Python library for generating natural language descriptions of meteorological data visualizations. The library extends **earthkit-plots** by providing automated text generation capabilities for weather charts, enabling programmatic conversion of visual data representations into structured textual descriptions.

The system implements a dual-LLM architecture consisting of a generator agent and an evaluator agent. The generator creates initial descriptions from chart images and associated GRIB file metadata, while the evaluator assesses output quality across multiple criteria including scientific accuracy, coherence, and meteorological relevance. This iterative process continues until quality thresholds are met or maximum iterations are reached.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
