# agent/agent.py
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_cohere import ChatCohere

from agent.tools import (
    fetch_articles,
    stock_forecast,
    stock_fundamentals,
    stock_technicals,
)
from config import config

# 1) Define your system prompt once
SYSTEM_PROMPT = (
    "You are a professional financial analyst assistant.\n"
    "You have access to the following tools:\n"
    "- fetch_articles(query: str, language: str): Use for live market news, recent developments, or headlines about a company or region.\n"
    "- stock_forecast(...): For analyst projections\n"
    "- stock_fundamentals(...): For financial overviews\n"
    "- stock_technicals(...): For technical indicators\n\n"
    "Do not guess. Always use tools when the user asks for current status, sentiment, or data."
)

# 2) Initialize Cohere LLM and bind tools
llm = ChatCohere(
    model="command-r-plus-v2",
    cohere_api_key=config.COHERE_API_KEY,
)
llm_with_tools = llm.bind_tools([
    fetch_articles,
    stock_forecast,
    stock_fundamentals,
    stock_technicals,
])

def ai_interaction_node(state: MessagesState) -> dict:
    history = state["messages"]

    # 3) If no SystemMessage yet, prepend it exactly once
    if not any(isinstance(m, SystemMessage) for m in history):
        history = [SystemMessage(content=SYSTEM_PROMPT)] + history

    # 4) Invoke the tool-enabled LLM
    assistant_reply = llm_with_tools.invoke(history)

    return {"messages": history + [assistant_reply]}

def create_graph():
    tools = [
        fetch_articles,
        stock_forecast,
        stock_fundamentals,
        stock_technicals,
    ]

    builder = StateGraph(MessagesState)
    builder.add_node("ai", ai_interaction_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "ai")
    builder.add_conditional_edges("ai", tools_condition)
    builder.add_edge("tools", "ai")
    builder.add_edge("ai", END)

    return builder.compile()
