import json


# formats input from JSON file to be used later
def load_input(input_file_path):
    json_input = '''[\n'''
    with open(input_file_path, 'r') as file:
        for line in file:
            line=line.strip()
            json_input+="\t"+ line+",\n"
        json_input=json_input[:len(json_input)-2]+"\n]"
    return json_input



# function to be called in main
def generate_subtitles(local_file_path = 'voice-output/speech'):
    
    # loading input and calling prev func
    json_input = load_input(input_file_path=local_file_path)
    speech_marks = json.loads(json_input)
    
    subtitles = []
    num_words = len(speech_marks)
    
    # Quick explanation:
    #
    # the way the captions are processed is that the 
    # paragraph is split into multiple "chunks" (determined by chunk_size)
    # 
    # each chunk will have a different "highlighted word" depending on 
    # when that word is said (info found in speech marks)
    # 
    # the chunks are shown on the screen together and the words are highlighted one at a time
    
    
    # Haha just kidding
    # that was the original plan but moviepy doesn't let you render the blue on top of the white and its difficult to have it line up because font isn't monospaced
    # so i will just have it put up one word at a time (which is more common)
    
    # TODO: have title show up as one big block
        
    i = 0
    while i < num_words:
        
        # get values from json value
        start_time = (speech_marks[i]['time'] + 1)
        end_time = (speech_marks[i + 1]['time']) if i + 1 < num_words else start_time + 1500
        current_word = speech_marks[i]['value']
        
        # if one word is too short time display on the screen, combine it with the next word
        if (end_time - start_time)<170 and i + 2 < num_words:
            end_time = (speech_marks[i + 2]['time'])
            current_word += " "+speech_marks[i+1]['value']
            i+=1

        # create tuples based on those values
        # current_word = current_word.lower()
        subtitle = ((start_time, end_time), current_word)
        subtitles.append(subtitle)
        
        i += 1
    
    return subtitles