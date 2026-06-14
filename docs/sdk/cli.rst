CLI
===

The package ships with a command-line entry point named ``gitcode-api`` and also
supports module invocation via ``python -m gitcode_api``.

The CLI mirrors the synchronous ``GitCode`` client surface:

.. code-block:: text

   gitcode-api <resource> <method> [options]

For example, ``client.repos.get()`` becomes ``gitcode-api repos get ...`` and
``client.pulls.list()`` becomes ``gitcode-api pulls list ...``.

Running ``gitcode-api`` with **no arguments** prints a short banner (version line
and ASCII art when stdout is a TTY) followed by the same top-level help as
``gitcode-api -h``.

Installation
------------

Install the package from PyPI:

.. code-block:: bash

   pip install -U gitcode-api

Or install the local project in editable mode while developing:

.. code-block:: bash

   pip install -e .

Authentication and connection options
---------------------------------------

Pass ``--api-key`` directly or set ``GITCODE_ACCESS_TOKEN`` in your environment.
Most leaf commands share ``--base-url``, ``--timeout``, ``--output-file``,
``--compact``, and ``-e`` / ``--escape`` (see :ref:`cli-escaping`).

The CLI does **not** expose the Python client's ``decrypt`` or custom
``http_client`` hooks. If you store an encrypted token or need a bespoke
``httpx`` client, use :class:`~gitcode_api.GitCode` in code instead (see
:doc:`index` authentication examples).

.. code-block:: bash

   export GITCODE_ACCESS_TOKEN="your-token"

.. code-block:: bash

   gitcode-api repos get --owner SushiNinja --repo GitCode-API

If a command calls a repository-scoped method and no ``owner`` / ``repo`` is
available from the command line, the SDK raises ``GitCodeConfigurationError``.

Bundled MCP server (``serve``)
------------------------------

With the ``[mcp]`` extra installed (**Python 3.10+**), ``gitcode-api serve``
starts the bundled FastMCP server (same tool as :doc:`llm_tools`).

* ``--transport`` — ``stdio``, ``http``, or ``sse`` (default ``stdio``).
* ``--show-banner`` — ``true`` or ``false`` to show or hide the FastMCP startup
  banner; omit the flag to use FastMCP’s default.
* ``--owner`` / ``--repo`` — optional defaults for repository-scoped tool calls.

.. code-block:: bash

   gitcode-api serve --api-key "$GITCODE_ACCESS_TOKEN"

Discovering commands
--------------------

Use ``-h`` / ``--help`` at any level to inspect available resource groups, methods, and flags:

.. code-block:: bash

   gitcode-api --help
   gitcode-api repos --help
   gitcode-api pulls create --help

Resource help lists subcommand names in the **same order** as
``resource.methods`` on the sync client. Each method's help opens with a
signature line matching ``resource.method_signature("<name>")`` in Python, then
the docstring summary—so the CLI stays aligned with runtime introspection on
:class:`~gitcode_api.GitCode`.

Print the installed package version:

.. code-block:: bash

   gitcode-api --version

Basic examples
--------------

Get repository metadata:

.. code-block:: bash

   gitcode-api repos get \
       --api-key "$GITCODE_ACCESS_TOKEN" \
       --owner SushiNinja \
       --repo GitCode-API

List open pull requests:

.. code-block:: bash

   gitcode-api pulls list \
       --owner SushiNinja \
       --repo GitCode-API \
       --state open \
       --per-page 20

Search repositories:

.. code-block:: bash

   gitcode-api search repositories \
       --q sdk

Build an OAuth authorization URL:

.. code-block:: bash

   gitcode-api oauth build-authorize-url \
       --client-id client-id \
       --redirect-uri https://example.com/callback \
       --scope user_info \
       --state opaque-state

Passing extra keyword arguments
-------------------------------

Some SDK methods accept ``**payload`` so the CLI cannot know
every supported flag ahead of time. For those methods, pass repeated
``--set key=value`` pairs or a JSON object with ``--set-json``.

.. code-block:: bash

   gitcode-api pulls list \
       --owner SushiNinja \
       --repo GitCode-API \
       --set only_count=true \
       --set reviewer=octocat

.. code-block:: bash

   gitcode-api repos update \
       --owner SushiNinja \
       --repo GitCode-API \
       --set-json '{"description": "Updated from CLI", "has_wiki": false}'

If the JSON payload is easier to keep in a file, prefix the path with ``@``:

.. code-block:: bash

   gitcode-api repos update \
       --owner SushiNinja \
       --repo GitCode-API \
       --set-json @payload.json

Output handling
---------------

Most commands print JSON to stdout. Use ``--compact`` for single-line JSON, or
``--output-file`` to write the response to disk.

.. code-block:: bash

   gitcode-api search repositories --q sdk --compact

Raw-byte responses such as ``contents get-raw`` can also be written directly to
a file:

.. code-block:: bash

   gitcode-api contents get-raw \
       --owner SushiNinja \
       --repo GitCode-API \
       --path README.md \
       --output-file README.downloaded.md

.. _cli-escaping:

Escaping and multi-line input
-----------------------------

When using string arguments with escape sequences (such as a line break as
``\n``), your shell may leave the backslashes as literal characters instead of
turning them into the intended character. Pass ``-e`` / ``--escape`` with the
sequences you want un-escaped—for example ``-e '\n\t'``. Those tokens are
substituted into other string arguments and into string elements of list
arguments. The escape flag itself, ``resource``, ``method``, ``api_key``, and
``base_url`` are not rewritten. If ``--escape`` is set but contains no valid
tokens, argument parsing fails.

.. code-block:: bash

   gitcode-api pulls create ... --body 'Line1\nLine2' -e '\n'

Module invocation
-----------------

If you prefer not to rely on the installed console script, use the module entry
point:

.. code-block:: bash

   python -m gitcode_api users me --api-key "$GITCODE_ACCESS_TOKEN"
