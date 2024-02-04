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
    collection_name = os.getenv("ASTRA_DB_COLLECTION_NAME", "test-1")

    assert astra_db_application_token, "ASTRA_DB_APPLICATION_TOKEN is required"
    assert astra_db_api_endpoint, "ASTRA_DB_API_ENDPOINT is required"

    astra_db_store = AstraDBVectorStore(
        token="AstraCS:phGMiukriFDqacgHjsZZSxOD:9a2e970d6f0230de5290fcb13e3dec8db116c28a8ab9b20ea23e4da0841658fb",
        api_endpoint="https://1cc8497e-1486-4e21-83f4-9911c31d9ca8-us-east-1.apps.astra.datastax.com",
        collection_name="test1",
        embedding_dimension=1536,
    )

    return StorageContext.from_defaults(vector_store=astra_db_store)
