#!/usr/bin/env python3
"""
Download Advent of Code 2025 input using session cookie.

Usage:
    python3 fetch_input.py <day>
    
Example:
    python3 fetch_input.py 8
"""

import sys
import urllib.request
from pathlib import Path

def fetch_input(day: int):
    """Download input for the specified day."""
    # Read session cookie
    session_file = Path.home() / '.adventofcode.session'
    if not session_file.exists():
        print(f"❌ Session cookie file not found: {session_file}")
        print("   Create this file with your AoC session cookie.")
        return False
    
    session_cookie = session_file.read_text().strip()
    
    # Download input
    url = f'https://adventofcode.com/2025/day/{day}/input'
    req = urllib.request.Request(url)
    req.add_header('Cookie', f'session={session_cookie}')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
    
    try:
        with urllib.request.urlopen(req) as response:
            input_data = response.read().decode('utf-8')
        
        # Save to input.txt in the day's directory
        output_dir = Path(__file__).parent / 'solutions' / f'day-{day:02d}'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'input.txt'
        output_file.write_text(input_data)
        
        print(f"✅ Downloaded input to {output_file}")
        print(f"   Input size: {len(input_data)} bytes")
        print(f"   Number of lines: {len(input_data.strip().split(chr(10)))}")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"   Make sure your session cookie is valid and Day {day} is unlocked.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 fetch_input.py <day>")
        print("Example: python3 fetch_input.py 8")
        sys.exit(1)
    
    try:
        day = int(sys.argv[1])
        if day < 1 or day > 25:
            print("❌ Day must be between 1 and 25")
            sys.exit(1)
        
        success = fetch_input(day)
        sys.exit(0 if success else 1)
        
    except ValueError:
        print("❌ Day must be a number")
        sys.exit(1)
