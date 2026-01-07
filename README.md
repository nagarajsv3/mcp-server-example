uv init

uv venv

uv add mcp[cli]

#Starts a MCP inspector and we can use it to connect to MCP Server

mcp dev src/weather.py

#run mcp server weather with claude

{
"mcpServers": {
"airbnb": {
"command": "npx",
"args": [
"-y",
"@openbnb/mcp-server-airbnb",
"--ignore-robots-txt"
]
},
"weather": {
"command": "uv",
"args": [
"--directory",
"C:\\Users\\bhata\\Pythonprojects\\hello-world-mcp",
"run",
"src\\weather.py"
]
}
}
}

#automatically add mcp server to claude config
mcp install src/weather.py


#Transport Streamable Http
https://github.com/modelcontextprotocol/python-sdk
1. Terminal 1 , Run Uvicorn server
   (hello-world-mcp) C:\Users\bhata\Pythonprojects\hello-world-mcp>uv run src\server_greet_streamablehttp.py
   INFO:     Started server process [3140]
   INFO:     Waiting for application startup.
   [12/29/25 20:04:40] INFO     StreamableHTTP session manager started                                                                                                            streamable_http_manager.py:115
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

2. In Terminal 2 , Run MCP Dev Inspector mcp dev src/server_greet_streamablehttp.py
   Starting MCP inspector...
   ⚙️ Proxy server listening on localhost:6277
   🔑 Session token: 14fd70ea79ade6fa5027154a714f64830663c236625245239386a8f49446119e
   Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🚀 MCP Inspector is up and running at:
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=14fd70ea79ade6fa5027154a714f64830663c236625245239386a8f49446119e

3. In the browser , http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=14fd70ea79ade6fa5027154a714f64830663c236625245239386a8f49446119e
Choose Transport type as Streamable Http
URL http://localhost:8000/mcp
Connect -> Tools -> Test



Reference :
https://platform.openai.com/docs/guides/retrieval
https://platform.openai.com/storage/files/file-8rnjAWTRmwWxbCb91mwp5w