from collections import deque
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage


class SlidingWindowMemory:
    """Keep only last N messages to prevent context explosion"""

    def __init__(self, max_messages=10):
        self.messages = deque(maxlen=max_messages * 2)  # *2 for user+AI pairs

    def add_exchange(self, user_msg, ai_msg):
        self.messages.append(HumanMessage(content=user_msg))
        self.messages.append(AIMessage(content=ai_msg))

    def get_history(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()


llm = ChatOpenAI(model="gpt-4o-mini")

# Usage
memory = SlidingWindowMemory(max_messages=10)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# Conversation with bounded memory
response = chain.invoke({"history": memory.get_history(), "input": "Hi"})
memory.add_exchange("Hi", response.content)