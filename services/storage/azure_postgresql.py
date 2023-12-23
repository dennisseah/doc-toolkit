# Install Azure Database for PostgreSQL Flexible Server.
# Once it is deployed, enable two extensions.
#   Under Server parameters, search for `azure.extensions`
#   Add UUID_OSSP and VECTOR

from typing import Any, Callable

import psycopg2

from common.settings import AzurePostgreSQLSettings


def connect_pgl(settings: AzurePostgreSQLSettings):
    """Connect to the PostgreSQL database server

    :param settings: Azure PostgreSQL settings
    """
    conn_string = " ".join(
        [
            f"host={settings.pghost}",
            f"user={settings.pguser}",
            f"dbname={settings.pgdatabase}",
            f"password={settings.pgpassword}",
            f"sslmode={settings.pgssl}",
        ]
    )
    return psycopg2.connect(dsn=conn_string)


def __runnable(settings: AzurePostgreSQLSettings, func: Callable[[Any, Any], Any]):
    conn = connect_pgl(settings=settings)
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

        return func(conn, cursor)
    finally:
        if cursor:
            cursor.close()
        conn.close()


def create_table(
    settings: AzurePostgreSQLSettings, tbl_name: str, pri_key: str, cols: str
):
    """Create a table in the PostgreSQL database

    :param settings: Azure PostgreSQL settings
    :param tbl_name: table name
    :param pri_key: primary key
    :param cols: columns
    """

    def func(conn, cursor):
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {tbl_name} ( {cols}, PRIMARY KEY ({pri_key}))"
        )
        conn.commit()

    __runnable(settings=settings, func=func)


def drop_table(settings: AzurePostgreSQLSettings, tbl_name: str):
    """Drop a table in the PostgreSQL database

    :param settings: Azure PostgreSQL settings
    :param tbl_name: table name
    """

    def func(conn, cursor):
        cursor.execute(f"DROP TABLE IF EXISTS {tbl_name}")
        conn.commit()

    __runnable(settings=settings, func=func)


def cosine_similarity_search(
    settings: AzurePostgreSQLSettings,
    tbl_name: str,
    query_embedding: list[float],
    limit: int = 100,
) -> list[tuple[Any, ...]]:
    """Cosine similarity search

    :param settings: Azure PostgreSQL settings
    :param tbl_name: table name
    :param query_embedding: query embedding
    :param limit: number of rows to return
    """

    def func(conn, cursor):
        cursor.execute(
            f"""SELECT text, 1 - (embedding <=> %s::vector) AS similarity_score
            FROM {tbl_name}
            ORDER BY 1 - (embedding <=> %s::vector) LIMIT {limit};""",
            (query_embedding, query_embedding),
        )
        return cursor.fetchall()

    return __runnable(settings=settings, func=func)


def add_record(
    settings: AzurePostgreSQLSettings,
    tbl_name: str,
    cols: str,
    vals: str,
    params: tuple | None = None,
):
    def func(conn, cursor):
        if not params:
            cursor.execute(f"INSERT INTO {tbl_name} ({cols}) VALUES ({vals})")
        else:
            cursor.execute(f"INSERT INTO {tbl_name} ({cols}) VALUES ({vals})", params)
        conn.commit()

    __runnable(settings=settings, func=func)


def add_records(
    settings: AzurePostgreSQLSettings,
    tbl_name: str,
    cols: str,
    vals: list[str],
    params: list[tuple | None] | None = None,
):
    def func(conn, cursor):
        if not params:
            for val in vals:
                cursor.execute(f"INSERT INTO {tbl_name} ({cols}) VALUES ({val})")
        else:
            for val, param in zip(vals, params):
                cursor.execute(f"INSERT INTO {tbl_name} ({cols}) VALUES ({val})", param)

        conn.commit()

    __runnable(settings=settings, func=func)


# def main():
#     settings = AzurePostgreSQLSettings.model_validate({})
#     drop_table(settings=settings, tbl_name="test")
#     create_table(
#         settings=settings,
#         tbl_name="test",
#         pri_key="id",
#         cols="id uuid, text text not null, embedding vector(1536)",
#     )

#     from common.settings import AzureOpenAISettings
#     from services.ai.azure_openai import get_embedding

#     openai_settings = AzureOpenAISettings.model_validate({})

#     vals = []
#     params = []
#     for val in ["hello world", "happy birthday", "good morning"]:
#         embeddings = get_embedding(settings=openai_settings, text=val)
#         vals.append("uuid_generate_v4(), %s, %s")
#         params.append((val, embeddings.data[0].embedding))

#     add_records(
#         settings=settings,
#         tbl_name="test",
#         cols="id, text, embedding",
#         vals=vals,
#         params=params,
#     )

#     query = get_embedding(settings=openai_settings, text="hello world")
#     results = cosine_similarity_search(
#         settings=settings,
#         tbl_name="test",
#         query_embedding=query.data[0].embedding,
#     )
#     print(results)


# if __name__ == "__main__":
#     main()
