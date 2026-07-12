from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.core.config import Settings

class SemanticCache:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()
        self.settings = Settings()

    def search(self, query: str):

        embedding = self.embedding_service.generate_embedding(query)

        results = self.qdrant_service.search_similar(embedding)

        if not results:
            return None

        best_match = results[0]
        print("Best score:", best_match.score)
        if best_match.score < self.settings.SEMANTIC_THRESHOLD:
            return None

        return {
            "score": best_match.score,
            "payload": best_match.payload,
        }