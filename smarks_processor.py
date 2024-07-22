import json

json_input = '''[\n'''

#formats json file into format used by python json module
with open("voice-output/speech_marks.json", 'r') as file:
    for line in file:
        line=line.strip()
        json_input+="\t"+ line+",\n"
    json_input=json_input[:len(json_input)-2]+"\n]"
print(json_input)

# processes json using python module
speech_marks = json.loads(json_input)

# function to be called in main hopefully LMAO
def generate_subtitles(speech_marks, chunk_size=3):
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
    # 
    # for an example video i based this on: 
    # 
        
    i = 0
    while i < num_words:
        # chunk size stuffs
        start_index = i
        end_index = min(num_words, start_index + chunk_size)
        
        # Extract the words in the current chunk
        chunk_words = [speech_marks[j]['value'] for j in range(start_index, end_index)]
        
        # Generate the subtitles for each word in the chunk
        for j in range(start_index, end_index):
            # Create the normal and highlighted text segments
            normal_before = ' '.join(chunk_words[:j - start_index])
            highlighted = chunk_words[j - start_index]
            normal_after = ' '.join(chunk_words[j - start_index + 1:])
            
            # Create the subtitle tuple
            start_time = speech_marks[j]['time'] + 1
            end_time = speech_marks[j + 1]['time'] if j + 1 < num_words else start_time + 500
            
            subtitle = ((start_time, end_time), (normal_before, highlighted, normal_after))
            subtitles.append(subtitle)
        
        # Move to the next chunk
        i += chunk_size
    
    return subtitles

# Generate and print subtitles
# subtitles = generate_subtitles(speech_marks, chunk_size=3)
# for subtitle in subtitles:
#     print(subtitle)