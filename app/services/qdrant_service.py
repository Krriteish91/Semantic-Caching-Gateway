from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4

from qdrant_client.models import PointStruct

class QdrantService:

    COLLECTION_NAME = "semantic_cache"

    def __init__(self):
        self.client = QdrantClient(
            host="qdrant",
            port=6333,
        )

    def create_collection(self):

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME in existing:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )
    def store_embedding(
        self,
        embedding: list[float],
        query: str,
        response: str,
        cache_key: str,
        model: str,
    ):

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "query": query,
                        "response": response,
                        "cache_key": cache_key,
                        "model": model,
                    },
                )
            ],
        )
    def search_similar(
        self,
        embedding: list[float],
        limit: int = 1,
    ):

        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=embedding,
            limit=limit,
            with_payload=True,
        )

        return results.points