# Friends Data Preprocessing

## Data Fetching

Our main data source for Friends is https://edersoncorbari.github.io/friends-scripts/. In this code we fetch html content and parse it correctly.

To download all episodes

```bash
python3 main.py --download --start 1
```

To preprocess all downloaded episodes

```bash
python3 main.py --preprocess --start 1
```

Create question and answer pairs for speaker

```bash
python3 main.py --create_pair --speaker Chandler --filename friends-1-227.json
```
