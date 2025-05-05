"""
Helper utilities for the research proposal generation system.

This module provides common utility functions used throughout the system.
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, Union
from jsonschema import validate, ValidationError
from pathlib import Path

# Import configuration
from config.settings import PROMPTS_DIR, JSON_OUTPUT_INDENT

logger = logging.getLogger(__name__)


def validate_json_output(json_str: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validate JSON output against a schema and fix common issues.

    Args:
        json_str: JSON string to validate
        schema: Optional JSON schema to validate against

    Returns:
        Dict[str, Any]: Parsed and validated JSON

    Raises:
        ValueError: If JSON is invalid and cannot be fixed
    """
    # Try to parse the JSON
    try:
        parsed_json = json.loads(json_str)

        # If schema is provided, validate against it
        if schema:
            try:
                validate(instance=parsed_json, schema=schema)
            except ValidationError as e:
                logger.warning(f"JSON validation error: {str(e)}")
                # Here we could implement automatic fixes for common schema issues

        return parsed_json

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {str(e)}")

        # Try to fix common JSON formatting issues
        try:
            # Sometimes LLMs produce invalid JSON with extra text before/after
            # Try to extract just the JSON part with { } or [ ]
            if '{' in json_str and '}' in json_str:
                start_idx = json_str.find('{')
                end_idx = json_str.rfind('}') + 1
                fixed_json_str = json_str[start_idx:end_idx]
                return json.loads(fixed_json_str)

            elif '[' in json_str and ']' in json_str:
                start_idx = json_str.find('[')
                end_idx = json_str.rfind(']') + 1
                fixed_json_str = json_str[start_idx:end_idx]
                return json.loads(fixed_json_str)

            # Fix missing quotes around keys
            if ': ' in json_str and not '"' in json_str:
                import re
                fixed_json_str = re.sub(r'(\w+):\s', r'"\1": ', json_str)
                return json.loads(fixed_json_str)

            raise ValueError(f"Failed to fix JSON: {json_str[:100]}...")

        except (json.JSONDecodeError, ValueError) as fix_error:
            logger.error(f"Failed to fix JSON: {str(fix_error)}")
            raise ValueError(f"Invalid JSON output: {str(e)}. Could not automatically fix.")


def load_prompt_template(template_name: str) -> str:
    """
    Load a prompt template from the templates file.

    Args:
        template_name: Name of the template to load

    Returns:
        str: The loaded template text

    Raises:
        FileNotFoundError: If the template file doesn't exist
        KeyError: If the template name doesn't exist in the file
    """
    template_file = PROMPTS_DIR / "templates.yaml"

    if not template_file.exists():
        logger.error(f"Template file not found: {template_file}")
        raise FileNotFoundError(f"Template file not found: {template_file}")

    try:
        with open(template_file, 'r') as f:
            templates = yaml.safe_load(f)

        if template_name not in templates:
            logger.error(f"Template not found: {template_name}")
            raise KeyError(f"Template '{template_name}' not found in templates file")

        template = templates[template_name]

        # If the template is a dict with a 'system' key (or others), return the 'system' part
        if isinstance(template, dict) and 'system' in template:
            return template['system']

        return template

    except yaml.YAMLError as e:
        logger.error(f"Error parsing templates file: {str(e)}")
        raise ValueError(f"Error parsing templates file: {str(e)}")


def format_json_output(data: Dict[str, Any]) -> str:
    """
    Format a dictionary as a pretty-printed JSON string.

    Args:
        data: Dictionary to format

    Returns:
        str: Pretty-printed JSON string
    """
    return json.dumps(data, indent=JSON_OUTPUT_INDENT, ensure_ascii=False)


def save_research_proposal(proposal_data: Dict[str, Any], output_dir: str = "output") -> str:
    """
    Save a research proposal to a file.

    Args:
        proposal_data: Proposal data to save
        output_dir: Directory to save the file in

    Returns:
        str: Path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a filename based on the proposal title
    title = proposal_data.get("proposal_title", "research_proposal")
    clean_title = "".join(c if c.isalnum() else "_" for c in title).lower()
    timestamp = proposal_data.get("timestamp", "")

    filename = f"{clean_title}_{timestamp}.json" if timestamp else f"{clean_title}.json"
    filepath = os.path.join(output_dir, filename)

    # Save the proposal
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(proposal_data, f, indent=JSON_OUTPUT_INDENT, ensure_ascii=False)

    logger.info(f"Saved research proposal to {filepath}")
    return filepath


def load_research_proposal(filepath: str) -> Dict[str, Any]:
    """
    Load a research proposal from a file.

    Args:
        filepath: Path to the proposal file

    Returns:
        Dict[str, Any]: The loaded proposal data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Proposal file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        proposal_data = json.load(f)

    logger.info(f"Loaded research proposal from {filepath}")
    return proposal_data