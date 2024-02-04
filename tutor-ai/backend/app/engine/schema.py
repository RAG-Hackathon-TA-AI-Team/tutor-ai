import os
from typing import TypedDict, Optional
from enum import Enum


class VideoMetaType(str, Enum):
    TRANSCRIPT = "transcript"
    KEYFRAME = "keyframe"


class VideoMetadata(TypedDict, total=False):
    type: VideoMetaType
    video_path: str
    start_time: float
    end_time: float
    text: Optional[str]
    frame_path: Optional[str]


def create_transcript_meta(
        video_path: str,
        start_time: float,
        end_time: float,
        text: Optional[str],
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
        frame_path: str,
) -> VideoMetadata:
    return {
        "type": VideoMetaType.KEYFRAME,
        "video_path": video_path,
        "start_time": start_time,
        "end_time": end_time,
        "frame_path": frame_path,
    }
