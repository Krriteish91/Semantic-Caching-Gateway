from locust import HttpUser, task, between
import random

PROMPTS = [
    # ---------- Semantic Caching ----------
    "What is semantic caching?",
    "Explain semantic caching.",
    "Describe semantic caching.",
    "How does semantic caching work?",
    "What are the benefits of semantic caching?",
    "How is semantic caching different from exact caching?",

    # ---------- Redis ----------
    "What is Redis?",
    "Explain Redis.",
    "How does Redis work?",
    "Describe Redis caching.",
    "What are Redis data structures?",
    "Why is Redis used for caching?",

    # ---------- Qdrant / Vector DB ----------
    "What is Qdrant?",
    "Explain vector databases.",
    "How does vector search work?",
    "What are embeddings used for?",
    "What is similarity search?",
    "How does Qdrant perform nearest neighbor search?",

    # ---------- LLM ----------
    "What is a Large Language Model?",
    "Explain transformer models.",
    "How do LLMs generate text?",
    "What is prompt engineering?",
    "What is tokenization?",
    "How do embeddings work in LLMs?",

    # ---------- FastAPI ----------
    "What is FastAPI?",
    "Why is FastAPI popular?",
    "How does dependency injection work in FastAPI?",
    "Explain asynchronous programming in FastAPI.",

    # ---------- Docker ----------
    "What is Docker?",
    "Explain Docker containers.",
    "What is Docker Compose?",
    "How do Docker volumes work?",

    # ---------- Observability ----------
    "What is Prometheus?",
    "Explain Grafana dashboards.",
    "What are application metrics?",
    "What is distributed tracing?",
    "Why is monitoring important?",

    # ---------- AI Infrastructure ----------
    "Explain retrieval augmented generation.",
    "What is vector similarity?",
    "How do AI gateways work?",
    "What is an inference server?",
    "Explain embedding models."
]

class SemanticCacheUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def chat_completion(self):

        self.client.post(
            "/v1/chat/completions",
            json={
                "model": "qwen2.5:3b",
                "messages": [
                    {
                        "role": "user",
                        "content": random.choice(PROMPTS)
                    }
                ]
            }
        )