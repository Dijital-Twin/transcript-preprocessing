import argparse
import requests
from os.path import exists 
from utils.data import get_episode_list, extract_content_div, extract_dialogues
import json

def download(urls, start=0, end=-1):
    exists_count = 0
    downloaded_count = 0
    error_count = 0
    if end == None:
        end = len(urls) - 1
    
    print(f"Downloading between {start} and {end}")
    for i in range(start, end+1):
        filename = f'./data/website_data/himym_{i}.html'
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
        filename = f'./data/website_data/himym_{i}.html'
        if not exists(filename):
            not_exists_count = not_exists_count + 1
            continue
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            div_content = extract_content_div(content)
            transcripts = extract_dialogues(div_content)
            all_scripts.append({'episode': i, 'url': url, 'dialogues': transcripts})
            preprocessed_count = preprocessed_count + 1
    
    with open(f'./data/transcripts/himym-{start}-{end}.json', 'w', encoding='utf-8') as f:
        json.dump(all_scripts, f, ensure_ascii=False, indent=4)

        

def main():
    parser = argparse.ArgumentParser(description="How I Met Your Mother Transcript Preprocessing.")
    parser.add_argument("--download", action="store_true", help="Download all transcripts.")
    parser.add_argument("--start", type=int, help="Start episode.")
    parser.add_argument("--end", type=int, help="End episode.")
    parser.add_argument("--preprocess", action="store_true", help="Preprocess all transcripts.")

    args = parser.parse_args()

    if args.download:
        urls = get_episode_list('./data/episodes/himym.txt', 'https://scriptmochi.com')
        download(urls=urls, start=args.start, end=args.end)
    if args.preprocess:
        urls = get_episode_list('./data/episodes/himym.txt', 'https://scriptmochi.com')
        preprocess(urls=urls, start=args.start, end=args.end)

if __name__ == "__main__":
    main()
