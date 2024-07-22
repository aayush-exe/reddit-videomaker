import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys

# Local file path, will differ
save_directory = "voice-output"

# Initialize a session using AWS Polly
session = Session(profile_name="default")
polly = session.client("polly")

def synthesize_polly_speech(input_text, local_file_name):
    ssml_text = f"<speak>{input_text}</speak>"
    
    try:
        # Request speech synthesis with SSML text
        response = polly.synthesize_speech(
            Text=ssml_text,
            TextType="ssml",
            OutputFormat="mp3",
            VoiceId="Matthew",
            Engine="neural"
        )
    except (BotoCoreError, ClientError) as error:
        # AWS returned an error
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
        # Request speech marks with SSML text
        response_marks = polly.synthesize_speech(
            Text=ssml_text,
            TextType="ssml",
            OutputFormat="json",
            VoiceId="Matthew",
            Engine="neural",
            SpeechMarkTypes=["word", "ssml"]
        )
    except (BotoCoreError, ClientError) as error:
        # AWS returned an error
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

# Example usage
synthesize_polly_speech("Hey chatters, this is me aayush coming at u from this python file, i'm having a great day and i hope you're having a great day as well\nits going pretty good in here", "speech")
