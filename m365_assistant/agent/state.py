from typing import TypedDict, Any,List


class AgentState(TypedDict):
    user_input: str
    fetched_context: Any
    final_schedule: str
