
from config.config import settings
from qdrant_client import QdrantClient


class QdrantManager:
    def __init__(self, host: str = settings.qdrant_host, port: int = settings.qdrant_port):
        """
        Initialize the Qdrant HTTP client.
        """
        self.client = QdrantClient(host=host, port=port)

    def get_client(self) -> QdrantClient:
        """
        Returns the internal Qdrant client instance.
        """
        return self.client

def get_qdrant_client() -> QdrantClient:
    manager = QdrantManager()
    return manager.get_client()
