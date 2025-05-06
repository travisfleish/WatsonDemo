"""
Base tool implementation compatible with CrewAI 0.75.0
"""
from typing import Any, Dict, Callable, Optional, List, Type
import json

class BaseTool:
    """Base class for tools compatible with CrewAI 0.75.0"""

    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self._func = func

        # Create a model_fields attribute that CrewAI expects
        self.model_fields = {
            "tool_input": {
                "type": "string",
                "description": "Input for the tool"
            }
        }

    def __call__(self, tool_input: str) -> str:
        """Execute the tool with the given input"""
        return self._func(tool_input)

    def invoke(self, *args, **kwargs) -> str:
        """
        Invoke method that CrewAI 0.75.0 calls on tools.

        This method accepts any arguments and keyword arguments for flexibility
        and handles the different ways CrewAI might call the tool.

        Returns:
            str: The result of executing the tool
        """
        try:
            # Check if 'input' is in kwargs (as seen in the error message)
            if 'input' in kwargs:
                input_data = kwargs['input']
            # Check if there are positional arguments
            elif len(args) > 0:
                input_data = args[0]
            else:
                return "Error: No input provided to tool"

            # Handle input data
            if isinstance(input_data, dict):
                # If input is already a dict, extract the right parameter
                if 'query' in input_data:
                    return self._func(input_data['query'])
                elif 'expression' in input_data:
                    return self._func(input_data['expression'])
                elif 'tool_input' in input_data:
                    return self._func(input_data['tool_input'])
                else:
                    # Just use the first value in the dict
                    return self._func(next(iter(input_data.values())))
            elif isinstance(input_data, str):
                # Try to parse as JSON if it's a string
                if input_data.startswith('{'):
                    try:
                        parsed_input = json.loads(input_data)
                        if 'query' in parsed_input:
                            return self._func(parsed_input['query'])
                        elif 'expression' in parsed_input:
                            return self._func(parsed_input['expression'])
                        elif 'tool_input' in parsed_input:
                            return self._func(parsed_input['tool_input'])
                        else:
                            # If no recognized parameter, use the first value
                            return self._func(next(iter(parsed_input.values())))
                    except json.JSONDecodeError:
                        # If not valid JSON, just use the string directly
                        return self._func(input_data)
                else:
                    # If not JSON, pass the input directly
                    return self._func(input_data)
            else:
                # For any other type, convert to string
                return self._func(str(input_data))
        except Exception as e:
            return f"Error processing tool input: {str(e)}"

def create_tool(func: Callable, name: Optional[str] = None, description: Optional[str] = None) -> BaseTool:
    """
    Create a tool from a function.

    Args:
        func: The function to wrap
        name: The name of the tool (defaults to function name)
        description: The description of the tool (defaults to function docstring)

    Returns:
        BaseTool: A tool instance compatible with CrewAI 0.75.0
    """
    name = name or func.__name__
    description = description or func.__doc__ or ""

    return BaseTool(name=name, description=description, func=func)