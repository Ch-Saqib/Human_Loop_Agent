# """Mock tools to retrieve user profile and progress data."""

# from typing import Annotated, Any, Dict, Optional, Union

# from langchain_core.runnables import RunnableConfig
# from langchain_core.tools import InjectedToolArg, tool

# from data.lib import get_global_neo4j_service


# @tool(parse_docstring=False)
# def user_profile_finder(
#     config: Annotated[RunnableConfig, InjectedToolArg],
# ) -> dict[str, Any]:
#     """Search for user info based on user ID from config.

#     Args:
#         config (RunnableConfig): The current configuration.

#     Returns:
#         Dict[str, Union[bool, Dict[str, Any], str, None]]: The user info.
#     """
#     try:
#         return {
#             "success": True,
#             "data": "User Profile is null.",
#         }
#     except Exception as error:
#         return {"success": False, "error": str(error), "data": None}


# @tool(parse_docstring=False)
# async def user_progress_finder(
#     config: Annotated[RunnableConfig, InjectedToolArg],
# ) -> Dict[str, Union[bool, Dict[str, Any], str, None]]:
#     """Retrieve progress for a user based on user ID from config.

#     Args:
#         config (RunnableConfig): The current configuration.

#     Returns:
#         Dict[str, Union[bool, Dict[str, Any], str, None]]: The user progress.
#     """
#     try:
#         user_id: Optional[str] = config.get("configurable", {}).get("user_id")

#         return {
#             "success": False,
#             "error": f"No progress found for user with ID {user_id}.",
#             "data": None,
#         }

#     except Exception as error:
#         return {
#             "success": False,
#             "error": str(error),
#         }


# @tool(parse_docstring=False)
# async def user_enrolled_courses(
#     config: Annotated[RunnableConfig, InjectedToolArg],
# ) -> dict[str, Any]:
#     """Retrieve the list of available courses.

#     Returns:
#         Dict[str, Union[bool, List[str], str]]: The list of available courses.
#     """
#     try:
#         user_id: Optional[str] = config.get("configurable", {}).get("user_id")

#         query = """
#             MATCH (student:Student {student_id: $studentNodeId})-[:ASSIGNED_TO]->(section:Section)
#             MATCH (student)-[:REGISTERED_IN]->(course:Course)
#             RETURN
#                 course.course_name AS course_name,
#                 course.course_code AS course_code,
#                 section.section_code AS section_code,
#                 section.status AS section_status,
#                 section.registration_deadline AS section_registration_deadline,
#                 course AS course_details
#             """

#         neo4j_client = await get_global_neo4j_service()
#         parameters = {"studentNodeId": user_id}
#         result = await neo4j_client.run_query(query, parameters)
#         return {"success": True, "data": result, "error": None}
#     except Exception as error:
#         return {"success": False, "data": [], "error": str(error)}
