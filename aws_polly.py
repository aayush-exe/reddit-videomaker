from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys

# Local file path, will differ
save_directory = ""

# Initialize a session using AWS Polly
session = Session(profile_name="default")
polly = session.client("polly")

def synthesize_polly_speech(input_text, local_file_name, speed_mod):
    
    rate = speed_mod+"%" if speed_mod.isdigit() else speed_mod
    
    # need <speak> and <prosody> wrappers here for SSML text and speed
    ssml_text = f"""
    <speak>
        <prosody rate="{rate}">
            {input_text}.
            Follow for more tips.
        </prosody>
    </speak>
    """
    
    try:
        # Request speech w/ SSML text 
        response = polly.synthesize_speech(
            Text=ssml_text,
            TextType="ssml",
            OutputFormat="mp3",
            VoiceId="Matthew",
            Engine="neural"
        )
    except (BotoCoreError, ClientError) as error:
        # AWS error (uh oh)
        print(error)
        sys.exit(-1)

    # Process binary stream as audio file
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(save_directory, local_file_name + "_voice.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
        print(f"Audio content saved to {output}")
    else:
        print("ERROR: Response did not contain audio data")
        sys.exit(-1)

    try:
        # Request speech marks w/ text
        response_marks = polly.synthesize_speech(
            Text=ssml_text,
            TextType="ssml",
            OutputFormat="json",
            VoiceId="Matthew",
            Engine="neural",
            SpeechMarkTypes=["word", "ssml"]
        )
    except (BotoCoreError, ClientError) as error:
        # AWS error (bad)
        print(error)
        sys.exit(-1)

    # Process speech marks
    if "AudioStream" in response_marks:
        with closing(response_marks["AudioStream"]) as stream:
            speech_marks_output = os.path.join(save_directory, local_file_name + "_marks.json")
            try:
                with open(speech_marks_output, "w") as file:
                    file.write(stream.read().decode('utf-8'))
            except IOError as error:
                print(error)
                sys.exit(-1)
        print(f"Speech marks saved to {speech_marks_output}")
    else:
        print("ERROR: Response did not contain speech marks data")
        sys.exit(-1)