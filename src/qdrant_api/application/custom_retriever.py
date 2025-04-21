from langchain.schema import Document
from langchain.vectorstores import VectorStoreRetriever
import requests
from config.config import settings

class APIRetriever(VectorStoreRetriever):
    def __init__(self, collection_name: str, k: int = 3):
        self.collection_name = collection_name
        self.k = k

    def get_relevant_documents(self, query: str) -> list[Document]:

        embedding_response = requests.post(
            "https://localhost:8081/v1/embedding",
            json={"texts": [query]},
            timeout=30
        )

        if embedding_response.status_code != 200:
            raise Exception("Failed to generate embedding from API")

        vector = embedding_response.json()["vectors"][0]

        search_response = requests.post(
            "https://localhost:8081/v1/search_points",
            json={
                "collection_name": self.collection_name,
                "query_vector": vector,
                "limit": self.k
            },
            timeout=30
        )

        if search_response.status_code != 200:
            raise Exception("Failed to search points from API")

        results = search_response.json()["results"]

        return [
            Document(page_content=point["payload"].get("text", ""), metadata={"score": point["score"]})
            for point in results
        ]
