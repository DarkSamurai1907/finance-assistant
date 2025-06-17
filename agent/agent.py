from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_cohere import ChatCohere
from agent.tools import fetch_articles
from config import config

llm = ChatCohere(
    model="command-r-plus-v2",
    cohere_api_key=config.COHERE_API_KEY
)
llm_with_tools = llm.bind_tools([
    fetch_articles
])

def ai_interaction(state: MessagesState) -> dict:
    response = llm_with_tools.invoke(state['messages'])
    return {'messages': response}

# build graph
def create_graph():
    builder = StateGraph(MessagesState)
    builder.add_node('ai', ai_interaction)
    builder.add_node('tools', ToolNode([fetch_articles]))

    builder.add_edge(START, 'ai')
    builder.add_conditional_edges('ai', tools_condition)
    builder.add_edge('tools', 'ai')
    builder.add_edge('ai', END)

    return builder.compile()
