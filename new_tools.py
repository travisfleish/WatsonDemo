# new_tools.py
import logging
from typing import Any, Dict, Optional
from pydantic import Field, BaseModel

logger = logging.getLogger(__name__)


class ToolSpecification(BaseModel):
    name: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None


class Tool:
    """A simple tool implementation compatible with CrewAI 0.75.0"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._specification = ToolSpecification(
            name=name,
            description=description,
            input_schema={"type": "string"}
        )

    @property
    def specification(self) -> ToolSpecification:
        """Return the tool specification"""
        return self._specification

    def __call__(self, input_str: str) -> str:
        """Execute the tool with the given input"""
        return self._execute(input_str)

    def _execute(self, input_str: str) -> str:
        """
        Implement this method in subclasses to define tool behavior.

        Args:
            input_str: The input to the tool

        Returns:
            str: The tool's output
        """
        raise NotImplementedError("Tool subclasses must implement _execute method")