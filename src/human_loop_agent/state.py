"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END, MessagesState
# from data.global_schema import UserProfile


# @dataclass
# class InputState:
#     """Defines the input state for the agent, representing a narrower interface to the outside world.

#     This class is used to define the initial state and structure of incoming data.
#     """

#     messages: Annotated[Sequence[AnyMessage], add_messages] = field(
#         default_factory=list
#     )
#     """
#     Messages tracking the primary execution state of the agent.

#     Typically accumulates a pattern of:
#     1. HumanMessage - user input
#     2. AIMessage with .tool_calls - agent picking tool(s) to use to collect information
#     3. ToolMessage(s) - the responses (or errors) from the executed tools
#     4. AIMessage without .tool_calls - agent responding in unstructured format to the user
#     5. HumanMessage - user responds with the next conversational turn

#     Steps 2-5 may repeat as needed.

#     The `add_messages` annotation ensures that new messages are merged with existing ones,
#     updating by ID to maintain an "append-only" state unless a message with the same ID is provided.
#     """



@dataclass
class ChatbotState:
    """State to hold messages and track question index."""
    messages: Sequence[AnyMessage] = field(default_factory=list)
    question_index: int = 0  # Track which question to ask next

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
