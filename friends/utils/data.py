from bs4 import BeautifulSoup
import re
import json 
def get_episode_list(file_path, prefix):
    episode_list = []

    with open(file_path, 'r') as file:
        for line in file:
            episode_list.append(f"{prefix}{line.strip()}")
    return episode_list

def convert_html_script_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')

    dialogue_list = []
    for p in paragraphs:
        if ':' in p.text:
            speaker, dialogue = p.text.split(':', 1)
            speaker = speaker.strip()
            dialogue = dialogue.strip()
            dialogue_list.append({"speaker": speaker, "dialogue": dialogue})

    return dialogue_list

def clean_dialogue(dialogue):
    """Removes parenthetical remarks from dialogue."""
    return re.sub(r"\([^)]*\)", "", dialogue)

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
            dialogue = clean_dialogue(dialogue)  # Remove parenthetical remarks
            dialogues.append({"speaker": speaker.strip(), "dialogue": dialogue.strip()})
    return dialogues