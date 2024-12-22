"""This module defines the student assistant tools for agent."""

from langgraph.prebuilt import ToolNode

from student_support_agent.tools.user_profile_finder import (
    user_enrolled_courses,
    user_profile_finder,
    user_progress_finder,
)

student_assistant_tools = [
    user_profile_finder,
    user_progress_finder,
    user_enrolled_courses,
]

student_assistant_tools_node: ToolNode = ToolNode(student_assistant_tools)
