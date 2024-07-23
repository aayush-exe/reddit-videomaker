import os
import random
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import *
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

from smarks_processor import *

video_duration = 30

# Choose a random background from the "backgrounds" folder
items = os.listdir("backgrounds")
file_count = sum(1 for item in items if os.path.isfile(os.path.join("backgrounds", item))) - 1
clip_number = str(random.randint(0, file_count - 1))
background = VideoFileClip("backgrounds/background_" + clip_number + ".mp4")

# Select a random starting point
starting = random.randint(0, int(background.duration - video_duration))
background = background.subclip(starting, starting + video_duration)

# get a random background audio clip
items = os.listdir("music")
file_count = sum(1 for item in items if os.path.isfile(os.path.join("music", item))) - 1
clip_number = str(random.randint(0, file_count - 1))
random_audio = "music/track_" + clip_number + ".mp3"
audio_clips = ["voice-output/speech_voice.mp3", random_audio]

print("using clip #" + clip_number + " with starting time " + str(starting // 60) + ":" + str(starting % 60))

def create_captions_video(subtitles, background, audio_clips, video_width=720, video_height=1280):
    clips = []
    for (start_time, end_time), current_text in subtitles:
        # Create a TextClip for each caption with a specific font and black outline
        txt_clip = TextClip(
            current_text,
            fontsize=70,
            color='white',
            font='Arial-Rounded-MT-Bold',  # Update with the path to your font if necessary
            stroke_color='black',
            stroke_width=5,
            size=(video_width, video_height // 4)
        )

        # Set the position and duration for each TextClip
        txt_clip = txt_clip.set_start(start_time / 1000).set_duration((end_time - start_time) / 1000).set_position('center')

        # Apply animation to the highlighted word
        txt_clip = txt_clip.crossfadein(0.05).crossfadeout(0.05)
        
        clips.append(txt_clip)
    
    # Combine text clips with background video
    video = CompositeVideoClip([background] + clips, size=(video_width, video_height))

    # Load audio clips
    audio_clips = [AudioFileClip(clip) for clip in audio_clips]

    # Combine audio clips
    combined_audio = CompositeAudioClip(audio_clips).set_duration(video.duration)

    # Add the combined audio to the video
    final_video = video.set_audio(combined_audio)
    final_video.write_videofile("output/test_with_new_captions.mp4", fps=24, logger=None)

# Path to the JSON input file
file_path = 'voice-output/speech_marks.json'  # Update with the actual file path

# Generate subtitles from the JSON input file
subtitles = smarks_processor.generate_subtitles()



# Create the captions video with the background and audio
create_captions_video(subtitles, background, audio_clips)

# showing clip
# clip.write_videofile("movie.mp4", threads=4, audio=False, logger=None)