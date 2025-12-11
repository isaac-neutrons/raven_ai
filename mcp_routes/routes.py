from fastmcp import FastMCP

async def register_mcp_handlers(fastmcp: FastMCP):
    @fastmcp.tool
    async def on_handshake(packet, client):
            print("Handshake packet received:", packet)
            return {"status": "ok"}

    @fastmcp.tool
    async def on_chat_message(packet, client):
        print(f"[MCP] {client.username} says: {packet.data['message']}")

    @fastmcp.tool
    async def mcp_echo(message: str) -> str:
        return f"[MCP] Echo: {message}"