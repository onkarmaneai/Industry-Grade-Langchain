# --- 02_prompt_patterns.py ---
"""
Production-grade prompt patterns
Key: structure, validation, error handling
"""
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Pattern 1: Multi-message prompt with explicit structure
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a legal contract analyzer.

    RULES:
    - Return ONLY valid JSON
    - If uncertain, use null (never guess)
    - Follow exact format specified
    - No preamble or explanation"""),

    ("human", "Contract text:\n{contract}"),

    ("human", "Extract these clause types:\n{clause_types}"),

    ("human", """Output format:
    {{
        "clauses": [
            {{"type": "termination", "content": "...", "confidence": 0.95}}
        ],
        "metadata": {{"total": 5, "uncertain": 1}}
    }}""")
])
