# Fetching Puzzle Input

The actual puzzle input needs to be downloaded from Advent of Code using your session cookie.

## Setup: Get Your Session Cookie

1. Log into https://adventofcode.com
2. Open browser developer tools (F12)
3. Go to Application/Storage → Cookies → https://adventofcode.com
4. Copy the value of the `session` cookie
5. Save it to `~/.adventofcode.session`:

```bash
echo "your_session_cookie_here" > ~/.adventofcode.session
```

## Option 1: Using the Python script (Recommended)

```bash
# From the repository root
python3 fetch_input.py <day>

# Example: Fetch input for day 8
python3 fetch_input.py 8
```

## Option 2: Using the shell script

```bash
# From the repository root
chmod +x fetch_input.sh
./fetch_input.sh <day>

# Example: Fetch input for day 8
./fetch_input.sh 8
```

## Option 3: Manual download with curl

```bash
DAY=8  # Change this to the day you want
curl -H "Cookie: session=$(cat ~/.adventofcode.session)" \
     -H "User-Agent: Mozilla/5.0" \
     https://adventofcode.com/2025/day/${DAY}/input \
     -o solutions/day-$(printf "%02d" ${DAY})/input.txt
```

## Option 4: Manual browser download

1. Go to https://adventofcode.com/2025/day/X/input (replace X with day number)
2. Save the page as `input.txt` in the `solutions/day-XX/` directory

## Verification

After downloading, verify the input:

```bash
DAY=08  # Change this to the day you want

# Check file exists and has content
ls -lh solutions/day-${DAY}/input.txt

# Count lines
wc -l solutions/day-${DAY}/input.txt

# Preview first few lines
head solutions/day-${DAY}/input.txt
```

## Security Note

**Never commit your `input.txt` files or session cookie to git!**

The `.gitignore` file is configured to exclude:
- `input.txt` files in all solution directories
- The `~/.adventofcode.session` file is outside the repository

## Troubleshooting

### "HTTP Error 400: Bad Request"
- Your session cookie may have expired
- Get a fresh session cookie by logging into AoC again

### "HTTP Error 404: Not Found"  
- The puzzle for that day may not be unlocked yet
- Check that the day number is correct (1-25)

### "Session cookie file not found"
- Create the file: `echo "your_cookie" > ~/.adventofcode.session`
- Make sure you're using the correct path

### Input downloads but is empty or shows an error
- You may not have access to that day's puzzle yet
- The puzzle unlocks at midnight EST (UTC-5)
