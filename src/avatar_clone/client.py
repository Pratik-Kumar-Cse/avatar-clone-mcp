import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Set server parameters
    server_params = StdioServerParameters(
        command="avatar-clone",  # Path to server.py
        args=[
            "--directory",
            "avatar-clone",
            "run",
            "avatar-clone",
        ],  # Command line arguments (if needed)
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            try:
                # Get list of available tools
                tools = await session.list_tools()
                print(f"Available tools: {tools}")

                # Example of calling a tool
                tool_result = await session.call_tool(
                    "clone_avatar",
                    arguments={
                        "name": "my",
                        "image": "http://example.com/image.jpg",
                        "platform": "heygen",
                    },
                )
                print(f"Tool execution result: {tool_result}")

            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Running")
    asyncio.run(main())
