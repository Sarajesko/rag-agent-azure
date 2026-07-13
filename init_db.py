from ai_provider import create_embedding
from db import count_chunks, create_table_if_not_exists, insert_chunk
from settings import settings

SEED_DOCUMENTS = [
    {
        "title": "Que es RAG",
        "source": "guia-entregable5",
        "content": (
            "RAG significa Retrieval Augmented Generation. El sistema recupera fragmentos "
            "relevantes desde una base de conocimiento y los usa como contexto para responder."
        ),
    },
    {
        "title": "Rol de Azure SQL",
        "source": "guia-entregable5",
        "content": (
            "En esta practica Azure SQL almacena la tabla knowledge_chunks con titulo, fuente, "
            "contenido y embeddings. La API consulta esos fragmentos antes de generar la respuesta."
        ),
    },
    {
        "title": "Despliegue en Azure Container Apps",
        "source": "guia-entregable5",
        "content": (
            "La imagen Docker se publica en Azure Container Registry y Azure Container Apps "
            "ejecuta la API con ingress externo en el puerto 8000."
        ),
    },
    {
        "title": "CI/CD con Azure DevOps",
        "source": "guia-entregable5",
        "content": (
            "El pipeline ejecuta tests, construye la imagen, la sube a ACR y actualiza la "
            "Container App existente en cada push a la rama main."
        ),
    },
]


def main() -> None:
    create_table_if_not_exists()
    if count_chunks() > 0:
        print(f"La base de conocimiento ya contiene {count_chunks()} fragmentos.")
        return

    embedding_model = (
        settings.embedding_model if settings.llm_provider == "openai" else "demo-embedding"
    )
    for document in SEED_DOCUMENTS:
        embedding = create_embedding(document["content"])
        insert_chunk(
            title=document["title"],
            source=document["source"],
            content=document["content"],
            embedding=embedding,
            embedding_model=embedding_model,
        )

    print("Base de conocimiento inicial cargada correctamente.")


if __name__ == "__main__":
    main()
