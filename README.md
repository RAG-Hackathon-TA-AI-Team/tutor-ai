# tutor-ai

## Install Dependencies
1. Make sure you have python 3.7.1 or newer and pip installed
2. Follow https://ffmpeg.org/download.html to install ffmpeg. Ensure
'''
ffmpeg -version
'''
does have output.
For example, on Ubuntu/Debian, ffmpeg can be installed by
'''
sudo apt update && sudo apt install ffmpeg

3. Add your OpenAI API token with GPT-4 access to env:OPENAI_API_KEY. Example: Add
'''
export OPENAI_API_KEY='<your token>'
'''
to ~/.bashrc or ~/.zprofile

4. Install Python packages. Run
'''
pip install --upgrade openai
'''

If you met any problem, checkout https://platform.openai.com/docs/quickstart?context=python

## Current Status
Created python library keyframe_extractor.extractor. keyframe_extractor.extractor.extract() extracts key frames from a video. It takes in parameter src, which is path to the source video, and a parameter dest_dir, which is where output frames are stored.
Created python library image_to_test.parser. image_to_test.parser.parse() takes in a vector of image filenames, and output a single string from Vision GPT-4 summarizing those images.
Checkout example.py for usages.
