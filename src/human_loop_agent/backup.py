"""This module defines the state graph for the LangGraph chatbot."""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from human_loop_agent.configuration import Configuration
from langchain_core.runnables import RunnableConfig
from human_loop_agent.utils import load_chat_model
from human_loop_agent.prompts import SYSTEM_PROMPT
from human_loop_agent.state import ChatbotState


def call_llm(state: ChatbotState, config: RunnableConfig) -> Command:
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    # Prepend the system prompt to the conversation history
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    messages_with_prompt = [system_message] + state.messages  # Access messages as an attribute

    response = model.invoke(messages_with_prompt)

    # Update the state directly
    state.messages = response
    return Command(goto="generate_question")  # Removed update_state


def generate_question(state: ChatbotState) -> Command:
    # Generate a question based on the conversation history
    question = "Could you tell me more about your experience with LangGraph?"

    questions = {
        "role": "system",
        "questions": question,
    }

    # Use interrupt to pause and wait for the user's answer
    state.messages = interrupt({"question": questions})  # Access messages as an attribute

    return Command(goto="call_llm")  # Removed update_state


builder = StateGraph(ChatbotState)
builder.add_node("call_llm", call_llm)
builder.add_node("generate_question", generate_question)

builder.add_edge(START, "generate_question")
builder.add_edge("call_llm", "generate_question")
builder.add_edge("generate_question", "call_llm")
builder.add_edge("generate_question", END)

human_loop_agent = builder.compile()
human_loop_agent.name = "human_loop_agent"
