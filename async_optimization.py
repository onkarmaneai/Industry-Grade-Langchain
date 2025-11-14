# --- 01_model_optimization.py ---
"""
Model optimization patterns for production
Demonstrates: streaming, batching, async, model tiering
"""
import asyncio
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Tier 1: Fast, cheap model for initial screening
cheap_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Tier 2: Premium model for complex cases
premium_model = ChatOpenAI(model="gpt-4o", temperature=0)

async def process_contracts_async(contracts):
    """Async processing for 10x speedup"""
    tasks = [cheap_model.ainvoke([HumanMessage(content=c)]) for c in contracts]
    results = await asyncio.gather(*tasks)
    return results

def tier_based_processing(contract, complexity_score):
    """Use cheap model first, escalate if needed"""
    if complexity_score < 0.5:
        return cheap_model.invoke([HumanMessage(content=contract)])
    return premium_model.invoke([HumanMessage(content=contract)])

# Streaming for better UX
def stream_response(query):
    for chunk in cheap_model.stream([HumanMessage(content=query)]):
        print(chunk.content, end="", flush=True)