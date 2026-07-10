from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.core.config import Settings

class SemanticCache:

    THRESHOLD = Settings().SEMANTIC_THRESHOLD

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(self, query: str):

        embedding = self.embedding_service.generate_embedding(query)

        results = self.qdrant_service.search_similar(embedding)

        if not results:
            return None

        best_match = results[0]
        print("Best score:", best_match.score)
        if best_match.score < self.THRESHOLD:
            return None

        return {
            "score": best_match.score,
            "payload": best_match.payload,
        }