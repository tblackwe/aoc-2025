#!/usr/bin/env python3
"""
Download Advent of Code 2025 Day 8 input using session cookie.
"""

import urllib.request
from pathlib import Path

# Read session cookie
session_file = Path.home() / '.adventofcode.session'
session_cookie = session_file.read_text().strip()

# Download input
url = 'https://adventofcode.com/2025/day/8/input'
req = urllib.request.Request(url)
req.add_header('Cookie', f'session={session_cookie}')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req) as response:
        input_data = response.read().decode('utf-8')
    
    # Save to input.txt
    output_file = Path(__file__).parent / 'input.txt'
    output_file.write_text(input_data)
    print(f"✅ Downloaded input to {output_file}")
    print(f"   Input size: {len(input_data)} bytes")
    print(f"   Number of lines: {len(input_data.strip().split(chr(10)))}")
    
except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error {e.code}: {e.reason}")
    print("   Make sure your session cookie is valid and Day 8 is unlocked.")
except Exception as e:
    print(f"❌ Error: {e}")
