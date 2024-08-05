from aws_polly import *
from moviepy_maker import *
from smarks_processor import *
from text_processor import *
from audio_video_format import *
from openai_custom import *
from datetime import datetime

username = "admin"

def set_username(new_user):
    global username
    username = new_user

def get_timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    formatted_date = date_time.strftime("%A_%B_%d,%H:%M:%S")
    return formatted_date

speed_mult = "115"
text_file_path = 'input_files/current.txt'
voice_file_path = 'voice-output/speech'
output_file_path = 'output/DEFAULT'

def make_money():
    output_file_path = 'output/'+get_timestamp()+",@"+username
    get_openai_response("Andres Garcia (likes to say he went to stanford a lot), Erin Song, Emmy Vu", "AITA andres promised erin and emmy to play valorant with them but later he ditched them for league of legends")
    
    print('Processing text')
    init_text = process_text_file(text_file_path)
    print('Sending speech requests')
    synthesize_polly_speech(init_text, voice_file_path, speed_mod=speed_mult)
    
    # Generate subtitles from the JSON input file
    print('Processing subtitles')
    subtitles = generate_subtitles(local_file_path = voice_file_path+'_marks.json')
    
    video_duration = int((get_audio_duration(voice_file_path+"_voice.mp3"))+2)
    
    print('Creating background and music')
    background, audio_clips = select_randoms(video_duration)
    # Create the captions video with the background and audio

    print('Adding captions')
    create_captions_video(subtitles, background, audio_clips, video_duration, output_path=output_file_path+'.mp4')
    
    print('Video successfully saved as '+output_file_path+'.mp4')
    
