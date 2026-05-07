LLM tools: OpenAI, MCP, and openJiuwen
======================================

.. versionadded:: 1.2.5

The ``gitcode_api.llm`` package bundles optional adapters so agents can call the
same resource-oriented API as :class:`~gitcode_api.GitCode` and
:class:`~gitcode_api.AsyncGitCode`, without duplicating endpoint logic.

Heavy dependencies (for example FastMCP or the `openJiuwen <https://openjiuwen.com>`__
Python package) load **lazily** when you import symbols from ``gitcode_api.llm``;
only the symbols you use trigger their submodule imports.

Logical tool: ``gitcode_api_tool``
----------------------------------

All adapters expose one logical function tool named ``gitcode_api_tool``.
Model-facing arguments follow the JSON Schema used by OpenAI-style function
calling:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Parameter
     - Role
   * - ``op_type`` (required)
     - Resource group on the client (same names as attributes on
       :class:`~gitcode_api.GitCode`, for example ``repos``, ``pulls``,
       ``issues``).
   * - ``action``
     - Method on that resource (for example ``get``, ``list``). When empty and
       combined with ``help``, returns discovery text instead of a normal call.
   * - ``params``
     - Keyword arguments for the method as a JSON object; omitted or ``null``
       is treated as ``{}``.
   * - ``help``
     - When ``true``, returns formatted help (available methods or a target
       signature) instead of performing a request where applicable.

Successful values are JSON-friendly (``APIObject.to_dict()``, base64-wrapped
``bytes``, and similar). Failures are objects with ``"error": true`` and a
``"message"`` string; HTTP and configuration errors may include extra fields.

OpenAI Chat Completions tool
----------------------------

:class:`~gitcode_api.llm.openai.GitCodeOpenAITool` ships with the **core** package (no
MCP extra). It wraps :class:`~gitcode_api.llm._tool.GitCodeLLMTool` with:

* ``.tool`` / :meth:`~gitcode_api.llm.openai.GitCodeOpenAITool.to_dict` — payload in
  OpenAI Chat Completions ``tools`` shape (``type: function``, name
  ``gitcode_api_tool``, shared schema).
* Callable invocation with ``(op_type, action, params=..., help=...)`` in sync
  mode, or ``async_mode=True`` for the async path.

.. code-block:: python

   from gitcode_api.llm import GitCodeOpenAITool

   tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API")
   tools_payload = [tool.tool]

   result = tool("repos", "get", params={})

   async_tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API", async_mode=True)
   # await async_tool("pulls", "list", params={"state": "open", "per_page": 5})

You can pass the emitted tool definition straight into an OpenAI client and
handle tool calls directly:

.. code-block:: python

  import json
  import os
  from typing import Dict, List

  from openai import OpenAI

  from gitcode_api.llm import GitCodeOpenAITool

  MESSAGE_SEP = "\n" + "=" * 60 + "\n"
  USER_QUERY = "List the repos owned by SushiNinja."
  CONVERSATION: List[Dict[str, str]] = [dict(role="user", content=USER_QUERY)]

  tools = {"gitcode_api_tool": GitCodeOpenAITool()}
  client = OpenAI()

  print("U:\n" + USER_QUERY + MESSAGE_SEP)
  while True:
      response = (
          client.chat.completions.create(
              model="gpt-5.4-nano",
              messages=CONVERSATION,
              tools=[tools["gitcode_api_tool"].tool],
          )
          .choices[0]
          .message
      )
      CONVERSATION.append(response.to_dict())
      print("A:\n" + (response.content or ""))
      for tool_call in response.tool_calls or []:
          selected_tool = tools[tool_call.function.name]
          result = selected_tool(**json.loads(tool_call.function.arguments))
          CONVERSATION.append(dict(role="tool", tool_call_id=tool_call.id, content=result))
          print(f"<Calling tool {tool_call.function.name}({tool_call.function.arguments})>")
      print(MESSAGE_SEP)
      if not response.tool_calls:
          break

Constructor arguments mirror the clients: ``client=``, ``async_client=``,
``api_key=``, ``owner=``, ``repo=``, ``base_url=``, ``timeout=``, ``decrypt=``.
For dict-driven setups that reserve the name ``async``, you may pass
``**{"async": True}`` instead of ``async_mode=True`` (but not both).

Shared tool instance
--------------------

To reuse authentication or HTTP clients across several integrations, construct
:class:`~gitcode_api.llm._tool.GitCodeLLMTool` once and pass it as ``tool=`` into
:class:`~gitcode_api.llm.mcp.GitCodeMCP`, :func:`~gitcode_api.llm.mcp.create_mcp_server`,
:func:`~gitcode_api.llm.mcp.register_mcp_gitcode_api_tool`, or
:func:`~gitcode_api.llm.mcp.create_mcp_gitcode_api_tool`.

.. code-block:: python

   from gitcode_api.llm._tool import GitCodeLLMTool

   shared = GitCodeLLMTool(owner="SushiNinja", repo="GitCode-API")

The ``gitcode_api.llm._tool`` module is internal-facing but stable for this
``tool=`` sharing pattern (also described in the project README).

MCP (FastMCP)
-------------

`Model Context Protocol <https://modelcontextprotocol.io>`__ integration uses
`FastMCP <https://github.com/jlowin/fastmcp>`__. Install the optional extra
(**Python 3.10+** is required because of the ``fastmcp`` dependency pin):

.. code-block:: bash

   pip install 'gitcode-api[mcp]'

Public helpers (see module reference below):

* :func:`~gitcode_api.llm.mcp.create_mcp_server` — returns a ``FastMCP`` instance with
  ``gitcode_api_tool`` already registered; ``name=``, ``tool=``, and other
  keyword arguments are forwarded to ``FastMCP(...)``. Unless you pass
  ``instructions=``, the server receives default MCP server instructions that
  summarize the tool, parameters, base64-wrapped bytes, and the valid ``op_type``
  names for the installed SDK.
* :class:`~gitcode_api.llm.mcp.GitCodeMCP` — constructs that server and registers
  the tool; unknown attributes are delegated to the underlying ``FastMCP``
  object (for example transport helpers for your installed FastMCP version).
  It also registers **MCP resources** for help messages (plain text / markdown,
  same content as ``gitcode_api_tool`` help where applicable):

  * ``gitcode-api://help`` — index of per-``op_type`` URIs.
  * ``gitcode-api://help/{op_type}`` — method list for one resource.

  Call :func:`~gitcode_api.llm.mcp.register_mcp_help_resources` if you attach
  the tool to your own ``FastMCP`` instance and want the same resources.
* :func:`~gitcode_api.llm.mcp.create_mcp_gitcode_api_tool` — standalone async
  callable used as the tool body for custom wiring.
* :func:`~gitcode_api.llm.mcp.register_mcp_gitcode_api_tool` — attaches that callable
  to an existing FastMCP-compatible server (``mcp.tool(...)`` or
  ``mcp.add_tool(...)`` depending on the API).

.. code-block:: python

   from gitcode_api.llm import create_mcp_server

   mcp = create_mcp_server(name="GitCode API", owner="SushiNinja", repo="GitCode-API")
   # Start the server using FastMCP’s API for your version (stdio, HTTP, etc.).

The same server is exposed from the CLI as ``gitcode-api serve``; see
:doc:`cli`.

openJiuwen ``LocalFunction``
----------------------------

`openJiuwen <https://openjiuwen.com>`__ is an open source agent platform. When the
separate ``openjiuwen`` distribution is installed (**Python 3.11+**),
:func:`~gitcode_api.llm.jiuwen.create_openjiuwen_gitcode_api_tool` wraps the
same :class:`~gitcode_api.llm._tool.GitCodeLLMTool` logic in an openJiuwen
``LocalFunction`` that exposes the standard ``op_type`` /
``action`` / ``params`` / ``help`` schema. The implementation is **async
only**: use ``await jiuwen_tool.invoke(...)`` (or your runtime’s equivalent) rather than
calling the underlying coroutine synchronously.

.. code-block:: bash

   pip install openjiuwen

.. code-block:: python

   from gitcode_api.llm import create_openjiuwen_gitcode_api_tool

   jiuwen_tool = create_openjiuwen_gitcode_api_tool(owner="SushiNinja", repo="GitCode-API")
   # jiuwen_tool.card.name, jiuwen_tool.card.description, jiuwen_tool.card.input_params — tool metadata
   # await jiuwen_tool.invoke({"op_type": "repos", "action": "get", "params": {}})

Constructor arguments mirror the clients: ``client=``, ``async_client=``,
``api_key=``, ``owner=``, ``repo=``, ``base_url=``, ``timeout=``, ``decrypt=``,
plus optional ``name=`` and ``description=`` for the tool card (defaults match
``gitcode_api_tool`` and the shared description).

Published GitHub Releases also ship a ``gitcode-<version>.mcpb`` bundle for
`Claude Desktop <https://claude.com/docs/connectors/building/mcpb>`__ extension
installs (local MCP via MCPB). A checkout can run ``make mcpb`` when the
official ``mcpb`` CLI is available.

Corporate TLS / custom ``httpx`` clients
----------------------------------------

If you need a custom CA or proxy settings, build :class:`~gitcode_api.GitCode` /
:class:`~gitcode_api.AsyncGitCode` with ``http_client=`` / ``async_client=`` and
pass those instances into ``GitCodeOpenAITool``, MCP helpers, or
:func:`~gitcode_api.llm.jiuwen.create_openjiuwen_gitcode_api_tool` via
``client=`` / ``async_client=``, or pass a preconfigured
:class:`~gitcode_api.llm._tool.GitCodeLLMTool` via ``tool=`` into the OpenAI /
MCP adapters, so tool calls reuse the same TLS stack as the rest of your app.

Further reading
---------------

* :doc:`index` — install, authentication, and client lifecycle.
* :doc:`reference` — autodoc for ``gitcode_api.llm`` and submodules.
