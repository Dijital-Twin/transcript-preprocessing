import argparse
import requests
from os.path import exists 
from utils.data import get_episode_list, convert_html_script_to_json, extract_dialogues
import json

def download(urls, start=0, end=-1):
    exists_count = 0
    downloaded_count = 0
    error_count = 0
    if end == None:
        end = len(urls) - 1
    
    print(f"Downloading between {start} and {end}")
    for i in range(start, end+1):
        filename = f'./data/website_data/friends_{i}.html'
        if exists(filename):
            exists_count = exists_count + 1
            continue
        url = urls[i]
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
                downloaded_count = downloaded_count + 1
        else:
            print(f"Failed to fetch {url}")
            error_count = error_count + 1
        
    print(f"Downloading completed: {downloaded_count} downloaded, {exists_count} already exist, {error_count} error.")

def preprocess(urls, start=0, end=1):
    not_exists_count = 0
    preprocessed_count = 0
    all_scripts = []

    if end == None:
        end = len(urls) - 1

    print(f"Preprocessing between {start} and {end}")

    for i in range(start, end+1):
        url = urls[i]
        filename = f'./data/website_data/friends_{i}.html'
        if not exists(filename):
            not_exists_count = not_exists_count + 1
            continue
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            transcripts = convert_html_script_to_json(content)
            all_scripts.append(transcripts)
            preprocessed_count = preprocessed_count + 1
    
    with open(f'./data/transcripts/friends-{start}-{end}.json', 'w', encoding='utf-8') as f:
        json.dump(all_scripts, f, ensure_ascii=False, indent=4)

def create_pair(speaker_name, filename):
    transcripts = None

    with open(f"./data/transcripts/{filename}", 'r', encoding='utf-8') as file:
        transcripts = json.load(file)
    
    matched_dialogues = []
    for transcript in transcripts:
        for i in range(1, len(transcript)):
            if transcript[i]['speaker'] == speaker_name and transcript[i-1]['speaker'] != speaker_name:
                question = transcript[i-1]['dialogue']
                answer = transcript[i]['dialogue']
                matched_dialogue = {'question' : question, 'answer' : answer}
                matched_dialogues.append(matched_dialogue)
    
    with open(f'./data/transcripts/{filename}-{speaker_name}-pair.json', 'w', encoding='utf-8') as f:
        json.dump(matched_dialogues, f, ensure_ascii=False, indent=4)    

def main():
    parser = argparse.ArgumentParser(description="How I Met Your Mother Transcript Preprocessing.")
    parser.add_argument("--download", action="store_true", help="Download all transcripts.")
    parser.add_argument("--start", type=int, help="Start episode.")
    parser.add_argument("--end", type=int, help="End episode.")
    parser.add_argument("--preprocess", action="store_true", help="Preprocess all transcripts.")
    parser.add_argument("--create_pair", action="store_true", help="Create pair for a speaker transcripts.")
    parser.add_argument("--speaker", type=str, help="Speaker.")
    parser.add_argument("--filename", type=str, help="Transcript filename")
    args = parser.parse_args()

    if args.download:
        urls = get_episode_list('./data/episodes/friends.txt', 'https://edersoncorbari.github.io/')
        download(urls=urls, start=args.start, end=args.end)
    if args.preprocess:
        urls = get_episode_list('./data/episodes/friends.txt', 'https://edersoncorbari.github.io/')
        preprocess(urls=urls, start=args.start, end=args.end)
    if args.create_pair:
        create_pair(speaker_name=args.speaker, filename=args.filename)

if __name__ == "__main__":
    main()
