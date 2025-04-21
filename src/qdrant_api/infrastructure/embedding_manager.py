from sentence_transformers import SentenceTransformer
from config.config import settings

class EmbeddingModel:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(settings.embedding_model_name)
        return cls._model

    @classmethod
    def encode(cls, texts, convert_to_numpy=False):
        model = cls.get_model()
        return model.encode(texts, convert_to_numpy=convert_to_numpy)
