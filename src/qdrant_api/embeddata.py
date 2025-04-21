""""
This class handles the loading of an embedding model and
provides methods to batch-process data for efficient embedding.
It stores the generated embeddings for use in the retrieval system.
"""

import yaml
from sentence_transformers import SentenceTransformer
from typing import List, Union
from tqdm import tqdm

def batch_iterate(data: List[str], batch_size: int):
    """
    Generator that yields batches of data.

    Args:
        data (List[str]): The data to batch.
        batch_size (int): Size of each batch.

    Yields:
        List[str]: Next batch of data.
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

        
class EmbedData:
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initializes the class using parameters from a YAML configuration file.

        Args:
            config_path (str): Path to the YAML config file.
        """
        self.config = self._load_config(config_path)
        self.embed_model_name = self.config["embedding"]["model_name"]
        self.batch_size = self.config["embedding"]["batch_size"]
        self.embed_model = self._load_embed_model()
        self.embeddings = []

    def _load_config(self, path: str) -> dict:
        """
        Loads configuration from a YAML file.

        Args:
            path (str): Path to the YAML config file.

        Returns:
            dict: Parsed configuration.
        """
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _load_embed_model(self) -> SentenceTransformer:
        """
        Loads the embedding model using the SentenceTransformer library.

        Returns:
            SentenceTransformer: The loaded embedding model.
        """
        return SentenceTransformer(self.embed_model_name)

    def generate_embedding(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generates embeddings for a single string or a list of strings.

        Args:
            texts (Union[str, List[str]]): Text(s) to embed.

        Returns:
            List[List[float]]: List of embedding vectors.
        """
        if isinstance(texts, str):
            texts = [texts]

        # Process in batches
        embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_embeddings = self.embed_model.encode(batch, convert_to_numpy=True)
            embeddings.extend(batch_embeddings)

        self.embeddings.extend(embeddings)
        return embeddings
    
    def embed(self, contexts: List[str]):
        """
        Embeds a list of texts using batch processing and shows progress bar.

        Args:
            contexts (List[str]): List of texts to embed.
        """

        self.generate_embedding(contexts)