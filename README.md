# avatar-clone MCP server

A MCP server project

## Overview

The avatar-clone MCP server helps to clone avatars on platforms like Hegen, Tavus, or custom models for avatars.

## Components

### Resources

The server implements a simple note storage system with:

- Custom note:// URI scheme for accessing individual notes
- Each note resource has a name, description, and text/plain mimetype

### Prompts

The server provides a single prompt:

- summarize-notes: Creates summaries of all stored notes
  - Optional "style" argument to control detail level (brief/detailed)
  - Generates prompt combining all current notes with style preference

### Tools

The server implements one tool:

- add-note: Adds a new note to the server
  - Takes "name" and "content" as required string arguments
  - Updates server state and notifies clients of resource changes

## Configuration

[TODO: Add configuration details specific to your implementation]

## Quickstart

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Pratik-Kumar-Cse/avatar-clone-mcp.git
   cd avatar-clone-mcp
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate  # Windows
   ```

3. **Run the Server:**

   ```bash
   uv run avatar-clone
   ```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run _avatar-clone_.

### Using PIP

Alternatively, you can install `avatar-clone` via pip:

   ```bash
   pip install avatar-clone
   ```

After installation, you can run it as a script using:

   ```bash
   python -m avatar_clone
   ```

## Configuration

### Usage with Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

  ```json
  "mcpServers": {
    "avatar-clone": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/pratikkumar/Desktop/Projects/ciny/ciny-main/mcp-server/avatar-clone",
        "run",
        "avatar-clone"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>

  ```json
  "mcpServers": {
    "avatar-clone": {
      "command": "uvx",
      "args": [
        "avatar-clone"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:

   ```bash
   uv sync
   ```

2. Build package distributions:

   ```bash
   uv build
   ```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:

   ```bash
   uv publish
   ```

Note: You'll need to set PyPI credentials via environment variables or command flags:

- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
  <summary>Using uvx</summary>

  ```json
  "mcpServers": {
    "avatar-clone": {
      "command": "uvx",
      "args": ["avatar-clone", "--repository", "path/to/git/repo"]
    }
  }
  ```
</details>

<details>
  <summary>Using docker</summary>

  - Note: replace '/Users/username' with the path that you want to be accessible by this tool

  ```json
  "mcpServers": {
    "avatar-clone": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--mount", "type=bind,src=/Users/username,dst=/Users/username", "avatar-clone"]
    }
  }
  ```
</details>

<details>
  <summary>Using pip installation</summary>

  ```json
  "mcpServers": {
    "avatar-clone": {
      "command": "python",
      "args": ["-m", "avatar_clone", "--repository", "path/to/git/repo"]
    }
  }
  ```
</details>

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

<details>
  <summary>Using uvx</summary>

  ```json
  "context_servers": [
    "avatar-clone": {
      "command": {
        "path": "uvx",
        "args": ["avatar-clone"]
      }
    }
  ],
  ```
</details>

<details>
  <summary>Using pip installation</summary>

  ```json
  "context_servers": {
    "avatar-clone": {
      "command": {
        "path": "python",
        "args": ["-m", "avatar_clone"]
      }
    }
  },
  ```
</details>

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

   ```bash
   npx @modelcontextprotocol/inspector uv --directory /Users/pratikkumar/Desktop/Projects/ciny/ciny-main/mcp-server/avatar-clone run avatar-clone
   ```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

### Docker

   ```json
   {
     "mcpServers": {
       "avatar-clone": {
         "command": "docker",
         "args": [
           "run",
           "--rm",
           "-i",
           "--mount",
           "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
           "--mount",
           "type=bind,src=/path/to/other/allowed/dir,dst=/projects/other/allowed/dir,ro",
           "--mount",
           "type=bind,src=/path/to/file.txt,dst=/projects/path/to/file.txt",
           "avatar-clone"
         ]
       }
     }
   }
   ```

### UVX

   ```json
   {
     "mcpServers": {
       "avatar-clone": {
         "command": "uv",
         "args": [
           "--directory",
           "/<path to mcp-servers>/avatar-clone",
           "run",
           "avatar-clone"
         ]
       }
     }
   }
   ```

## Build

Docker build:

   ```bash
   docker build -t avatar-clone .
   ```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
