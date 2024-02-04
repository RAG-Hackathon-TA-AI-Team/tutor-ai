import os
from typing import List

from app.engine.constants import DATA_DIR
from app.engine.schema import VideoMetadata, VideoMetaType, create_keyframe_doc, create_transcript_doc
from llama_index import VectorStoreIndex, download_loader
from llama_index import SimpleDirectoryReader, Document


def get_mock_documents() -> List[Document]:
    # transcripts
    transcript_text = Document.example().text
    transcript_doc = create_transcript_doc(
        video_path="./video/example.mp4",
        start_time=0.0,
        end_time=10.0,
        text=transcript_text,
    )

    # keyframes
    keyframe_doc = create_keyframe_doc(
        video_path="./video/example.mp4",
        start_time=0.0,
        end_time=10.0,
        frames=["./example.jpg"],
    )

    return [transcript_doc, keyframe_doc]


def get_documents() -> List[Document]:
    return get_mock_documents()
