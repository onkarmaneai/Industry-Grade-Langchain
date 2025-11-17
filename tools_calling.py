# --- 04_tool_calling.py ---
"""
Production tool calling with validation and error handling
"""
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Dict


@tool
def validate_clause(clause_text: str, expected_type: str) -> Dict:
    """Validate if clause matches expected type.

    Args:
        clause_text: The clause content to validate
        expected_type: Expected clause type (e.g., 'termination', 'liability')

    Returns:
        Dict with validation result, confidence, and reasoning
    """
    try:
        # Your validation logic here
        is_valid = perform_validation(clause_text, expected_type)

        return {
            "valid": is_valid,
            "confidence": 0.95,
            "reason": "Clause contains required keywords",
            "status": "success"
        }
    except Exception as e:
        # Return error as data, not exception
        return {
            "valid": False,
            "confidence": 0.0,
            "reason": f"Validation failed: {str(e)}",
            "status": "error"
        }


@tool
def search_contract_database(query: str) -> Dict:
    """Search historical contracts for similar clauses"""
    return {"results": [], "count": 0}


# Bind tools to model
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([validate_clause, search_contract_database])

# Model decides which tools to call
response = llm_with_tools.invoke("Validate this termination clause: ...")
