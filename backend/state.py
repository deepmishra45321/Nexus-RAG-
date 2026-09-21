from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The `add_messages` function appends messages instead of overwriting
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Keep track of the current context/documents retrieved
    context: str
