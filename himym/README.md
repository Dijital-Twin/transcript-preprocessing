# HIMYM Data Preprocessing

## Data Fetching

Our main data source for HIMYM is https://scriptmochi.com/tv-series/how-i-met-your-mother. In this code we fetch html content and parse it correctly.

To download all episodes

```bash
python3 main.py --download --start 1
```

To preprocess all downloaded episodes

```bash
python3 main.py --preprocess --start 1
```
