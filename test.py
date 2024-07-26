import os
from pydub import AudioSegment
import librosa
import soundfile as sf

# Ensure the environment variables for ffmpeg and ffprobe are set
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"
os.environ["FFPROBE_BINARY"] = "/opt/homebrew/bin/ffprobe"

def speed_up_speech_audio(audio_file_path, speed_mult=1.5):
    # Load the audio file using librosa
    y, sr = librosa.load(audio_file_path, sr=None)

    # Apply time-stretching using librosa's time_stretch function
    y_fast = librosa.effects.time_stretch(y, speed_mult)

    # Save the modified audio to a temporary file
    temp_file_path = audio_file_path.replace(".mp3", f"_temp_fast_{speed_mult}.wav")
    sf.write(temp_file_path, y_fast, sr)

    # Convert the temporary file back to mp3 using pydub
    faster_audio = AudioSegment.from_wav(temp_file_path)
    output_file_path = audio_file_path.replace(".mp3", f"_fast_{speed_mult}.mp3")
    faster_audio.export(output_file_path, format="mp3")

    # Remove the temporary file
    os.remove(temp_file_path)

    return output_file_path

# Example usage
voice_file_path = "your_audio_file.mp3"
speed_factor = 1.5
output_path = speed_up_speech_audio(voice_file_path, speed_mult=speed_factor)
print(f"Processed audio saved at: {output_path}")
