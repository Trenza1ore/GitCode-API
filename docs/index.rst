GitCode API documentation
=========================

.. rubric:: Python SDK and mirrored REST reference

This documentation combines two complementary resources: a **Python SDK** for
building applications against GitCode, and a **REST API reference** that
mirrors the public English help content so you can read endpoints alongside
client usage.


GitHub repository: https://github.com/Trenza1ore/GitCode-API

GitCode repository: https://gitcode.com/SushiNinja/GitCode-API

PyPI package page: https://pypi.org/project/gitcode-api

My personal website: https://hugohuang.com

.. note::

   The SDK is published on `PyPI <https://pypi.org/project/gitcode-api/>`__,
   developed on `GitHub <https://github.com/Trenza1ore/GitCode-API>`__, and
   mirrored on `GitCode <https://gitcode.com/SushiNinja/GitCode-API>`__. The
   REST pages are mirrored from GitCode’s official documentation.

   Coffee requests may trigger a small :doc:`hot beverage notice <coffee>`.

.. topic:: Python SDK
   :class: gc-doc-card

   The ``gitcode_api`` package on PyPI exposes synchronous and asynchronous
   ``httpx`` clients with resource-oriented entry points such as
   ``client.repos`` and ``client.pulls``.

   :doc:`Open the SDK documentation <sdk/index>`

.. topic:: REST API reference
   :class: gc-doc-card

   Request paths, parameters, and response shapes are documented here in
   parallel with the `GitCode Help Docs <https://docs.gitcode.com/en/docs/>`__
   English site.

   :doc:`Open the REST API reference <rest_api/index>`

.. toctree::
   :maxdepth: 2
   :caption: Browse documentation

   General index <genindex>
   sdk/index
   rest_api/index

----

.. rubric:: Indices

The :ref:`genindex` lists documented names in alphabetical order.
