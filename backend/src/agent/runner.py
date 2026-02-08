import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from agents import Runner
from agents.mcp import MCPServerStdio

from .agent import create_agent


@dataclass
class ChatResult:
    response: str
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)


async def run(messages: List[Dict[str, str]], user_id: str) -> ChatResult:
    """Run the agent with conversation history and MCP tools.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
        user_id: The authenticated user's ID, injected into tool calls.

    Returns:
        ChatResult with the agent's response and any tool calls made.
    """
    # Determine the path to the MCP server module
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    python_executable = sys.executable

    # Inject user_id context into the conversation so the agent knows which user it's operating for
    system_context = f"The current user_id is: {user_id}. You MUST pass this user_id to every tool call."

    agent = create_agent()

    # Prepend the user_id context as a system-level instruction
    augmented_messages = [
        {"role": "user", "content": f"[System context: {system_context}]"},
        {"role": "assistant", "content": "Understood. I will use the provided user_id for all tool operations."},
    ] + messages

    async with MCPServerStdio(
        command=python_executable,
        args=["-m", "backend.src.mcp.server"],
        cwd=backend_dir,
    ) as mcp_server:
        agent = create_agent()
        agent.mcp_servers = [mcp_server]

        result = await Runner.run(agent, augmented_messages)

        # Extract tool calls from the run result
        tool_calls = []
        for item in result.raw_responses:
            if hasattr(item, "output") and isinstance(item.output, list):
                for output_item in item.output:
                    if hasattr(output_item, "type") and output_item.type == "function_call":
                        tool_calls.append({
                            "tool": output_item.name if hasattr(output_item, "name") else "unknown",
                            "input": output_item.arguments if hasattr(output_item, "arguments") else {},
                        })

        return ChatResult(
            response=result.final_output,
            tool_calls=tool_calls,
        )
