import subprocess
import os
import re

def extract(src, dest_dir, width = 720, height = 480):
    src = src.rstrip('/')
    dest_dir = dest_dir.rstrip('/')

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    _, src_filename = os.path.split(src)
    src_filename_no_ext, _ = os.path.splitext(src_filename)
    keyframe_file_prefix = dest_dir + "/" + src_filename_no_ext + "_frame"
    keyframe_filename = keyframe_file_prefix + "%02d.jpeg"

    resolution = str(width) + "x" + str(height)

    args = [
        "ffmpeg",
        "-i", src,
        "-vf", "select='eq(pict_type\,I)',showinfo",
        "-vsync", "2",
        "-s", resolution,
        "-f", "image2", keyframe_filename,
    ]

    result = subprocess.run(
        args,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
    )

    if result.returncode != 0:
        print("Error: ffmpeg failed to extract keyframes.")

    frames = []
    pattern = re.compile(r'\[Parsed_showinfo.*\] n: *(?P<n>\d+) +pts: *(?P<pts>\d+) +pts_time: *(?P<pts_time>\d+)(\.(?P<pts_time_dec>\d+))? +pos: *(?P<pos>\d+) .*')

    for line in result.stdout.decode('utf-8').split('\n'):
        line = line.strip()
        match = pattern.search(line)
        if match:
            # original n, which is n in ffmpeg log, starts with 0
            # filename start with 1
            # convert ffmpeg log n to filename n (+1)
            log_n_str = match.group('n')
            log_n_int = int(log_n_str)
            filename_n_int = log_n_int + 1
            filename_n_str = str(filename_n_int)
            if filename_n_int < 10:
                filename_n_str = "0" + filename_n_str
            filename = keyframe_file_prefix + filename_n_str + ".jpeg"

            frames.append({
                'pts': int(match.group('pts')),
                'pts_time': int(match.group('pts_time')),
                'pos': int(match.group('pos')),
                'filename': filename
            })

    return frames

extract("./samples/pos_video.mp4", "samples/frames")