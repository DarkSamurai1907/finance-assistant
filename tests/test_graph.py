from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain_core.messages import SystemMessage
from langchain_cohere import ChatCohere

llm = ChatCohere(model="command-r-plus-v2")

def echo_node(state: MessagesState) -> dict:
    return {"messages": state["messages"] + [SystemMessage(content="pong")]}

def create_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("echo", echo_node)
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    return builder.compile()
