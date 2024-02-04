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

def search_chunk_transcription(start, end, TranscriptItem):
        chunk_text = ""
        for text_block in TranscriptItem:
            if text_block["start"] >= start and text_block["start"] <= end:
                chunk_text += text_block['text'] + " "

        return chunk_text

def chunk_video_by_fixed_time(video_caption, last_name, chunk_duration=180):
    # check lenth of the transcript and chunkize it if too long
    number_of_chunks = int(last_name / chunk_duration) + 1
    chunked_text_list = []
    for i in range(number_of_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, last_name)
        chunk_text = search_chunk_transcription(start, end, video_caption)
        chunk = {
            "start_time": start,
            "end_time": end,
            "text": chunk_text
        }
        chunked_text_list.append(chunk)
    return chunked_text_list



@r.post("/process_video")
async def process_video(
    request: Request,
    data: _RequestData,
):
    # check preconditions and get last message
    video_id: str = data.video_id

    # download video
    _ = download_video(video_id)

    # get transcript
    video_caption, last_time = get_transcription_result_from_yt(video_id)
   
    # chunk video by fixed time
    chunk_list = chunk_video_by_fixed_time(video_caption, last_time)

    # video_caption_with_time_stamp: dict = combine_transcript(video_caption)
    # chunk video
    # chunked_text: list[any] = chunk_video(video_caption_with_time_stamp)

    for chunk in chunk_list:
        file_path = split_video(video_id, chunk["start_time"], chunk["end_time"])
        chunk['video_path'] = file_path

    # write to chunk_list to a json file
    with open("app/output/" + video_id + "TRANSCRIPT.json", 'w') as f:
        json.dump(chunk_list, f)

    return "success"



