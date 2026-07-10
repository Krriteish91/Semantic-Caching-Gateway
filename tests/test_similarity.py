from sklearn.metrics.pairwise import cosine_similarity

from app.services.embedding_service import EmbeddingService


service = EmbeddingService()

sentence1 = "What is semantic caching?"
sentence2 = "Explain semantic cache."
sentence3 = "How do I bake a chocolate cake?"

embedding1 = service.generate_embedding(sentence1)
embedding2 = service.generate_embedding(sentence2)
embedding3 = service.generate_embedding(sentence3)

similarity12 = cosine_similarity([embedding1], [embedding2])[0][0]
similarity13 = cosine_similarity([embedding1], [embedding3])[0][0]

print(f"Sentence 1: {sentence1}")
print(f"Sentence 2: {sentence2}")
print(f"Similarity: {similarity12:.4f}")

print()

print(f"Sentence 1: {sentence1}")
print(f"Sentence 3: {sentence3}")
print(f"Similarity: {similarity13:.4f}")