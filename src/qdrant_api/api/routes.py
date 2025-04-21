from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from infrastructure.embedding_manager import EmbeddingModel
from domain.models import (
    HealthCheckResponse,
    CreateCollectionRequest,
    CreateCollectionResponse,
    ListCollectionsResponse,
    InsertPointsRequest,
    InsertPointsResponse,
    SearchPointsResponse,
    SearchPointsRequest,
    EmbeddingRequest,
    EmbeddingResponse,
    AskRequest,
    AskResponse
)
from qdrant_client.http.models import (
    VectorParams,
    PointStruct,
    Filter as QdrantFilter,
    FieldCondition as QdrantFieldCondition,
    MatchValue as QdrantMatchValue
)
from api.dependencies import get_qdrant_client
from config.config import settings
import requests


router = APIRouter()

@router.get("/", include_in_schema=False)
def redirect_to_docs():
    """
    Redirect root URL to the API documentation.
    """
    return RedirectResponse(url="/docs")

@router.get("/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    
    Returns:
        dict: A dictionary with service status and current timestamp.
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@router.get(
    "/v1/get_collections",
    response_model=ListCollectionsResponse,
    dependencies=[Depends(get_qdrant_client)],
    summary="List all available collections"
)
async def list_collections():
    """
    List all existing collection names.
    
    Returns:
        dict: A dictionary with a list of collection names.
    """
    client = get_qdrant_client()
    collections = client.get_collections()
    return {"collections": [c.name for c in collections.collections]}

@router.put(
    "/v1/create_collection",
    response_model=CreateCollectionResponse,
    dependencies=[Depends(get_qdrant_client)],
    summary="Create or ensure a collection exists"
)
async def create_collection(
    request: CreateCollectionRequest
):
    """
    Create a new collection or ensure it exists.
    
    Args:
        request (CreateCollectionRequest): Request body containing collection details.
        client (QdrantClient): Qdrant client instance.
    
    Returns:
        dict: A dictionary with the status of the operation.
    """

    client = get_qdrant_client()
    try:
        client.create_collection(
            collection_name=request.collection_name,
            vectors_config=VectorParams(
                size=request.vector_size,
                distance=request.distance
            ),
            replication_factor=request.replicas,
            shard_number=request.shards
        )
        return {"status": "created", "collections": [request.collection_name]}
    except Exception as e:
        if "already exists" in str(e).lower():
            return {"status": "already_exists", "collections": [request.collection_name]}
        raise e

@router.put(
    "/v1/insert_points",
    response_model=InsertPointsResponse,
    summary="Insert or upsert points into a collection",
    dependencies=[Depends(get_qdrant_client)]
)
async def insert_points(request: InsertPointsRequest):
    """
    Insert or upsert points into the specified Qdrant collection.

    Args:
        request (InsertPointsRequest): Request body with collection and points.

    Returns:
        InsertPointsResponse: Status and number of points inserted.
    """
    client = get_qdrant_client()

    point_structs = [
        PointStruct(id=point.id, vector=point.vector, payload=point.payload)
        for point in request.points
    ]

    result = client.upsert(
        collection_name=request.collection_name,
        points=point_structs
    )

    return {
        "status": "ok",
        "inserted_count": result.result.operation_count
    }

@router.post(
    "/v1/search_points",
    response_model=SearchPointsResponse,
    summary="Search for similar vectors in a collection",
    dependencies=[Depends(get_qdrant_client)]
)
async def search_points(request: SearchPointsRequest):
    """
    Perform a similarity search in the specified collection using a vector and optional filter.

    Args:
        request (SearchPointsRequest): Contains the query vector, collection, and filter.

    Returns:
        SearchPointsResponse: List of matching points with scores.
    """
    client = get_qdrant_client()

    qdrant_filter = None
    if request.query_filter:
        qdrant_filter = QdrantFilter(
            must=[
                QdrantFieldCondition(
                    key=cond.key,
                    match=QdrantMatchValue(value=cond.match.value)
                ) for cond in request.query_filter.must
            ]
        )

    search_result = client.search(
        collection_name=request.collection_name,
        query_vector=request.query_vector,
        query_filter=qdrant_filter,
        limit=request.limit
    )

    return {
        "results": [
            {
                "id": point.id,
                "score": point.score,
                "payload": point.payload
            }
            for point in search_result
        ]
    }

@router.post(
    "/v1/embedding",
    response_model=EmbeddingResponse,
    summary="Generate embeddings from text"
)
async def generate_embedding(request: EmbeddingRequest):
    vectors = EmbeddingModel.encode(request.texts, convert_to_numpy=False)
    return {"vectors": [vec.tolist() for vec in vectors]}

@router.post(
    "/v1/ask",
    response_model=AskResponse,
    summary="Ask a question using RAG pipeline with Ollama and Qdrant"
)
async def ask_question(request: AskRequest):
    """
    Answer a question using vector search with Qdrant and response from Ollama.

    Args:
        request (AskRequest): User question.

    Returns:
        AskResponse: Answer generated by the LLM.
    """
    try:
        vector = EmbeddingModel.encode([request.question], convert_to_numpy=False)[0].tolist()

        collection_name = settings.qdrant_collection

        #Search top-k similar vectors
        client = get_qdrant_client()
        result = client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=3
        )

        #Build context from matched documents
        context = "\n".join([
            point.payload.get("text", "") for point in result
        ])

        prompt = f"""Context:\n{context}\n\nQuestion: {request.question}\nAnswer:"""

        ollama_host = settings.ollama_host
        model_name = settings.ollama_model

        response = requests.post(
            f"{ollama_host}/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=60
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to connect to Ollama")

        answer = response.json().get("response", "").strip()
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
