from openai import OpenAI
import base64

client = OpenAI()

def imgs_to_base64s(imgs):
    base64s = []
    for img in imgs:
        with open(img, "rb") as image_file:
            base64s.append(base64.b64encode(image_file.read()))
    return base64s

def base64s_to_text(base64s):
    # update prompt to optimize what gets returned
    content = [{ "type": "text", "text": "What's in the images?" }]
    for base64 in base64s:
        content.append({
            "type": "image_url",
            "image_url": { "url": "data:image/jpeg;base64,%s" % base64.decode('utf-8') },
        })

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": content
        }],
        max_tokens=500,
    )

    return response.choices[0].message.content

def parse(imgs):
    return base64s_to_text(imgs_to_base64s(imgs))

#res = parse([
#    '/home/maxzh/git/tutor-ai/keyframe_extractor/samples/frames/Tidead_frame06.jpeg',
#    '/home/maxzh/git/tutor-ai/keyframe_extractor/samples/frames/Tidead_frame07.jpeg',
#    '/home/maxzh/git/tutor-ai/keyframe_extractor/samples/frames/Tidead_frame08.jpeg',
#    '/home/maxzh/git/tutor-ai/keyframe_extractor/samples/frames/Tidead_frame09.jpeg',
#    '/home/maxzh/git/tutor-ai/keyframe_extractor/samples/frames/Tidead_frame10.jpeg',  
#])
#print(res)
