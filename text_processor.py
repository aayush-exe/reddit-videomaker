import re

def replace_acronyms(text):
    # replaces common acronyms with their full-length counterparts
    # thanks chatgpt
    replacements = {
        "AITA": "Am I the asshole",
        "AITAH": "Am I the asshole",
        "TIL": "Today I learned",
        "IMO": "In my opinion",
        "IMHO": "In my humble opinion",
        "TL;DR": "Too long; didn't read",
        "FWIW": "For what it's worth",
        "BRB": "Be right back",
        "BTW": "By the way",
        "IDK": "I don't know",
        "FYI": "For your information",
        "OP": "Original poster",
        "DM": "Direct message",
        "AMA": "Ask me anything",
        "IIRC": "If I recall correctly",
        "NSFW": "Not safe for work",
        "SMH": "Shaking my head",
        "TBF": "To be fair",
        "TBT": "Throwback Thursday",
        "YOLO": "You only live once",
        "IRL": "In real life",
        "FOMO": "Fear of missing out",
        "FTW": "For the win",
        "GG": "Good game",
        "JK": "Just kidding",
        "LMAO": "Laughing my ass off",
        "NVM": "Never mind",
        "ROFL": "Rolling on the floor laughing",
        "TMI": "Too much information",
        "WTF": "What the fuck",
        "BFF": "Best friends forever",
        "DIY": "Do it yourself",
        "ETA": "Estimated time of arrival",
        "HF": "Have fun",
        "HIFW": "How I feel when",
        "IDC": "I don't care",
        "IFYP": "I feel your pain",
        "ILY": "I love you",
        "LMK": "Let me know",
        "MMW": "Mark my words",
        "NM": "Not much",
        "OMW": "On my way",
        "PPL": "People",
        "RN": "Right now",
        "TBH": "To be honest",
        "TIA": "Thanks in advance",
        "TTYL": "Talk to you later",
        "WBU": "What about you",
        "WTH": "What the hell",
        "WYD": "What you doing",
        "YMMV": "Your mileage may vary",
        "AF": "As fuck",
        "BAE": "Before anyone else",
        "BF": "Boyfriend",
        "GF": "Girlfriend",
        "HRU": "How are you",
        "IDGAF": "I don't give a fuck",
        "IG": "Instagram",
        "IYKYK": "If you know you know",
        "JIC": "Just in case",
        "MCM": "Man crush Monday",
        "OOMF": "One of my followers",
        "OOTD": "Outfit of the day",
        "SB": "Snap back",
        "SC": "Snapchat",
        "SFW": "Safe for work",
        "SNH": "Stupid network hardware",
        "SOB": "Son of a bitch",
        "SRSLY": "Seriously",
        "TBA": "To be announced",
        "TTYN": "Talk to you never",
        "WB": "Welcome back",
        "WCW": "Woman crush Wednesday",
        "ASAP": "As soon as possible",
        "CYA": "See you",
        "DOB": "Date of birth",
        "FAQ": "Frequently asked questions",
        "NP": "No problem",
        "ROFLMAO": "Rolling on the floor laughing my ass off",
        "STFU": "Shut the fuck up",
        "TTFN": "Ta ta for now",
        "ATM": "At the moment",
        "BFFL": "Best friends for life",
        "GTG": "Got to go",
        "ILYSM": "I love you so much",
        "IKR": "I know right",
        "L8R": "Later",
        "THX": "Thanks",
        "TY": "Thank you"
        }

    # uses regex to replace whole words only
    # thanks chatgpt again
    pattern = re.compile(r'\b(' + '|'.join(replacements.keys()) + r')\b')
    result = pattern.sub(lambda x: replacements[x.group()], text)
    return result

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each line
    processed_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # Skip blank lines
            replaced_line = replace_acronyms(stripped_line)
            processed_lines.append(replaced_line)
    
    # Combine all lines into a single string
    final_text = '  '.join(processed_lines)
    return final_text


def get_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
    return first_line