# opensearch_mcp_server.py
from mcp import tool, start_stdio_server
from opensearchpy import OpenSearch
import os

QINDEX = os.getenv("OPENSEARCH_INDEX", "mcp-test-index")
OS_HOST = os.getenv("OPENSEARCH_HOST", "http://localhost:9200")
OS_API_KEY = os.getenv("OPENSEARCH_API_KEY", "")

client = OpenSearch(
    hosts=[OS_HOST],
    http_auth=("admin", OS_API_KEY) if OS_API_KEY else None,
)

@tool
def push_to_opensearch(payload: dict) -> str:
    response = client.index(index=QINDEX, document=payload)
    return f"Document indexed with ID: {response['_id']}"

@tool
def search_opensearch(query: str, top_k: int = 5) -> list:
    result = client.search(
        index=QINDEX,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["user", "assistant"]
                }
            },
            "size": top_k
        }
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

if __name__ == "__main__":
    start_stdio_server()
