## Getting Started

### Quick Install

Click one of the buttons below to install the MCP server in your preferred IDE:

[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D&quality=insiders)
[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)
[![Install in Goose](https://block.github.io/goose/img/extension-install-dark.svg)](https://block.github.io/goose/extension?cmd=uvx&arg=--from%2520gitcode-api%5Bmcp%5D%2520gitcode-api%2520serve&id=GitCode%20API&name=GitCode%20API&description=MCP%20Server%20for%20GitCode%20API)
[![Add MCP Server GitCode API to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)

### Manual Installation

> **Note:** This configuration includes secure password prompts. When you install the MCP server, you'll be prompted to enter the following:
> - **gitcode_access_token**: Enter GITCODE_ACCESS_TOKEN
>
> These values are stored securely and never hardcoded in your configuration.

**Standard config** works in most tools:

```js
{
  "servers": {
    "GitCode API": {
      "command": "uvx",
      "args": [
        "--from",
        "gitcode-api[mcp]",
        "gitcode-api",
        "serve"
      ],
      "env": {
        "GITCODE_ACCESS_TOKEN": "${input:gitcode_access_token}"
      }
    }
  }
}
```

Replace `${input:gitcode_access_token}` with your actual [GitCode access token](https://docs.gitcode.com/en/docs/help/home/user_center/security_management/user_pat/) and you can start using the service.

<details>
<summary>VS Code</summary>

#### Click the button to install:

[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&inputs=%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%7D)

#### Or install manually:

Follow the MCP install [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server), use the standard config above. You can also install the GitCode API MCP server using the VS Code CLI:

```bash
code --add-mcp '{\"name\":\"GitCode API\",\"command\":\"uvx\",\"args\":[\"--from\",\"gitcode-api[mcp]\",\"gitcode-api\",\"serve\"],\"env\":{\"GITCODE_ACCESS_TOKEN\":\"${input:gitcode_access_token}\"},\"inputs\":[{\"id\":\"gitcode_access_token\",\"type\":\"promptString\",\"description\":\"Enter GITCODE_ACCESS_TOKEN\",\"password\":true}]}'
```

After installation, the GitCode API MCP server will be available for use with your GitHub Copilot agent in VS Code.
</details>

<details>
<summary>VS Code Insiders</summary>

#### Click the button to install:

[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=GitCode%20API&inputs=%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%7D&quality=insiders)

#### Or install manually:

Follow the MCP install [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server), use the standard config above. You can also install the GitCode API MCP server using the VS Code Insiders CLI:

```bash
code-insiders --add-mcp '{\"name\":\"GitCode API\",\"command\":\"uvx\",\"args\":[\"--from\",\"gitcode-api[mcp]\",\"gitcode-api\",\"serve\"],\"env\":{\"GITCODE_ACCESS_TOKEN\":\"${input:gitcode_access_token}\"},\"inputs\":[{\"id\":\"gitcode_access_token\",\"type\":\"promptString\",\"description\":\"Enter GITCODE_ACCESS_TOKEN\",\"password\":true}]}'
```

After installation, the GitCode API MCP server will be available for use with your GitHub Copilot agent in VS Code Insiders.
</details>

<details>
<summary>Visual Studio</summary>

#### Click the button to install:

[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%7D)

#### Or install manually:

1. Open Visual Studio
2. Navigate to the GitHub Copilot Chat window
3. Click the tools icon (🛠️) in the chat toolbar
4. Click the + "Add Server" button to open the "Configure MCP server" dialog
5. Fill in the configuration:
   - **Server ID**: `GitCode API`
   - **Type**: Select `stdio` from the dropdown
   - **Command**: `uvx`
   - **Arguments**: `--from gitcode-api[mcp] gitcode-api serve`
   - **Environment Variables**: Configure as needed
   - **Note**: You'll be prompted for secure values during installation
6. Click "Save" to add the server

For detailed instructions, see the [Visual Studio MCP documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers).
</details>

<details>
<summary>Cursor</summary>

#### Click the button to install:

[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJuYW1lIjoiR2l0Q29kZSBBUEkiLCJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)

#### Or install manually:

Go to `Cursor Settings` -> `MCP` -> `Add new MCP Server`. Name to your liking, use `command` type with the command from the standard config above. You can also verify config or add command like arguments via clicking `Edit`.
</details>

<details>
<summary>Goose</summary>

#### Click the button to install:

[![Install in Goose](https://block.github.io/goose/img/extension-install-dark.svg)](https://block.github.io/goose/extension?cmd=uvx&arg=--from%2520gitcode-api%5Bmcp%5D%2520gitcode-api%2520serve&id=GitCode%20API&name=GitCode%20API&description=MCP%20Server%20for%20GitCode%20API)

#### Or install manually:

Go to `Advanced settings` -> `Extensions` -> `Add custom extension`. Name to your liking, use type `STDIO`, and set the `command` from the standard config above. Click "Add Extension".
</details>

<details>
<summary>LM Studio</summary>

#### Click the button to install:

[![Add MCP Server GitCode API to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=GitCode%20API&config=eyJuYW1lIjoiR2l0Q29kZSBBUEkiLCJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)

#### Or install manually:

Go to `Program` in the right sidebar -> `Install` -> `Edit mcp.json`. Use the standard config above.
</details>

<details>
<summary>Claude Code</summary>

Use the Claude Code CLI to add the GitCode API MCP server:

```bash
claude mcp add GitCode API uvx --from gitcode-api[mcp] gitcode-api serve
```
</details>

<details>
<summary>Claude Desktop</summary>

Follow the MCP install [guide](https://modelcontextprotocol.io/quickstart/user), use the standard config above.

Alternatively, download the **`gitcode-<version>.mcpb`** asset from the matching [GitHub Release](https://github.com/Trenza1ore/GitCode-API/releases) and install it in Claude Desktop (double-click, drag-and-drop, or **Settings → Extensions → Advanced settings → Install Extension…**). That format is Anthropic’s MCP bundle for local servers; see [Build a desktop extension with MCPB](https://claude.com/docs/connectors/building/mcpb).
</details>

<details>
<summary>Codex</summary>

Create or edit the configuration file `~/.codex/config.toml` and add:

```toml
[mcp_servers.GitCode API]
command = "uvx"
args = ["--from", "gitcode-api[mcp]", "gitcode-api", "serve"]
```

For more information, see the [Codex MCP documentation](https://github.com/openai/codex/blob/main/codex-rs/config.md#mcp_servers).
</details>

<details>
<summary>Gemini CLI</summary>

Follow the MCP install [guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md#configure-the-mcp-server-in-settingsjson), use the standard config above.
</details>

<details>
<summary>OpenCode</summary>

Follow the MCP Servers [documentation](https://opencode.ai/docs/mcp-servers/). For example in `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "GitCode API": {
      "type": "local",
      "command": [
        "uvx",
        "--from",
        "gitcode-api[mcp]",
        "gitcode-api",
        "serve"
      ],
      "enabled": true
    }
  }
}
```
</details>

<details>
<summary>GitHub Copilot Coding Agent</summary>

GitHub Copilot Coding Agent can use MCP servers to extend its capabilities. Use the configuration below specifically formatted for the Coding Agent:

```json
{
  "mcpServers": {
    "GitCode API": {
      "command": "uvx",
      "args": [
        "--from",
        "gitcode-api[mcp]",
        "gitcode-api",
        "serve"
      ],
      "env": {
        "GITCODE_ACCESS_TOKEN": "${input:gitcode_access_token}"
      },
      "type": "local",
      "tools": [
        "*"
      ]
    }
  }
}
```

Add this configuration to your repository settings under **Copilot > Coding agent**. The `"tools": ["*"]` setting enables all available tools from the MCP server.

For more information, see the [GitHub Copilot Coding Agent MCP documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp).
</details>

### Configuration Details

- **Server Name:** `GitCode API`
- **Type:** UVX Package
- **Package:** `gitcode-api`
- **From:** `gitcode-api[mcp]`

### Need Help?

For more information about the Model Context Protocol, visit [modelcontextprotocol.io](https://modelcontextprotocol.io).
