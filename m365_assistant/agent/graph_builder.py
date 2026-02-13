from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentState
from .client import get_executor_llm, get_planner_llm
from .prompts import EXECUTOR_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT
from m365_assistant.agent import state
from langchain_core.messages import ToolMessage

def build_graph(mcp_tools):

    executor_llm = get_executor_llm().bind_tools(mcp_tools)
    planner_llm = get_planner_llm()

    graph = StateGraph(AgentState)

    # Node 1 — Fetch Context
    


    async def fetch_context(state: AgentState):

        messages = [
            SystemMessage(content=EXECUTOR_SYSTEM_PROMPT),
            HumanMessage(content=state["user_input"])
        ]

        while True:

            response = await executor_llm.ainvoke(messages)

            # No tool calls → finished
            if not response.tool_calls:
                return {"fetched_context": response.content}

            # Execute tool calls
            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                tool = next(t for t in mcp_tools if t.name == tool_name)

                result = await tool.ainvoke(tool_args)

                messages.append(response)
                messages.append(
                    ToolMessage(
                        tool_call_id=tool_call["id"],
                        content=str(result),
                    )
                )

    async def fetch_context(state: AgentState):

        messages = state.get("messages", [])

        # Add new user message
        messages.append(HumanMessage(content=state["user_input"]))

        while True:

            response = await executor_llm.ainvoke(messages)

            if not response.tool_calls:
                messages.append(response)
                return {
                    "fetched_context": response.content,
                    "messages": messages
                }

            for tool_call in response.tool_calls:

                tool = next(t for t in mcp_tools if t.name == tool_call["name"])
                result = await tool.ainvoke(tool_call["args"])

                messages.append(response)
                messages.append(
                    ToolMessage(
                        tool_call_id=tool_call["id"],
                        content=str(result),
                    )
                )

    # Node 2 — Create Routine
    async def create_schedule(state: AgentState):
        response = await planner_llm.ainvoke([
            SystemMessage(content=PLANNER_SYSTEM_PROMPT),
            HumanMessage(content=state["fetched_context"])
        ])

        return {"final_schedule": response.content}


        return {
            "final_schedule": response.content,
            "messages": messages
        }



    graph.add_node("fetch_context", fetch_context)
    graph.add_node("create_schedule", create_schedule)

    graph.set_entry_point("fetch_context")
    graph.add_edge("fetch_context", "create_schedule")

    # # LOOP BACK
    # graph.add_edge("create_schedule", "fetch_context")


    return graph.compile()
