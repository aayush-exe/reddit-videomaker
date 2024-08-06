import os
import random
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import *
from moviepy.config import change_settings
import moviepy.video.fx.all as vfx
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

from mutagen.mp3 import MP3


# helper functions just random calls but placed here cause they were buggy
def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

def get_video_duration(file_path):
    return VideoFileClip(file_path).duration

def weighted_random_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

# local folder paths
video_folder = "data/backgrounds"
audio_folder = "data/music"

# speed of background video (doesnt affect audio, only visuals)
# sped up to increase brainrot impact
video_speed = 1.2

# % of original brightness for new video
# Must be between 0 and 1
darken_const = 0.8

def select_randoms(video_duration):

    # get all video files + durations from path
    video_count = len([f for f in os.listdir(video_folder) if f.startswith('background_') and f.endswith('.mp4')])
    video_files = [f"background_{i}.mp4" for i in range(video_count)]
    video_durations = [get_video_duration(f"{video_folder}/{f}") for f in video_files]
    video_weights = [duration / sum(video_durations) for duration in video_durations]

    # select a random video based on weighted durations
    selected_video = weighted_random_choice(video_files, video_weights)
    background = VideoFileClip(f"{video_folder}/{selected_video}")
    
    # select a random starting point
    real_duration = video_duration * video_speed
    starting = random.randint(0, int(background.duration - real_duration))
    background = background.subclip(starting, starting + real_duration)
    
    # apply speed and slight darkening effect to make captions pop
    background = background.fl_image(lambda image: image *  darken_const)
    background =  background.fx(vfx.speedx,video_speed)

    # get all audio files + durations from path
    audio_count = len([f for f in os.listdir(audio_folder) if f.startswith('track_') and f.endswith('.mp3')])
    audio_files = [f"track_{i}.mp3" for i in range(audio_count)]
    audio_durations = [get_audio_duration(f"{audio_folder}/{f}") for f in audio_files]
    audio_weights = [duration / sum(audio_durations) for duration in audio_durations]

    # select a random audio based on weighted duration
    selected_audio = weighted_random_choice(audio_files, audio_weights)
    random_audio = f"{audio_folder}/{selected_audio}"
    audio_clips = ["voice-output/speech_voice.mp3", random_audio]
    
    # since we only return the path of the audio file, the random segment of audio is done later, specifically in moviepy_maker
    
    # returns everything
    print("Using video clip '{}' with starting time {}:{} and audio clip '{}'".format(
        selected_video, starting // 60, starting % 60, selected_audio))
    return (background, audio_clips)

