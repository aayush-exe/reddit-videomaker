from aws_polly import *
from moviepy_maker import *
from smarks_processor import *
from text_processor import *
from audio_video_format import *


speed_factor = 1.2
text_file_path = 'input_files/current.txt'
voice_file_path = 'voice-output/speech'
output_file_path = 'output/mainpy-testing'

def make_money():
    
    print('Processing text')
    init_text = process_text_file(text_file_path)
    print('Sending speech requests')
    #synthesize_polly_speech(init_text, voice_file_path)
    
    # Generate subtitles from the JSON input file
    print('Processing subtitles')
    subtitles = generate_subtitles(speed_mult=speed_factor, local_file_path = voice_file_path+'_marks.json')
    
    print('Creating background and music')
    background, audio_clips = select_randoms(int((get_audio_duration(voice_file_path+"_voice.mp3")/speed_factor)+2))
    # Create the captions video with the background and audio

    print('Adding captions')
    create_captions_video(subtitles, background, audio_clips, speed_mult=speed_factor, output_path=output_file_path+'.mp4')
    
    print('Video successfully saved as '+output_file_path+'.mp4')
    
make_money()