from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


embedding_service = EmbeddingService()
qdrant_service = QdrantService()

qdrant_service.create_collection()

#