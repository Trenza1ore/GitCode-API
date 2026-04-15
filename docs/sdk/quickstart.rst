Quickstart
==========

This page documents the implemented ``gitcode_api`` SDK surface rather than the
upstream raw REST endpoints.

Create a sync client
--------------------

.. code-block:: python

   from gitcode_api import GitCode

   client = GitCode(
       api_key="your-token",
       owner="SushiNinja",
       repo="GitCode-API",
   )

   try:
       repo = client.repos.get()
       print(repo.full_name)
   finally:
       client.close()

Create an async client
----------------------

.. code-block:: python

   import asyncio

   from gitcode_api import AsyncGitCode


   async def main() -> None:
       client = AsyncGitCode(owner="SushiNinja", repo="GitCode-API")
       try:
           pulls = await client.pulls.list(state="open", per_page=20)
           print(len(pulls))
       finally:
           await client.close()


   asyncio.run(main())

Repository-scoped defaults
--------------------------

Most repository resources accept ``owner=`` and ``repo=`` per call. If you set
them on the client, repository methods can omit them:

.. code-block:: python

   client = GitCode(owner="SushiNinja", repo="GitCode-API")

   branches = client.branches.list(per_page=10)
   commits = client.commits.list(sha="main", per_page=10)
   pulls = client.pulls.list(state="open")

If ``owner`` and ``repo`` are missing for a repository-scoped call, the SDK
raises ``GitCodeConfigurationError``.

Working with response objects
-----------------------------

Responses are wrapped in lightweight ``APIObject`` subclasses. Use attribute
access for common fields or ``.get()`` when a field may be missing.

.. code-block:: python

   pull = client.pulls.get(number=42)
   print(pull.title)
   print(pull.get("source_branch"))

   payload = pull.to_dict()

Common workflows
----------------

Create a pull request:

.. code-block:: python

   pull = client.pulls.create(
       title="Add feature",
       head="feature-branch",
       base="main",
       body="Implements the new flow.",
   )

Create or update repository content:

.. code-block:: python

   result = client.contents.create(
       path="README.md",
       content="IyBIZWxsbyBHaXRDb2RlCg==",
       message="Add README",
       branch="main",
   )

Search across GitCode:

.. code-block:: python

   repos = client.search.repositories(q="sdk language:python", per_page=10)
   users = client.search.users(q="SushiNinja")

OAuth helper methods
--------------------

The ``oauth`` resource includes helper methods for the authorization code flow.

.. code-block:: python

   authorize_url = client.oauth.build_authorize_url(
       client_id="client-id",
       redirect_uri="https://example.com/callback",
       scope="user_info",
       state="opaque-state",
   )

   token = client.oauth.exchange_token(
       code="returned-code",
       client_id="client-id",
       client_secret="client-secret",
   )

Examples
--------

The repository includes runnable examples under ``examples/`` for:

- current user lookup
- repository overview
- pull request listing
- asynchronous branch listing
