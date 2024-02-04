import os
from typing import List

from app.engine.schema import create_keyframe_doc, create_transcript_doc
from llama_index import Document


def get_mock_documents(mock_frames: List[str]) -> List[Document]:
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
        end_time=1.0,
        frames=mock_frames,
    )

    return [transcript_doc, keyframe_doc]


def get_documents() -> List[Document]:
    return get_mock_documents(["./data/frames/1.jpg", "./data/frames/2.jpg", "./data/frames/3.jpg"])
