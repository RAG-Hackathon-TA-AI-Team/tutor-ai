import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import os

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
VIDEO_PATH = "app/videoData"


def get_youtube_transcript(video_id) -> dict:
    """
        Input: video_id
        Output: transcript of the video
    """
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    # Fetching video details to ensure the video exists
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()

    if not response['items']:
        return "Video not found or unavailable"

    # Fetching the transcript
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en']).fetch()
        return transcript
    except Exception as e:
        print(e)
        return str(e)


def download_video(video_id) -> str:
    """
        Input: video_id
        Output: path to the downloaded video
    """
    url = "https://www.youtube.com/watch?v=" + video_id
    yt = YouTube(url, 
        use_oauth=True, 
        allow_oauth_cache=True, 
        # on_progress_callback=progress_func,
        # on_complete_callback=complete_func
    )

    res_list = ['720p', '1080p', '360p']

    for res in res_list:
        print("searching for quality: ", res)
        stream_list = yt.streams.filter(file_extension='mp4', res=res, type="video")
        if len(stream_list) != 0: #check if the download list is not empty
            stream = yt.streams.get_by_itag(int(stream_list[0].itag))
            break

    filename = VIDEO_PATH + "/" + video_id + ".mp4"

    if stream is not None:
        stream.download(filename=filename)

        return filename
    else:
        return False
    

def split_video(video_id, start_time, end_time) -> str:
    """
        Input: video_id, start_time, end_time
        Output: path to the split video
    """
    filename = VIDEO_PATH + "/" + video_id + ".mp4"
    output_filename = VIDEO_PATH + "/" + video_id + "_" + start_time + "_" + end_time + ".mp4"
    os.system(f"ffmpeg -i {filename} -ss {start_time} -to {end_time} -c copy {output_filename}")
    return output_filename
