import os
from langchain_cohere import ChatCohere

llm = ChatCohere(model="command-r-plus-v2", cohere_api_key=os.getenv("COHERE_API_KEY"))

def get_summary(prompt: str) -> str:
    print("Prompt: ", prompt)
    print("=========================================================")
    return llm.invoke(prompt).content.strip()

__all__ = ['get_summary']