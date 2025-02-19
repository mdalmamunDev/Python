import os
import re
import textwrap
import cv2
import numpy as np
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont


# Input text in Bangla
text_bangla =  "বাংলা ভাষা বিশ্বের সবচেয়ে সমৃদ্ধ ভাষাগুলির মধ্যে একটি। এটি বাংলাদেশের সরকারি ভাষা এবং ভারতের পশ্চিমবঙ্গ, ত্রিপুরা, এবং আসামের কিছু অংশে ভাষা হিসেবে ব্যবহৃত হয়। বাংলা সাহিত্য ও সংস্কৃতি পৃথিবীজুড়ে প্রসিদ্ধ। বাংলা ভাষায় অনেক পুরানো ও আধুনিক সাহিত্য রচনা হয়েছে, যার মধ্যে কবিতা, উপন্যাস, নাটক এবং গল্প অন্তর্ভুক্ত। বাংলাদেশে প্রতিবছর ২১শে ফেব্রুয়ারি ভাষা দিবস হিসেবে পালন করা হয়, যা আন্তর্জাতিক মাতৃভাষা দিবস হিসেবে বিশ্বের অন্যান্য দেশে পালিত হয়। বাংলা ভাষার আধুনিক রূপটির বিকাশ হয়েছে ১৯শ শতাব্দীর প্রথম দিকে, যখন বাংলা সাহিত্যে নতুন ধারার সৃষ্টি হয়। বাংলা ভাষার উত্থান অনেকটা দেশ ও জাতির ইতিহাসের সঙ্গে সম্পর্কিত। বাংলাদেশের ভাষা আন্দোলন এবং স্বাধীনতা সংগ্রামের ইতিহাসও বাংলা ভাষার সাথে জড়িত। আমরা যদি বাংলা ভাষার গুরুত্ব বুঝে এটির রক্ষণাবেক্ষণ করি এবং উন্নতি ঘটাই, তাহলে এটি বিশ্বের অন্যতম গুরুত্বপূর্ণ ভাষা হিসেবে স্বীকৃত হবে। "
image_path = "image.jpg"  # Replace with your image file
audio_path = "output/audio_bangla.mp3"  # Audio output path
output_filename = "output/silent_video_bangla.mp4"
final_output_path = "output/output_bangla.mp4"
# Mobile screen resolution (portrait mode)
width, height = 1080, 1920
fps = 30

# Font for Bangla text
font_path = "/usr/share/fonts/truetype/lohit-bengali/Lohit-Bengali.ttf"  # Linux
font_size = 80  # Font size for better visibility
font = ImageFont.truetype(font_path, font_size)

# Create audio from text (Bangla)
def text_to_speech(text, audio_path, lang="bn"):
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)
    print(f"Audio created successfully: {audio_path}")

# Wrap text to fit the screen
def wrap_text(text, max_width, font_size=24):
    avg_char_width = font_size * 0.6  # Approximate width of each character
    max_chars_per_line = max_width // avg_char_width
    wrapped_text = "\n".join(textwrap.wrap(text, width=int(max_chars_per_line)))
    return wrapped_text

# Function to create silent video with text overlay
def create_video_with_text(sentences, audio_duration, output_filename):
    bg_image = Image.open(image_path).resize((width, height))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    # Calculate the total number of characters in all sentences
    total_characters = sum(len(sentence) for sentence in sentences)

    for sentence in sentences:
        # Calculate the duration for each sentence based on the number of characters
        sentence_duration = (len(sentence) / total_characters) * audio_duration
        num_frames = int(fps * sentence_duration)  # Frames for each sentence

        for _ in range(num_frames):
            # Convert background image to OpenCV format
            img = np.array(bg_image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Create an Image object for text drawing
            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)

            # Wrap text to fit the screen
            wrapped_text = wrap_text(sentence, width, font_size=font_size)

            # Calculate text position (center of screen)
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            x = (width - text_width) // 2
            y = (height - text_height) // 2  # Centered vertically

            # Draw Bangla text
            draw.text((x, y), wrapped_text, font=font, fill="white")

            # Convert back to OpenCV format
            frame = np.array(pil_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Write frame to video
            out.write(frame)

    out.release()
    print(f"Silent video created successfully: {output_filename}")


# Merge audio and silent video
def merge_audio_video(video_path, audio_path, output_path):
    os.system(f"""ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac -b:a 192k -shortest {output_path}""")
    print(f"Final video with audio saved as {output_path}")
    try:
        os.remove(video_path)
        os.remove(audio_path)
        print(f"Deleted temporary files: {video_path}, {audio_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")

# Main process
def create_bangla_video():
    # Step 1: Create audio from text (Bangla)
    text_to_speech(text_bangla, audio_path, lang="bn")

    # Step 2: Get the duration of the generated audio
    audio_duration_cmd = f"ffmpeg -i {audio_path} 2>&1 | grep Duration"
    duration_info = os.popen(audio_duration_cmd).read()
    duration_parts = duration_info.split(",")[0].split(":")

    if len(duration_parts) >= 3:
        audio_duration = float(duration_parts[1]) * 3600 + float(duration_parts[2]) * 60 + float(duration_parts[3])
    else:
        audio_duration = 10  # Default fallback

    # Step 3: Create silent video from sentences
    # Split text into sentences using both Bengali period and comma
    sentences = re.split(r'।|,', text_bangla)

    # Remove any leading or trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences]
    create_video_with_text(sentences, audio_duration, output_filename)

    # Step 4: Merge the audio and silent video
    merge_audio_video(output_filename, audio_path, final_output_path)

# Run the main process
create_bangla_video()
