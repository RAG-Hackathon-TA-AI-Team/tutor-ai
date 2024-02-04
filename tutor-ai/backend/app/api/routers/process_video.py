from typing import List

from app.engine.index import get_chat_engine
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
import asyncio
import json

from app.tools.openai.generate import GPTSummarizer
from app.tools.youtube.video_processor import download_video, get_transcription_result_from_yt, combine_transcript, split_video

video_router = r = APIRouter()

# data structure 
class _RequestData(BaseModel):
    video_id: str

chunker = GPTSummarizer()

def chunk_video(full_transcript_with_time_stamp):
    # check lenth of the transcript and chunkize it if too long
    # Assuming `full_transcript_with_time_stamp` is the correct argument to pass
    result = chunker.chunkize_timestamp(full_transcript_with_time_stamp)

    # check if result can be parsed into dict

    print("\n\n")
    print(result)
    print("\n\n")

    chunked_text_dict = []
    try:
        result = "\n".join(result.split("\n")[1:-1])
        result_dict = json.loads(result)

        for item in result_dict:
            # success, start, end, text_block = self.search_time_stamp(chunk_text)
            item["duration"] = float(item["end"]) - float(item["start"])

            chunked_text_dict.append(item)
    except Exception as e:
        print(e)
        chunked_text_dict = []

    return chunked_text_dict

@r.post("/process_video")
async def process_video(
    request: Request,
    data: _RequestData,
):
    # check preconditions and get last message
    video_id: str = data.video_id

    # download video
    video_path: str = download_video(video_id)

    # get transcript
    video_caption: dict = get_transcription_result_from_yt(video_id)

    print(video_caption)
    # chunk video
    video_caption_with_time_stamp: dict = combine_transcript(video_caption)

    print(video_caption_with_time_stamp)

    # chunk video
    chunked_text: list[any] = chunk_video(video_caption_with_time_stamp)

    splitted_video_list: List[str] = []
    for chunk in chunked_text:
        splitted_video_list.append(split_video(video_id, chunk["start"], chunk["end"]))


    # return success response with status 200 and a json file
    return {
        "video_path": video_path,
        "video_caption": video_caption,
        "video_caption_with_time_stamp": video_caption_with_time_stamp,
        "chunked_text": chunked_text,
        "splitted_video_list": splitted_video_list
    }



