from typing import Sequence, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langchain_core.runnables import RunnableConfig
from human_loop_agent.configuration import Configuration
from human_loop_agent.utils import load_chat_model
from human_loop_agent.state import ChatbotState

# Define the System Prompt
SYSTEM_PROMPT = """
You are an AI assistant knowledgeable about LangGraph.
Engage the user by generating insightful questions about LangGraph and provide informative responses based on their answers.

Here are some specific questions to consider:
1. What aspects of LangGraph do you find most challenging?
2. How has LangGraph improved your workflow?
3. Are there any features you wish LangGraph had?
4. Can you describe a project where LangGraph was particularly useful?
5. What resources helped you learn LangGraph effectively?
"""


def ask_question(state: ChatbotState) -> Command[Literal["check_answer"]]:
    """Generate a question and interrupt for user input."""
    questions = [
        "What aspects of LangGraph do you find most challenging?",
        "How has LangGraph improved your workflow?",
        "Are there any features you wish LangGraph had?",
        "Can you describe a project where LangGraph was particularly useful?",
        "What resources helped you learn LangGraph effectively?",
    ]

    question_index = state["question_index"]
    if question_index >= len(questions):
        return Command(goto=END)  # End after all questions are asked

    question = questions[question_index]

    # Interrupt to ask the user and update the state
    return Command(
        goto="check_answer",
        update={
            "messages": state["messages"]
            + [{"role": "assistant", "content": question}],
        },
        interrupt=interrupt({"question": question}),
    )


def check_answer(
    state: ChatbotState, resume: dict = None
) -> Command[Literal["ask_question", END]]:
    """
    Check the user's answer and decide whether to proceed.
    Handles resume action from the interrupt.
    """
    if resume:
        # Resume after the interrupt with the user's input
        user_response = resume.get("data", {}).get("response", "").strip()
        if not user_response:
            clarification_message = (
                "I didn't get your response. Could you provide more details?"
            )
            return Command(
                goto="check_answer",
                update={
                    "messages": state["messages"]
                    + [{"role": "assistant", "content": clarification_message}],
                },
                interrupt=interrupt({"question": clarification_message}),
            )

        # Add the user's response to the state and proceed to the next question
        return Command(
            goto="ask_question",
            update={
                "messages": state["messages"]
                + [{"role": "user", "content": user_response}],
                "question_index": state["question_index"] + 1,
            },
        )

    # If no resume action is provided, stay in check_answer
    clarification_message = "Please answer the question to proceed."
    return Command(
        goto="check_answer",
        update={
            "messages": state["messages"]
            + [{"role": "assistant", "content": clarification_message}],
        },
        interrupt=interrupt({"question": clarification_message}),
    )


# Build the state graph
builder = StateGraph(ChatbotState)
builder.add_node("ask_question", ask_question)
builder.add_node("check_answer", check_answer)

builder.add_edge(START, "ask_question")
builder.add_edge("ask_question", "check_answer")
builder.add_edge("check_answer", "ask_question")
builder.add_edge("check_answer", END)

# Compile the graph
human_loop_agent = builder.compile()
human_loop_agent.name = "human_loop_agent"
