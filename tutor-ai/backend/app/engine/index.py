import logging
import os
from dotenv import load_dotenv, find_dotenv
from llama_index import (
    StorageContext,
    load_index_from_storage,
    VectorStoreIndex,
)

from app.engine.constants import STORAGE_DIR
from app.engine.context import create_service_context

load_dotenv(find_dotenv())

def get_chat_engine():
    service_context = create_service_context()
    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        raise Exception(
            "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
        )
    logger = logging.getLogger("uvicorn")
    # load the existing index
    logger.info(f"Loading index from {STORAGE_DIR}...")
    os.environ["OPENAI_API_KEY"] = "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"
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = VectorStoreIndex.from_documents(
        documents=[],
        storage_context=storage_context,
        service_context=service_context,
    )
    logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index.as_chat_engine(similarity_top_k=5, chat_mode="condense_plus_context")
