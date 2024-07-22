import os
import json
import random
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import *
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

import smarks_processor


video_duration = 30

# chooses random background from "backgrounds" folder
items = os.listdir("backgrounds")
file_count = sum(1 for item in items if os.path.isfile(os.path.join("backgrounds", item))) - 1

clip_number = str(random.randint(0, file_count-1))
background = VideoFileClip("backgrounds/background_" + clip_number + ".mp4")

# selects random starting point
starting = random.randint(0, int(background.duration - video_duration))
background = background.subclip(starting, starting + video_duration)

print("using clip #" + clip_number + " with starting time " + str(starting // 60) + ":" + str(starting % 60))

background.write_videofile("output/testingmore.mp4", threads=4, audio=False, logger=None)

def create_captions_video(subtitles, video_width=720, video_height=1280):
    clips = []
    for (start_time, end_time), (normal_before, highlighted, normal_after) in subtitles:
        text = f"{normal_before} {highlighted} {normal_after}".strip()
        
        # Create a TextClip for each caption
        txt_clip = TextClip(text, fontsize=70, color='white', size=(video_width, video_height), bg_color='black')
        
        # Highlight the current word in blue
        highlighted_clip = TextClip(highlighted, fontsize=70, color='blue', size=(video_width, video_height), bg_color='black')
        
        # Set the position and duration for each TextClip
        txt_clip = txt_clip.set_start(start_time / 1000).set_duration((end_time - start_time) / 1000).set_position('center')
        highlighted_clip = highlighted_clip.set_start(start_time / 1000).set_duration((end_time - start_time) / 1000).set_position('center')
        
        # Apply animation to the highlighted word
        highlighted_clip = highlighted_clip.crossfadein(0.1).crossfadeout(0.1)
        
        # Composite both clips
        composite_clip = CompositeVideoClip([txt_clip, highlighted_clip])
        
        clips.append(composite_clip)
    
    video = CompositeVideoClip(clips, size=(video_width, video_height))
    video.write_videofile("output/captions_video_9_16.mp4", fps=24, logger=None)

# Path to the JSON input file
file_path = 'speech_marks.json'  # Update with the actual file path

# Generate subtitles from the JSON input file
subtitles = smarks_processor.generate_subtitles(file_path, chunk_size=3)

# Create the captions video with animated text
create_captions_video(subtitles)

# showing clip
# clip.write_videofile("movie.mp4", threads=4, audio=False, logger=None)
