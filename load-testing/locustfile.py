from locust import HttpUser, task, between
import random

PROMPTS = [
    "What is semantic caching?",
    "Explain semantic caching.",
    "How does semantic cache work?",
    "Tell me about semantic caching.",
    "What is Redis?",
    "Explain Redis.",
    "How does Redis work?",
    "What is vector search?",
    "Explain vector databases.",
    "What is Qdrant?",
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