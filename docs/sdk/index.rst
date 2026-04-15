GitCode Python SDK
==================

``gitcode_api`` provides synchronous and asynchronous ``httpx`` clients for the
GitCode REST API. The public entry points are ``GitCode`` and
``AsyncGitCode``.

.. toctree::
   :maxdepth: 2

   quickstart
   client_api
   reference

Highlights
----------

- OpenAI-style resource namespaces such as ``client.repos`` and
  ``client.pulls``.
- Shared repository context via ``owner=`` and ``repo=`` on the client.
- Lightweight response wrappers that expose JSON fields as attributes.
- Matching sync and async resource surfaces.

Install
-------

Install the package from PyPI:

.. code-block:: bash

   pip install gitcode-api

For local development, install the project and optional documentation
dependencies with ``uv``:

.. code-block:: bash

   uv sync
   uv sync --group docs

Authentication
--------------

Pass ``api_key=`` directly or set ``GITCODE_ACCESS_TOKEN`` in your environment.

.. code-block:: bash

   export GITCODE_ACCESS_TOKEN="your-token"

Client lifecycle
----------------

Both clients accept shared defaults for ``owner``, ``repo``, ``base_url``, and
``timeout``.

``GitCode`` manages a synchronous ``httpx.Client`` and supports ``close()``.
``AsyncGitCode`` manages an asynchronous ``httpx.AsyncClient`` and supports
``await close()``.

.. code-block:: python

   from gitcode_api import GitCode

   client = GitCode(owner="SushiNinja", repo="GitCode-API")
   try:
       repo = client.repos.get()
       print(repo.full_name)
   finally:
       client.close()

Available resources
-------------------

The SDK exposes these resource groups on both sync and async clients:

- ``repos`` and ``contents``
- ``branches`` and ``commits``
- ``issues`` and ``pulls``
- ``labels``, ``milestones``, and ``members``
- ``releases``, ``tags``, and ``webhooks``
- ``users``, ``orgs``, ``search``, and ``oauth``

Next steps
----------

- See :doc:`quickstart` for common usage patterns.
- See :doc:`client_api` for the client-oriented chained API reference.
- See :doc:`reference` for the autodoc-generated module reference.
