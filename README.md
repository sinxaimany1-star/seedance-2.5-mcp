# Seedance 2.5 MCP Server

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![MCP compatible](https://img.shields.io/badge/MCP-compatible-green?style=flat-square)](https://modelcontextprotocol.io)

A focused [Model Context Protocol](https://modelcontextprotocol.io) server for generating Seedance 2.5 Preview videos through [MuAPI](https://muapi.ai). It exposes the standard Seedance 2.5 workflows with explicit 720p/480p selection, rather than making an assistant search through a large general-purpose model catalog.

The implementation is informed by [SamurAIGPT/muapi-mcp-server](https://github.com/SamurAIGPT/muapi-mcp-server): it forwards a MuAPI key, keeps generation asynchronous, and provides both an MCP stdio transport and a small HTTP bridge.

## Included tools

| Tool | Purpose |
| --- | --- |
| `seedance_25_text_to_video` | Text-to-video generation at 720p or 480p |
| `seedance_25_image_to_video` | Animate one input image at 720p or 480p |
| `seedance_25_first_last_frame` | Transition between exactly two frame images |
| `seedance_25_omni_reference` | Combine image, video, and audio references |
| `muapi_predict_result` | Poll a MuAPI prediction by `request_id` |
| `muapi_account_balance` | Read the MuAPI credit balance |

Generation tools return the completed prediction when used over stdio. The HTTP bridge returns a local request ID immediately and exposes the result at `/mcp/predictions/{request_id}` or as server-sent events.

## Quick start

```bash
git clone https://github.com/Anil-matcha/seedance-2.5-mcp.git
cd seedance-2.5-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MUAPI_API_KEY=your_muapi_key_here
```

Run the standards-based stdio server for an MCP client:

```bash
python mcp_stdio.py
```

Run the local HTTP bridge instead:

```bash
python mcp_server.py
# http://localhost:8000/docs
```

`MUAPIAPP_API_KEY` is accepted as a backwards-compatible alternative. `MUAPI_BASE_URL`, `MUAPI_HTTP_TIMEOUT`, `MUAPI_POLL_INTERVAL`, and `MUAPI_POLL_TIMEOUT` can be used for local testing or a compatible MuAPI deployment.

## Claude Code

With `MUAPI_API_KEY` exported in the shell used by Claude Code:

```bash
claude mcp add seedance-2.5 -- python /absolute/path/to/seedance-2.5-mcp/mcp_stdio.py
```

## Cursor, Windsurf, and Claude Desktop

Copy the `mcp.json` entry and replace the placeholder path. Keep the API key in the client environment; do not commit it.

```json
{
  "mcpServers": {
    "seedance-2.5": {
      "command": "python",
      "args": ["/absolute/path/to/seedance-2.5-mcp/mcp_stdio.py"],
      "env": {
        "MUAPI_API_KEY": "${MUAPI_API_KEY}"
      }
    }
  }
}
```

## HTTP bridge

The HTTP process is useful for local integrations that need a simple request/poll surface:

```bash
curl http://localhost:8000/mcp/tools

curl -X POST http://localhost:8000/mcp/tools/seedance_25_text_to_video/call \
  -H "Authorization: Bearer $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "prompt": "A red paper boat drifting through a sunlit forest stream, cinematic camera movement",
      "duration": 5,
      "aspect_ratio": "16:9",
      "resolution": "720p"
    }
  }'
```

Poll the returned local ID:

```bash
curl http://localhost:8000/mcp/predictions/REQUEST_ID
curl -N http://localhost:8000/mcp/predictions/REQUEST_ID/stream
```

The bridge allowlists all upstream paths and never accepts an arbitrary endpoint URL. Generation and polling consume MuAPI credits according to the selected resolution and workflow.

## Model notes

Seedance 2.5 Preview supports clips from 4 to 30 seconds. The standard routes support 720p and the dedicated `480p` routes are intended for faster, lower-cost previews. The first/last-frame tool requires exactly two images. Omni reference accepts up to 20 images, 6 video clips, and 6 audio files.

## Docker

```bash
docker build -t seedance-2-5-mcp .
docker run --rm -p 8000:8000 -e MUAPI_API_KEY="$MUAPI_API_KEY" seedance-2-5-mcp
```

## Development

```bash
python -m unittest discover -s tests -v
python -m compileall -q server_core.py mcp_server.py mcp_stdio.py
```

## License

MIT. See [LICENSE](LICENSE).
