from langchain.chains import ConversationalRetrievalChain
from langchain.llms import Ollama
from application.custom_retriever import APIRetriever
from config.config import settings

def create_rag_chain() -> ConversationalRetrievalChain:
    retriever = APIRetriever(collection_name=settings.qdrant_collection, k=3)

    llm = Ollama(
        base_url=settings.ollama_host,
        model=settings.ollama_model
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        verbose=True
    )


