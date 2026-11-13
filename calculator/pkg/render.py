import json
from typing import Any, Dict


def format_json_output(
    expression: str, 
    result: float, 
    indent: int = 2,
    sort_keys: bool = False,
    ensure_ascii: bool = True
) -> str:
    """
    Format expression and result as JSON with customizable options.
    
    Args:
        expression: The original mathematical expression
        result: The computed result
        indent: Number of spaces for indentation (2, 4, or None for compact)
        sort_keys: Whether to sort the JSON keys alphabetically
        ensure_ascii: Whether to escape non-ASCII characters
    
    Returns:
        Pretty-printed JSON string
    """
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data: Dict[str, Any] = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)