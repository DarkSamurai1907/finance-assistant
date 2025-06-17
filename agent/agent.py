from langgraph.graph import StateGraph, START
from agent.nodes.overview import *
from agent.state import State
from langgraph.graph.message import MessagesState

def create_graph():
    builder = StateGraph(MessagesState)
    builder.add_node(fetch_market_data)
    builder.add_node(summarize_consensus)
    builder.add_edge(START, "fetch_market_data")
    builder.add_edge("fetch_market_data", "summarize_consensus")
    return builder.compile()