from dotenv import load_dotenv

load_dotenv()

from agent import create_graph

if __name__ == "__main__":
    graph = create_graph()
    print("Graph Created!")
    result = graph.invoke({})
    print("Market Consensus Summary:")
    print(result["summary"])
