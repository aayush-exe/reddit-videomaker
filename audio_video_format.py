import os
import random
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import *
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

from pydub import AudioSegment


def get_video_duration(file_path):
    return VideoFileClip(file_path).duration

def get_audio_duration(file_path):
    return AudioSegment.from_file(file_path).duration_seconds

def weighted_random_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

def select_randoms(video_duration):
    # Define folder paths
    video_folder = "backgrounds"
    audio_folder = "music"

    # Get all video files and their durations
    video_count = len([f for f in os.listdir(video_folder) if f.startswith('background_') and f.endswith('.mp4')])
    video_files = [f"background_{i}.mp4" for i in range(video_count)]
    video_durations = [get_video_duration(f"{video_folder}/{f}") for f in video_files]
    video_weights = [duration / sum(video_durations) for duration in video_durations]

    # Select a random video based on weighted durations
    selected_video = weighted_random_choice(video_files, video_weights)
    background = VideoFileClip(f"{video_folder}/{selected_video}")

    # Select a random starting point
    starting = random.randint(0, int(background.duration - video_duration))
    background = background.subclip(starting, starting + video_duration)

    # Get all audio files and their durations
    audio_count = len([f for f in os.listdir(audio_folder) if f.startswith('track_') and f.endswith('.mp3')])
    audio_files = [f"track_{i}.mp3" for i in range(audio_count)]
    audio_durations = [get_audio_duration(f"{audio_folder}/{f}") for f in audio_files]
    audio_weights = [duration / sum(audio_durations) for duration in audio_durations]

    # Select a random audio based on weighted durations
    selected_audio = weighted_random_choice(audio_files, audio_weights)
    random_audio = f"{audio_folder}/{selected_audio}"
    audio_clips = ["voice-output/speech_voice.mp3", random_audio]

    print("Using video clip '{}' with starting time {}:{} and audio clip '{}'".format(
        selected_video, starting // 60, starting % 60, selected_audio))

# Example usage
select_randoms(60)  # 60 seconds video duration
