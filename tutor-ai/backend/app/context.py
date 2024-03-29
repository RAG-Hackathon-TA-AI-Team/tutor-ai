import os

from llama_index import ServiceContext
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding


def create_base_context():
    model = os.getenv("MODEL", "gpt-3.5-turbo")
    embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    return ServiceContext.from_defaults(
        llm=OpenAI(model=model, max_new_tokens=4096, max_tokens=4096),
        embed_model=OpenAIEmbedding(model=embed_model),
    )
