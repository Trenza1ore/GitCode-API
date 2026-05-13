GitCode API documentation
=========================

.. rubric:: Python SDK and mirrored REST reference

This documentation combines two complementary resources: a **Python SDK** for
building applications against GitCode, and a **REST API reference** that
mirrors the public English help content so you can read endpoints alongside
client usage.


Why this project
----------------

- **Community-maintained** Python SDK for the GitCode REST API: less
  boilerplate than spelling out raw ``httpx`` requests for each endpoint you
  use.
- **Synchronous and asynchronous** ``httpx`` clients with a matching API
  surface (``GitCode`` / ``AsyncGitCode``).
- **Resource-oriented** entry points (``client.repos``, ``client.pulls``,
  ``client.issues``, and others), with optional default ``owner=`` / ``repo=``
  on the client when you mostly work inside one repository.
- **Higher-level helpers** where they matter—for example issue and pull request
  :ref:`template discovery <sdk-client-api-templates>` on the issues and pulls
  resource groups.
- **Single documentation tree** Sphinx SDK reference sits beside a curated
  REST mirror: clarified, cross-linked, and corrected rather than treated as a
  bulk export of upstream help pages.
- **Optional agent integrations** OpenAI-style tools, MCP
  (FastMCP), and `openJiuwen <https://openjiuwen.com>`__ integration; see
  :doc:`sdk/llm_tools`.

Project links
-------------

- `Project homepage <https://hugohuang.com/gitcode-api>`__
- `GitHub (source and issues) <https://github.com/Trenza1ore/GitCode-API

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
   ``client.repos`` and ``client.pulls``. Optional :doc:`LLM tool adapters
   <sdk/llm_tools>` cover OpenAI-style function tools, MCP (FastMCP), and
   `openJiuwen <https://openjiuwen.com>`__ ``LocalFunction`` tools.

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

   sdk/index
   rest_api/index
   Changelog <changelog>

----

.. rubric:: Indices

The :ref:`genindex` lists documented names in alphabetical order.
