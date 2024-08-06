import os

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
os.environ["IMAGEIO_FFPROBE_EXE"] = "/opt/homebrew/bin/ffprobe"
import random
from moviepy.editor import *
from moviepy.config import change_settings
from moviepy.audio.fx.all import *
from moviepy.video.fx.all import *

# this will vary depending on OS, 
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})
from audio_video_format import *
from smarks_processor import *


video_duration = 30

def create_captions_video(subtitles, background, audio_clips, video_duration, video_width=720, video_height=1280, output_path = 'output/default-file-name',):
    clips = []
    offset = 200
    for (start_time, end_time), current_text in subtitles:
        # Create a TextClip for each caption with a specific font and black outline
        txt_clip = TextClip(
            current_text,
            fontsize=44,
            color='white',
            font='data/PolanCanIntoBigWritings.otf',  # Update with the path to your font if necessary
            stroke_color='black',
            stroke_width=3.5,
            size=(video_width, (video_height // 4))
        )
        
        # Set the position and duration for each TextClip
        # Assuming video_height and offset are already defined
        
        # txt_clip = txt_clip.fadein(0.03)

        txt_clip = txt_clip.set_position(("center", video_height // 2 - offset))
        txt_clip = txt_clip.set_start((start_time / 1000)).set_duration(((end_time - start_time) / 1000))
        
        clips.append(txt_clip)

     
    # Combine text clips with background video
    video = CompositeVideoClip([background]+clips, size=(video_width, video_height))

    audio_clips = [AudioFileClip(clip) for clip in audio_clips]

    # Convert the first audio clip to a video clip with a blank frame and apply speedx
    video_clip_0 = ColorClip(size=(1, 1), color=(0, 0, 0), duration=audio_clips[0].duration).set_audio(audio_clips[0])    

    video_duration = video.duration
    audio_duration = audio_clips[1].duration
    max_start_time = audio_duration - video_duration
    random_start_time = random.uniform(0, max_start_time)

    # Trim the second audio clip to start from the random start time
    trimmed_audio_clip_1 = audio_clips[1].subclip(random_start_time, random_start_time + video_duration)
    video_clip_1 = ColorClip(size=(1, 1), color=(0, 0, 0), duration=trimmed_audio_clip_1.duration).set_audio(trimmed_audio_clip_1)

    # Combine audio clips
    combined_audio = CompositeAudioClip([video_clip_0.audio, video_clip_1.audio]).set_duration(video.duration)


    # Add the combined audio to the video
    final_video = video.set_audio(combined_audio)
    final_video.write_videofile(output_path, threads = 32, fps=60, logger=None)



# showing clip
# clip.write_videofile("movie.mp4", threads=4, audio=False, logger=None)