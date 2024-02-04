import os
import json
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


def load_transcript_json(data: dict) -> List[Document]:
    documents = []
    for transcript_obj in data:
        documents.append(
            create_transcript_doc(
                video_path=transcript_obj["video_path"],
                start_time=transcript_obj["start_time"],
                end_time=transcript_obj["end_time"],
                text=transcript_obj["text"],
            )
        )
    return documents


def get_documents(video_folder: str = "./videos") -> List[Document]:
    # for all json file under videos folder
    documents = []
    for root, dirs, files in os.walk(video_folder):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file)) as f:
                    data = json.load(f)
                    documents.extend(load_transcript_json(data))
    return documents

"""
[
    {
        start: float
        end: float
        frames: [string, string, string]
    },

]
"""