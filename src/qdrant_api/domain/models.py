
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from qdrant_client.http.models import Distance


class HealthCheckResponse(BaseModel):
    """
    Model for the health check response.

    Atributes:
        status (str): Current status of the API (e.g., "ok").
        timestamp (str): ISO-formatted timestamp of the health check.
    """
    status: str
    timestamp: str


# --- Create / Ensure Collection ---

class CreateCollectionRequest(BaseModel):
    """
    Request body to create (or ensure) a Qdrant collection.
    """
    collection_name: str = Field(..., description="Name of the collection to create or ensure exists")
    vector_size: int = Field(..., gt=0, description="Dimensionality of the vectors in this collection")
    distance: Distance = Field(Distance.COSINE, description="Distance metric for similarity search")
    shards: Optional[int] = Field(None, gt=0, description="Number of shards (defaults to cluster setting)")
    replicas: Optional[int] = Field(None, gt=0, description="Number of replicas per shard")


class CreateCollectionResponse(BaseModel):
    """
    Response for collection creation or ensure-collection.
    """
    status: str = Field(..., description="Result status, e.g. 'created', 'already_exists'")


# --- List / Check / Get Collection ---

class ListCollectionsResponse(BaseModel):
    """
    Response model listing all collection names.
    """
    collections: List[str] = Field(..., description="All existing collection names")


class CollectionExistsResponse(BaseModel):
    """
    Response model indicating if a collection exists.
    """
    exists: bool = Field(..., description="True if the named collection exists")


class GetCollectionResponse(BaseModel):
    """
    Response model for detailed info on a single collection.
    The content is whatever Qdrant returns (config, status, payload schema...).
    """
    result: Dict[str, Any] = Field(..., description="Full collection metadata as returned by Qdrant")


class Point(BaseModel):
    id: Union[int, str] = Field(..., description="Unique identifier of the point")
    vector: List[float] = Field(..., description="Vector embedding for the point")
    payload: Optional[Dict[str, Union[str, int, float, bool]]] = Field(
        None, description="Optional metadata associated with the point"
    )

class InsertPointsRequest(BaseModel):
    collection_name: str = Field(..., description="Target collection name")
    points: List[Point] = Field(..., description="List of points to insert into the collection")

class InsertPointsResponse(BaseModel):
    status: str = Field(..., description="Insertion status, e.g., 'ok'")
    inserted_count: int = Field(..., description="Number of points inserted or upserted")


# --- Search Points ---

class MatchValue(BaseModel):
    value: Union[str, int, float, bool] = Field(..., description="Value to match for filtering")


class FieldCondition(BaseModel):
    key: str = Field(..., description="Payload field key to apply condition on")
    match: MatchValue = Field(..., description="Value condition to match")


class Filter(BaseModel):
    must: List[FieldCondition] = Field(..., description="List of filtering conditions to apply")


class SearchPointsRequest(BaseModel):
    collection_name: str = Field(..., description="Name of the collection to search in")
    query_vector: List[float] = Field(..., description="Vector used for similarity search")
    limit: int = Field(5, gt=0, description="Number of top results to return")
    query_filter: Optional[Filter] = Field(None, description="Optional filtering conditions")

class SearchResult(BaseModel):
    id: Union[int, str]
    score: float
    payload: Optional[Dict[str, Union[str, int, float, bool]]] = None


class SearchPointsResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="Top search results based on similarity")

# ----- Embedding -----

class EmbeddingRequest(BaseModel):
    texts: List[str]

class EmbeddingResponse(BaseModel):
    vectors: List[List[float]]

# ----- Chatbot -----

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
