import os
from llama_index import ServiceContext
from dotenv import load_dotenv, find_dotenv

from app.context import create_base_context
from app.engine.parser import VideoNodeParser
from app.engine.constants import CHUNK_SIZE, CHUNK_OVERLAP
from llama_index.vector_stores import AstraDBVectorStore
from llama_index import StorageContext

load_dotenv(find_dotenv())


def create_service_context():
    base = create_base_context()
    return ServiceContext.from_defaults(
        llm=base.llm,
        embed_model=base.embed_model,
        node_parser=VideoNodeParser(),
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )


def create_storage_context():
    astra_db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    astra_db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
    collection_name = os.getenv("ASTRA_DB_COLLECTION_NAME", "test")

    assert astra_db_application_token, "ASTRA_DB_APPLICATION_TOKEN is required"
    assert astra_db_api_endpoint, "ASTRA_DB_API_ENDPOINT is required"

    astra_db_store = AstraDBVectorStore(
        token=astra_db_application_token,
        api_endpoint=astra_db_api_endpoint,
        collection_name=collection_name,
        embedding_dimension=1536,
    )

    return StorageContext.from_defaults(vector_store=astra_db_store)
