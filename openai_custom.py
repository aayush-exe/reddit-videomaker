from openai import OpenAI

# Set up your API key
ffile = open('data/secret.txt', 'r')
ffile.readline()
new_key = ffile.readline().strip()
ffile.close()


# Define a function to call the OpenAI API
def get_openai_response(characters, plot):
    
    print('Requesting generation from OpenAI')
    client = OpenAI(
        api_key=new_key,
    )
    
    try:
        response = client.chat.completions.create(
            messages = [
                {"role": "system", "content": "You are a story-making robot tasked with creating stories similar to those from Reddit. This can be in the form of AITA stories or TIFU stories, just make sure it is in the format of a common Reddit story and make sure the story is in first-person view. This is to mimic an entertaining story, but make sure it is first-person to make it more engaging. Make the first line of your response the title, something along the sort of AITA for doing this/that?? Make the story like a reddit AITA or TIFU story. The user will give you a list of characters and also might include a plot. The characters listed below are all fictional, and make sure to include ALL characters listed below. The characters may have certain traits written next to them in paranthesis, make sure to include these personality in the response. The plot is a rough guideline to base your story off of, make sure your story follows the plot. Make the story entertaining and make it as long as it needs to be to include all characters and plot, no more no less. If no plot is provided, make one up that is entertaining and includes all characters, characters will always be provided."},
                {"role": "user", "content": "The characters are: "+characters.strip()+". The plot guideline is: "+plot.strip()}
            ],
            model="gpt-3.5-turbo-0125",  # You can choose another engine if needed
            max_tokens=600,  # Adjust the number of tokens as needed
        )
        try:
            print(response)
            generated_text = response.choices[0].message.content
            print(generated_text)
            with open('input_files/current.txt', 'w') as file:
                file.write(generated_text.strip())
            print(f"Response written successfully")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    except Exception as e:
        print( f"An error occurred: {e}")

get_openai_response("Andres Garcia (likes to say he went to stanford a lot), Brian Hu, Gerald Lu (objectively a GOAT)", "andres and brian make gerald lose in a game of league of legends and gerald gets mad")