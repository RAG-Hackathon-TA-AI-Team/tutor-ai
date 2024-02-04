from keyframe_extractor.extractor import extract
from image_to_text.parser import parse
import os

def main():
    dest_dir = 'data/frames'
    # extract key frames from video
    frames = extract('data/Tidead.mp4', dest_dir)
    # frames should include timestamps and corresponding frames' filenames
    print(frames)
    imgs = []
    for frame in frames:
        imgs.append(frame['filename'])
    # retrieve summary of frames from GPT-4 Vision
    # parse frames one-by-one if we want info at each timestamp
    text = parse(imgs)
    print(text)
    for file in os.listdir(dest_dir):
        os.remove(dest_dir + "/" + file)
    os.rmdir(dest_dir)

main()