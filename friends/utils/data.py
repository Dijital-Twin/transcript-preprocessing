from bs4 import BeautifulSoup
import re
import json 
def get_episode_list(file_path, prefix):
    episode_list = []

    with open(file_path, 'r') as file:
        for line in file:
            episode_list.append(f"{prefix}{line.strip()}")
    return episode_list

def convert_html_script_to_json(html_content, episode_number):
    bad_html_elements = ['<b>', '</b>', '<strong>', '</strong>', '<blockquote>', '</blockquote>', '<em>', '</em>']
    for element in bad_html_elements:
        html_content = html_content.replace(element, '')
    

    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')

    dialogue_list = []
    for p in paragraphs:
        if ':' in p.text:
            speaker, dialogue = p.text.split(':', 1)
            speaker = clean_pharanteses(speaker)
            dialogue = clean_pharanteses(dialogue)
            if not check_unsuitable_speaker_names(speaker) or len(dialogue.strip()) < 1 or len(speaker.strip()) < 1:
                continue
            dialogue_list.append({"speaker": speaker.strip(), "dialogue": dialogue.strip()})
    return {"episode": episode_number, "dialogues": dialogue_list}

def check_unsuitable_speaker_names(text):
    unsuitable_speaker_names = ["written by", "transcribed by", "directed by", "story by", "teleplay by", "["]
    
    for name in unsuitable_speaker_names :
        if name in text.lower():
            return False
    return True
def clean_pharanteses(text):
    text = re.sub(r"\([^)]*\)", "", text)  # Remove parentheses
    text = re.sub(r"\[[^\]]*\]", "", text)  # Remove square brackets
    text = re.sub(r"\{[^}]*\}", "", text)  # Remove curly braces
    return text

def extract_dialogues(script):
    """Extracts and returns dialogues and speakers from the script."""
    lines_temp = script.split('\n')
    lines = []
    # Merge lines that start with ':' to the previous line
    previous_line = ""
    for line in lines_temp:
        if line.startswith(":"):
            line = previous_line + line
        else:
            lines.append(previous_line)
        previous_line = line
    lines.append(previous_line)

    dialogues = []
    for line in lines:
        # Finding dialogue and speaker where line follows 'Speaker: Dialogue' format
        match = re.match(r"^(.*?):\s*(.*)", line)
        if match:
            speaker, dialogue = match.groups()
            dialogue = clean_pharanteses(dialogue)  # Remove parenthetical remarks
            dialogues.append({"speaker": speaker.strip(), "dialogue": dialogue.strip()})
    return dialogues