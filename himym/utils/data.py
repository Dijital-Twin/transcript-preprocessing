from bs4 import BeautifulSoup
import re

def get_episode_list(file_path, prefix):
    episode_list = []

    with open(file_path, 'r') as file:
        for line in file:
            episode_list.append(f"{prefix}{line.strip()}")
    return episode_list

def extract_content_div(html_content):
    """Extracts the content div and returns its text with <br> tags preserved."""
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', class_='content')
    if content_div:
        return '\n'.join(segment for segment in content_div.stripped_strings)
    return "No Div found"

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