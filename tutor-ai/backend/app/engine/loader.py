import os
from typing import List

from app.engine.constants import DATA_DIR
from app.engine.schema import VideoMetadata, VideoMetaType, create_keyframe_meta, create_transcript_meta
from llama_index import VectorStoreIndex, download_loader
from llama_index import SimpleDirectoryReader, Document


def get_mock_documents() -> List[Document]:
    # transcripts
    transcript_text = Document.example().text
    transcript_meta = create_transcript_meta(
        video_path="./video/example.mp4",
        start_time=0.0,
        end_time=10.0,
        text=transcript_text,
    )

    # keyframes
    keyframe_meta = create_keyframe_meta(
        video_path="./video/example.mp4",
        start_time=0.0,
        end_time=10.0,
        frame_path="./example.jpg",
    )

    transcript_doc = Document(
        text=transcript_text,
        metadata=transcript_meta,
    )
    keyframe_doc = Document(
        text="",
        metadata=keyframe_meta,
    )

    return [transcript_doc, keyframe_doc]


def get_documents() -> List[Document]:
    return get_mock_documents()
