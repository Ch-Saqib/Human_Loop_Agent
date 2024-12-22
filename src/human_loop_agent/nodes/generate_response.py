# """This module contains the `generate_response` function which is responsible for generating a response."""

# from typing import cast

# from langchain_core.messages import AIMessage, trim_messages
# from langchain_core.runnables import RunnableConfig

# from student_support_agent.configuration import Configuration

# # Import the tools node
# from student_support_agent.nodes._tools import student_assistant_tools
# from student_support_agent.prompts import AGENT_SYSTEM
# from student_support_agent.state import StudentAssistantGraphAnnotation
# from student_support_agent.utils import load_chat_model


# async def generate_response(
#     state: StudentAssistantGraphAnnotation, config: RunnableConfig
# ) -> dict[str, list[AIMessage]]:
#     """Generate a response based on the given state and configuration.

#     This function initializes a chat model with tool bindings, formats the system prompt,
#     trims the state messages to fit within the model's context window, and invokes the model
#     to generate a response. If the state indicates it's the last step and the model still
#     wants to use a tool, it returns a message indicating that an answer could not be found.

#     Args:
#         state (StudentAssistantGraphAnnotation): The current state of the student assistant graph.
#         config (RunnableConfig): The configuration for running the model.

#     Returns:
#         dict[str, list[AIMessage]]: A dictionary containing the model's response messages.
#     """
#     configuration = Configuration.from_runnable_config(config)

#     # Initialize the model with tool binding. Change the model or add more tools here.
#     model = load_chat_model(configuration.model).bind_tools(student_assistant_tools)

#     trimmedStateMessages = trim_messages(
#         state.messages,
#         max_tokens=40000,  # adjust for model's context window minus system & files message
#         strategy="last",
#         token_counter=model,
#         include_system=False,  # Not needed since systemMessage is added separately
#         allow_partial=True,
#     )

#     # Get the model's response
#     response = cast(
#         AIMessage,
#         await model.ainvoke(
#             [
#                 {
#                     "role": "system",
#                     "content": AGENT_SYSTEM.format(
#                         user_profile_data=state.user_profile_data or {},
#                         enrolled_courses_info=state.user_enrolled_courses or {},
#                     ),
#                 },
#                 *trimmedStateMessages,
#             ],
#             config,
#         ),
#     )

#     # Handle the case when it's the last step and the model still wants to use a tool
#     if state.is_last_step and response.tool_calls:
#         return {
#             "messages": [
#                 AIMessage(
#                     id=response.id,
#                     content="Sorry, I could not find an answer to your question - start new chat.",
#                 )
#             ]
#         }

#     # Return the model's response as a list to be added to existing messages
#     return {"messages": [response]}
