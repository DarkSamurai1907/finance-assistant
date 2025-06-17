from agent import create_graph
from langchain_core.messages import HumanMessage
from config import config
import sys

if __name__ == '__main__':
    if not config.validate():
        print("Error: Missing required environment variables. Please check your .env file.")
        sys.exit(1)

    graph = create_graph()
    print('Graph Created!')

    user_msg = HumanMessage(content="How is the tech sector in the US doing today? Tell me about Meta's forecast.")
    result = graph.invoke({'messages': [user_msg]})

    for msg in result['messages']:
        msg.pretty_print()
