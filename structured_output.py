# --- 03_structured_outputs.py ---
"""
Structured outputs with Pydantic - zero parsing errors
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI

# Define strict schema
class Clause(BaseModel):
    type: str = Field(description="Clause type (e.g., termination, liability)")
    content: str = Field(description="Exact clause text")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    metadata: Optional[dict] = None

class ContractAnalysis(BaseModel):
    clauses: List[Clause]
    total_clauses: int
    high_confidence_count: int

# Force model to return structured output
llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(ContractAnalysis)

# Guaranteed valid Pydantic object or exception
result = structured_llm.invoke("Analyze contract: ...")
# result.clauses[0].confidence  # Type-safe access