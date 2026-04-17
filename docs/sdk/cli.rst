CLI
===

The package ships with a command-line entry point named ``gitcode-api`` and also
supports module invocation via ``python -m gitcode_api``.

The CLI mirrors the synchronous ``GitCode`` client surface:

.. code-block:: text

   gitcode-api <resource> <method> [options]

For example, ``client.repos.get()`` becomes ``gitcode-api repos get ...`` and
``client.pulls.list()`` becomes ``gitcode-api pulls list ...``.

Installation
------------

Install the package from PyPI:

.. code-block:: bash

   pip install -U gitcode-api

Or install the local project in editable mode while developing:

.. code-block:: bash

   pip install -e .

Authentication and shared options
---------------------------------

Pass ``--api-key`` directly or set ``GITCODE_ACCESS_TOKEN`` in your environment.
The CLI also accepts shared client options such as ``--owner``, ``--repo``,
``--base-url``, and ``--timeout``.

.. code-block:: bash

   export GITCODE_ACCESS_TOKEN="your-token"

.. code-block:: bash

   gitcode-api repos get --owner SushiNinja --repo GitCode-API

If a command calls a repository-scoped method and no ``owner`` / ``repo`` is
available from the command line, the SDK raises ``GitCodeConfigurationError``.

Discovering commands
--------------------

Use ``--help`` at any level to inspect available resources, methods, and flags:

.. code-block:: bash

   gitcode-api --help
   gitcode-api repos --help
   gitcode-api pulls create --help

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

Some SDK methods accept ``**params`` or ``**payload`` so the CLI cannot know
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

Module invocation
-----------------

If you prefer not to rely on the installed console script, use the module entry
point:

.. code-block:: bash

   python -m gitcode_api users me --api-key "$GITCODE_ACCESS_TOKEN"
