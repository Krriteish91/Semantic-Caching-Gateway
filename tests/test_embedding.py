from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

embedding = service.generate_embedding(
    "What is semantic caching?"
)

print(type(embedding))
print(len(embedding))
print(embedding[:10])