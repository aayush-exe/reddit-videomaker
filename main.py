from aws_polly import *
from moviepy_maker import *
from smarks_processor import *
from text_processor import *
from audio_video_format import *
from openai_custom import *
from datetime import datetime

username = "admin"

# helper stuff 
def set_username(new_user):
    global username
    username = new_user

def get_timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%m%d%Y,%H:%M:%S")

# Make sure the file paths are good
speed_mult = "115"
text_file_path = 'input_files/current.txt'
voice_file_path = 'voice-output/speech'
output_file_path = 'output/DEFAULT'

def make_money(type=0):
    output_file_path = 'output/'+get_timestamp()+",from@"+username

    # gets TTS and subtitle formatting ready for generation
    print('Processing text')
    init_text = process_text_file(text_file_path)
    print('Sending speech requests')
    synthesize_polly_speech(init_text, voice_file_path, speed_mod=speed_mult)
    print('Processing subtitles')
    subtitles = generate_subtitles(local_file_path = voice_file_path+'_marks.json')
    
    # gets random segments of audio and background
    video_duration = int((get_audio_duration(voice_file_path+"_voice.mp3"))+2)
    print('Creating background and music')
    background, audio_clips = select_randoms(video_duration)

    # Main function, using moviepy to edit everything together
    print('Adding captions (this takes a few minutes)')
    create_captions_video(subtitles, background, audio_clips, video_duration, output_path=output_file_path+'.mp4')
    print('Video successfully saved as '+output_file_path+'.mp4')
    
    # TODO: upload to YouTube and return link
    youtube_link = "none"
    
    
    return youtube_link