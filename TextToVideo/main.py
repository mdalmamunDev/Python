import os
from gtts import gTTS
from PIL import Image

def text_to_speech(text, audio_path):
    """ Convert text to speech and save as an MP3 file """
    tts = gTTS(text=text, lang="en")
    tts.save(audio_path)

def ensure_even_dimensions(image_path):
    """ Ensure image has even width and height to avoid FFmpeg errors """
    img = Image.open(image_path)
    width, height = img.size

    # Adjust width and height to the nearest even number
    new_width = width if width % 2 == 0 else width + 1
    new_height = height if height % 2 == 0 else height + 1

    if new_width != width or new_height != height:
        img = img.resize((new_width, new_height))
        img.save(image_path)
        print(f"Resized image to {new_width}x{new_height} to be FFmpeg compatible.")

def create_video(image_path, text, video_path, duration):
    """ Create a silent video with the text overlay """
    ensure_even_dimensions(image_path)

    os.system(f"""ffmpeg -y -loop 1 -i {image_path} -vf "drawtext=text='{text}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-50, scale=trunc(iw/2)*2:trunc(ih/2)*2" -t {duration} -c:v libx264 -pix_fmt yuv420p {video_path}""")

def merge_audio_video(video_path, audio_path, output_path):
    """ Merge audio with video """
    os.system(f"""ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac -b:a 192k -shortest {output_path}""")

# Input Data
text = "Hello, this is an AI-generated video without using MoviePy."
image_path = "image.jpg"  # Replace with your image file
audio_path = "audio.mp3"
video_path = "silent_video.mp4"
output_path = "output.mp4"

# Step 1: Convert text to speech
text_to_speech(text, audio_path)

# Step 2: Get the duration of the generated audio
audio_duration_cmd = f"ffmpeg -i {audio_path} 2>&1 | grep Duration"
duration_info = os.popen(audio_duration_cmd).read()
duration_parts = duration_info.split(",")[0].split(":")

if len(duration_parts) >= 3:
    duration = float(duration_parts[1]) * 3600 + float(duration_parts[2]) * 60 + float(duration_parts[3])
else:
    duration = 10  # Default fallback

# Step 3: Create a silent video with text overlay
create_video(image_path, text, video_path, duration)

# Step 4: Merge the silent video with the generated audio
merge_audio_video(video_path, audio_path, output_path)

print("Video created successfully!")
