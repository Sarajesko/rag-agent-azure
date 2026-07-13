import hashlib
import math

from settings import settings


def demo_embedding(text: str, dimensions: int = 128) -> list[float]:
    """Crea un vector determinista para poder probar RAG sin coste externo."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values: list[float] = []
    while len(values) < dimensions:
        for byte in digest:
            values.append((byte / 255.0) - 0.5)
            if len(values) == dimensions:
                break
        digest = hashlib.sha256(digest).digest()
    norm = math.sqrt(sum(value * value for value in values))
    return [value / norm for value in values] if norm else values


def create_embedding(text: str) -> list[float]:
    if settings.llm_provider == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(model=settings.embedding_model, input=text)
        return response.data[0].embedding
    return demo_embedding(text)


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "No se encontro contexto relevante en la base de conocimiento."

    if settings.llm_provider == "openai":
        from openai import OpenAI

        context = "\n\n".join(
            f"Titulo: {chunk['title']}\nFuente: {chunk['source']}\nContenido: {chunk['content']}"
            for chunk in chunks
        )
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {
                    "role": "system",
                    "content": "Responde usando solo el contexto proporcionado. Cita las fuentes cuando sea posible.",
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPregunta: {question}",
                },
            ],
        )
        return response.choices[0].message.content or ""

    highlights = [f"- {chunk['title']}: {chunk['content']}" for chunk in chunks]
    return (
        f"Respuesta demo basada en {len(chunks)} fragmentos recuperados para la pregunta "
        f"\"{question}\":\n" + "\n".join(highlights)
    )
