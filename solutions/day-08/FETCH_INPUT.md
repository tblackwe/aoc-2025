# Fetching Puzzle Input for Day 08

The actual puzzle input needs to be downloaded from Advent of Code using your session cookie.

## Option 1: Using the shell script (Recommended)

```bash
cd solutions/day-08
chmod +x fetch_input.sh
./fetch_input.sh
```

## Option 2: Using the Python script

```bash
cd solutions/day-08
python3 download_input.py
```

## Option 3: Manual download with curl

```bash
cd solutions/day-08
curl -H "Cookie: session=$(cat ~/.adventofcode.session)" \
     -H "User-Agent: Mozilla/5.0" \
     https://adventofcode.com/2025/day/8/input \
     -o input.txt
```

## Option 4: Manual browser download

1. Go to https://adventofcode.com/2025/day/8/input
2. Save the page as `input.txt` in the `solutions/day-08/` directory

## Verification

After downloading, verify the input:

```bash
# Check file exists and has content
ls -lh solutions/day-08/input.txt

# Count lines (should be the number of junction boxes)
wc -l solutions/day-08/input.txt

# Preview first few lines
head solutions/day-08/input.txt
```

Expected format: Each line should be three comma-separated integers (X,Y,Z coordinates).

Example:
```
162,817,812
57,618,57
906,360,560
...
```
