from ai_provider import cosine_similarity, create_embedding, generate_answer
from db import list_chunks
from settings import settings


def retrieve_context(question: str) -> list[dict]:
    question_embedding = create_embedding(question)
    scored_chunks: list[dict] = []

    for chunk in list_chunks():
        score = cosine_similarity(question_embedding, chunk["embedding"])
        scored_chunks.append(
            {
                "id": chunk["id"],
                "title": chunk["title"],
                "source": chunk["source"],
                "content": chunk["content"],
                "score": score,
            }
        )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)
    return scored_chunks[: settings.top_k]


def ask_agent(question: str) -> dict:
    chunks = retrieve_context(question)
    answer = generate_answer(question, chunks)
    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "title": chunk["title"],
                "source": chunk["source"],
                "score": round(chunk["score"], 3),
            }
            for chunk in chunks
        ],
    }
