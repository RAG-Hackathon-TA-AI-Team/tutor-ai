import os
from typing import TypedDict, Optional, List
from enum import Enum

from llama_index import Document


class VideoMetaType(str, Enum):
    TRANSCRIPT = "transcript"
    KEYFRAME = "keyframe"


class VideoMetadata(TypedDict, total=False):
    type: VideoMetaType
    video_path: str
    start_time: float
    end_time: float
    text: Optional[str]
    frames: Optional[str]


EXCLUDED_KEYS = [
    "type",
    "video_path",
    "start_time",
    "end_time",
    "frames",
    "text",
]


def create_transcript_meta(
        video_path: str,
        start_time: float,
        end_time: float,
        text: str,
) -> VideoMetadata:
    return {
        "type": VideoMetaType.TRANSCRIPT,
        "video_path": video_path,
        "start_time": start_time,
        "end_time": end_time,
        "text": text,
    }


def create_keyframe_meta(
        video_path: str,
        start_time: float,
        end_time: float,
        frames: List[str],
) -> VideoMetadata:
    return {
        "type": VideoMetaType.KEYFRAME,
        "video_path": video_path,
        "start_time": start_time,
        "end_time": end_time,
        "frames": ",".join(frames),
    }


def create_transcript_doc(
        video_path: str,
        start_time: float,
        end_time: float,
        text: str,
) -> Document:
    metadata = create_transcript_meta(
        video_path=video_path,
        start_time=start_time,
        end_time=end_time,
        text=text,
    )

    return Document(
        text=text,
        metadata=metadata,
        excluded_embed_metadata_keys=EXCLUDED_KEYS,
    )


def create_keyframe_doc(
        video_path: str,
        start_time: float,
        end_time: float,
        frames: List[str],
        text: str = "",
) -> Document:
    metadata = create_keyframe_meta(
        video_path=video_path,
        start_time=start_time,
        end_time=end_time,
        frames=frames,
    )

    return Document(
        text=text,
        metadata=metadata,
        excluded_embed_metadata_keys=EXCLUDED_KEYS,
    )
