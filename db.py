import json

from settings import settings


def get_connection():
    import pyodbc

    if not settings.azure_sql_connection_string:
        raise RuntimeError(
            "Falta AZURE_SQL_CONNECTION_STRING. Configurala en .env, Azure DevOps o secretos de ACA."
        )
    return pyodbc.connect(settings.azure_sql_connection_string)


def create_table_if_not_exists() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        IF OBJECT_ID('dbo.knowledge_chunks', 'U') IS NULL
        CREATE TABLE dbo.knowledge_chunks (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(255) NOT NULL,
            source NVARCHAR(255) NULL,
            content NVARCHAR(MAX) NOT NULL,
            embedding NVARCHAR(MAX) NOT NULL,
            embedding_model NVARCHAR(100) NOT NULL,
            created_at DATETIME2 DEFAULT SYSUTCDATETIME()
        );
        """
    )
    conn.commit()
    conn.close()


def count_chunks() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dbo.knowledge_chunks")
    total = cursor.fetchone()[0]
    conn.close()
    return int(total)


def list_chunks() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, source, content, embedding, embedding_model, created_at
        FROM dbo.knowledge_chunks
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row.id,
            "title": row.title,
            "source": row.source,
            "content": row.content,
            "embedding": json.loads(row.embedding),
            "embedding_model": row.embedding_model,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]


def insert_chunk(
    title: str,
    source: str,
    content: str,
    embedding: list[float],
    embedding_model: str,
) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dbo.knowledge_chunks (title, source, content, embedding, embedding_model)
        VALUES (?, ?, ?, ?, ?)
        """,
        title,
        source,
        content,
        json.dumps(embedding),
        embedding_model,
    )
    conn.commit()
    conn.close()
