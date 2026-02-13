import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from .graph_builder import build_graph


async def run_agent(user_input: str):

    client = MultiServerMCPClient(
        {
            "m365": {
                "command": "uv",
                "args": [
                    "--directory",
                    "D:\\LLMOPS_Projects\\m365_assistant",
                    "run",
                    "python",
                    "-m",
                    "m365_assistant.main"
                ],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    graph = build_graph(tools)

    result = await graph.ainvoke({
    "user_input": user_input
    })


    return result["final_schedule"]


# 🔥 ADD THIS PART
if __name__ == "__main__":
    user_input = input("What would you like to plan today? \n> ")

    output = asyncio.run(run_agent(user_input))

    print("\n\n📅 Generated Daily Routine:\n")
    print(output)
