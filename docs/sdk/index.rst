GitCode Python SDK
==================

``gitcode_api`` provides synchronous and asynchronous ``httpx`` clients for the
GitCode REST API. The public entry points are ``GitCode`` and
``AsyncGitCode``.

.. toctree::
   :maxdepth: 2

   quickstart
   cli
   client_api
   llm_tools
   reference

Highlights
----------

- OpenAI-style resource groups such as ``client.repos`` and
  ``client.pulls``.
- Issue and pull request **template discovery** on ``client.issues`` and
  ``client.pulls``: :meth:`~gitcode_api.resources.collaboration.IssuesResource.list_templates`
  / :meth:`~gitcode_api.resources.collaboration.IssuesResource.get_template` (and the pull
  request counterparts) walk the GitCode ``.gitcode/`` tree on the default branch and resolve
  templates across the main repository, the owner's ``.gitcode`` repository, and fork-parent
  repositories (see :doc:`client_api`).
- Shared repository context via ``owner`` and ``repo`` on the client.
- Lightweight response wrappers that expose JSON fields as attributes.
- :func:`~gitcode_api.as_dict` for turning response models into plain
  dictionaries—one :class:`~gitcode_api._models.APIObject` becomes a ``dict``,
  a ``list`` of them becomes ``list[dict]``—in the same spirit as
  :func:`dataclasses.asdict` for structured objects (here backed by
  :meth:`~gitcode_api._models.APIObject.to_dict`), for example before JSON
  serialization.
- Matching sync and async resource surfaces.
- Optional :doc:`llm_tools` adapters: OpenAI Chat Completions tool shape, MCP
  server helpers (FastMCP), and `openJiuwen <https://openjiuwen.com>`__ ``LocalFunction``
  when ``openjiuwen`` is installed.
- Each resource group exposes a cached ``methods`` property (public
  callable names in stable SDK order) and ``method_signature(name)`` for a
  single method’s signature string, for runtime introspection.

Install
-------

Install the package from PyPI:

.. code-block:: bash

   pip install -U gitcode-api

For **MCP / FastMCP** helpers (Python **3.10+**), install the optional extra:

.. code-block:: bash

   pip install 'gitcode-api[mcp]'

For **openJiuwen** ``LocalFunction`` integration (see :doc:`llm_tools`), install
the upstream ``openjiuwen`` package separately (**Python 3.11+**):

.. code-block:: bash

   pip install openjiuwen

For local development, install the project and optional documentation
dependencies with ``uv``:

.. code-block:: bash

   uv sync
   uv sync --group docs

Authentication
--------------

Pass ``api_key`` directly or set ``GITCODE_ACCESS_TOKEN`` in your environment.
If either value is stored in encrypted form, pass ``decrypt`` so the client can
decode it before authenticating.

.. code-block:: bash

   export GITCODE_ACCESS_TOKEN="your-token"

.. code-block:: python

   from gitcode_api import GitCode
   from trusted_library import decrypt_token

   client = GitCode(api_key="encrypted-token", decrypt=decrypt_token)

Client lifecycle
----------------

Both clients accept shared defaults for ``owner``, ``repo``, ``base_url``, and
``timeout``.

``GitCode`` manages a synchronous ``httpx.Client`` and supports ``close()``.
``AsyncGitCode`` manages an asynchronous ``httpx.AsyncClient`` and supports
``await close()``.

Closing the SDK client also closes a supplied ``http_client`` instance.

.. code-block:: python

   from gitcode_api import GitCode

   client = GitCode(owner="SushiNinja", repo="GitCode-API")
   repo = client.repos.get()
   print(repo.full_name)

Available resource groups
-------------------------

The SDK exposes these resource groups on both sync and async clients:

- ``repos`` and ``contents``
- ``branches`` and ``commits``
- ``issues`` and ``pulls``
- ``labels``, ``milestones``, and ``members``
- ``releases``, ``tags``, and ``webhooks``
- ``users``, ``orgs``, ``search``, and ``oauth``

On any of the groups above, read ``client.<group>.methods`` for a stable tuple
of public method names (excluding private helpers and the ``methods`` /
``method_signature`` utilities). Order follows the SDK's segment-based sort key, not plain alphabetical
order on each full name. The value is built once per resource instance. Use
``client.<group>.method_signature("method_name")`` for parameters and return type of one callable.

Next steps
----------

- See :doc:`quickstart` for common usage patterns.
- See :doc:`cli` for the command-line entry point and examples.
- See :doc:`client_api` for the client-oriented chained API reference.
- See :doc:`llm_tools` for OpenAI tool definitions, MCP (FastMCP), and openJiuwen
  usage.
- See :doc:`reference` for the autodoc-generated module reference.
