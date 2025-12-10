#!/usr/bin/env python3
"""
Agentic Workflow for Advent of Code Solutions

This script orchestrates the complete TDD workflow:
1. Architect - Fetches puzzle and creates spec
2. SDET - Reviews spec and creates comprehensive tests
3. Implementer - Implements solution to make tests pass

Usage:
    ./solve-day.py <day> <model>
    
Examples:
    ./solve-day.py 5 gpt-4o
    ./solve-day.py 12 claude-3.5-sonnet
    ./solve-day.py 25 gemini-2.0-flash
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class AoCWorkflow:
    """Orchestrates the TDD workflow for solving AoC puzzles."""
    
    # Supported models from GitHub Copilot and OpenCode Zen
    # https://docs.github.com/en/copilot/reference/ai-models/supported-models
    SUPPORTED_MODELS = {
        # OpenAI models
        'gpt-4.1': 'GPT-4.1',
        'gpt-4o': 'GPT-4o (legacy)',
        'gpt-5': 'GPT-5',
        'gpt-5-mini': 'GPT-5 mini',
        'gpt-5-codex': 'GPT-5-Codex',
        'gpt-5.1': 'GPT-5.1',
        'gpt-5.1-codex': 'GPT-5.1-Codex',
        'gpt-5.1-codex-mini': 'GPT-5.1-Codex-Mini',
        'gpt-5.1-codex-max': 'GPT-5.1-Codex-Max',
        # Anthropic models
        'claude-haiku-4.5': 'Claude Haiku 4.5',
        'claude-opus-4.1': 'Claude Opus 4.1',
        'claude-opus-4.5': 'Claude Opus 4.5',
        'claude-sonnet-4': 'Claude Sonnet 4',
        'claude-sonnet-4.5': 'Claude Sonnet 4.5',
        # Google models
        'gemini-2.5-pro': 'Gemini 2.5 Pro',
        'gemini-3-pro': 'Gemini 3 Pro',
        # xAI models
        'grok-code-fast-1': 'Grok Code Fast 1',
        # Fine-tuned models
        'raptor-mini': 'Raptor mini',
        # OpenCode Zen models
        'big-pickle': 'Big Pickle (OpenCode Zen)',
    }
    
    def __init__(self, day: int, model: str, year: int = 2025):
        self.day = day
        self.day_str = f"{day:02d}"
        self.model = model
        self.year = year
        self.puzzle_url = f"https://adventofcode.com/{year}/day/{day}"
        self.input_url = f"{self.puzzle_url}/input"
        self.branch_name = f"day-{self.day_str}"
        
        # File paths
        self.spec_file = Path(f"specs/day-{self.day_str}.md")
        self.solution_dir = Path(f"solutions/day-{self.day_str}")
        self.solution_file = self.solution_dir / "solution.py"
        self.test_file = self.solution_dir / "test_solution.py"
        self.input_file = self.solution_dir / "input.txt"
        
        # Track workflow state
        self.start_time = datetime.now()
        self.results = {
            'day': day,
            'model': model,
            'stages': {},
            'branch': self.branch_name
        }
    
    def print_header(self, text: str):
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{text:^70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
    
    def print_step(self, step: str, status: str = "info"):
        """Print a formatted step message."""
        icons = {
            'info': '🔵',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'running': '⏳'
        }
        colors = {
            'info': Colors.CYAN,
            'success': Colors.GREEN,
            'error': Colors.RED,
            'warning': Colors.YELLOW,
            'running': Colors.BLUE
        }
        icon = icons.get(status, '•')
        color = colors.get(status, '')
        print(f"{color}{icon} {step}{Colors.ENDC}")
    
    def run_command(self, cmd: list[str], description: str) -> tuple[bool, str]:
        """Run a shell command and return success status and output."""
        self.print_step(f"{description}...", "running")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def create_git_branch(self) -> bool:
        """Create a new Git branch for this day."""
        self.print_step(f"Creating Git branch: {self.branch_name}", "info")
        
        # Check if we're in a git repo
        success, _ = self.run_command(['git', 'rev-parse', '--git-dir'], "Checking Git repository")
        if not success:
            self.print_step("Not in a Git repository - skipping branch creation", "warning")
            return False
        
        # Check current branch
        success, current_branch = self.run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], "Getting current branch")
        if success:
            current_branch = current_branch.strip()
            self.print_step(f"Current branch: {current_branch}", "info")
        
        # Check if branch already exists
        success, _ = self.run_command(['git', 'rev-parse', '--verify', self.branch_name], "Checking if branch exists")
        if success:
            self.print_step(f"Branch {self.branch_name} already exists - checking out", "warning")
            success, _ = self.run_command(['git', 'checkout', self.branch_name], f"Checking out {self.branch_name}")
            return success
        
        # Create new branch
        success, _ = self.run_command(['git', 'checkout', '-b', self.branch_name], f"Creating branch {self.branch_name}")
        if success:
            self.print_step(f"Created and checked out branch: {self.branch_name}", "success")
            self.results['branch_created'] = True
            return True
        else:
            self.print_step("Failed to create branch", "error")
            return False
    
    def create_directory_structure(self):
        """Create the directory structure for the day."""
        self.print_step(f"Creating directory structure for day {self.day}", "info")
        
        # Create specs directory if it doesn't exist
        Path("specs").mkdir(exist_ok=True)
        
        # Create solution directory
        if self.solution_dir.exists():
            self.print_step(f"Solution directory already exists: {self.solution_dir}", "warning")
        else:
            self.solution_dir.mkdir(parents=True, exist_ok=True)
            self.print_step(f"Created solution directory: {self.solution_dir}", "success")
    
    def fetch_puzzle_input(self) -> bool:
        """Fetch puzzle input using session cookie."""
        self.print_step("Fetching puzzle input", "info")
        
        # Check for session cookie
        session_file = Path.home() / ".adventofcode.session"
        if not session_file.exists():
            self.print_step(
                f"Session file not found: {session_file}\n"
                "  Create this file with your AoC session cookie to auto-fetch input.",
                "warning"
            )
            return False
        
        session_cookie = session_file.read_text().strip()
        
        # Fetch input using curl
        success, output = self.run_command(
            [
                'curl',
                '-s',
                '-b', f'session={session_cookie}',
                self.input_url
            ],
            f"Fetching input from {self.input_url}"
        )
        
        if success and output and not output.startswith('Puzzle inputs differ by user'):
            self.input_file.write_text(output)
            self.print_step(f"Saved input to {self.input_file}", "success")
            return True
        else:
            self.print_step("Failed to fetch input - you'll need to download manually", "warning")
            return False
    
    def stage_architect(self) -> bool:
        """Stage 1: Architect creates the specification."""
        stage_start = time.time()
        self.print_header(f"STAGE 1: ARCHITECT - Creating Spec for Day {self.day}")
        
        self.print_step(f"Puzzle URL: {self.puzzle_url}", "info")
        self.print_step(f"Using model: {self.model}", "info")
        
        # Create prompt for architect
        architect_prompt = f"""
Fetch and analyze the Advent of Code puzzle for day {self.day} of {self.year}.

Puzzle URL: {self.puzzle_url}

Your tasks:
1. Fetch the puzzle description from {self.puzzle_url}
2. Analyze the problem thoroughly following your architect guidelines
3. Create a comprehensive specification in specs/day-{self.day_str}.md

The spec should include:
- Clear problem description with examples
- Input/output format specifications  
- Algorithm analysis (2-3 approaches minimum)
- Data structure recommendations
- Comprehensive test plan with test cases
- Implementation guidance and gotchas

Be thorough and precise. The SDET and Implementer will rely on your spec.
"""
        
        self.print_step("Invoking architect agent", "running")
        self.print_step(f"Output: {self.spec_file}", "info")
        
        # Note: This is where we would call the OpenCode Task tool
        # For now, we'll provide instructions for manual invocation
        print(f"\n{Colors.YELLOW}Manual Step Required:{Colors.ENDC}")
        print(f"Run this command in OpenCode:")
        print(f"{Colors.CYAN}@architect {architect_prompt}{Colors.ENDC}\n")
        
        # Wait for user confirmation
        response = input(f"{Colors.BOLD}Press Enter when architect has created the spec (or 'skip' to continue): {Colors.ENDC}")
        
        if response.lower() == 'skip':
            self.print_step("Skipping architect stage", "warning")
            self.results['stages']['architect'] = {'status': 'skipped'}
            return True
        
        # Verify spec was created
        if self.spec_file.exists():
            spec_size = self.spec_file.stat().st_size
            self.print_step(f"Spec created: {self.spec_file} ({spec_size} bytes)", "success")
            
            stage_duration = time.time() - stage_start
            self.results['stages']['architect'] = {
                'status': 'success',
                'duration': stage_duration,
                'output': str(self.spec_file)
            }
            return True
        else:
            self.print_step(f"Spec file not found: {self.spec_file}", "error")
            self.results['stages']['architect'] = {'status': 'failed'}
            return False
    
    def stage_sdet(self) -> bool:
        """Stage 2: SDET creates comprehensive tests."""
        stage_start = time.time()
        self.print_header(f"STAGE 2: SDET - Creating Tests for Day {self.day}")
        
        if not self.spec_file.exists():
            self.print_step(f"Spec file not found: {self.spec_file}", "error")
            self.print_step("Cannot proceed without spec. Run architect first.", "error")
            return False
        
        self.print_step(f"Reading spec: {self.spec_file}", "info")
        self.print_step(f"Using model: {self.model}", "info")
        
        sdet_prompt = f"""
Review the specification for day {self.day} and create comprehensive unit tests.

Spec file: specs/day-{self.day_str}.md

Your tasks:
1. Read and analyze the spec file thoroughly
2. Extract all example test cases with expected outputs
3. Identify edge cases and boundary conditions
4. Create comprehensive test suite in solutions/day-{self.day_str}/test_solution.py

The test file should include:
- Tests for parsing logic
- Tests for Part 1 with example inputs (exact expected values from spec)
- Tests for Part 2 (when available)
- Edge case tests (empty input, single element, boundaries, etc.)
- Clear test names and docstrings

Follow TDD principles - tests should fail initially (no implementation yet).
After creating tests, run them to verify they fail appropriately.

Remember: You're creating tests BEFORE the implementation exists!
"""
        
        self.print_step("Invoking SDET agent", "running")
        self.print_step(f"Output: {self.test_file}", "info")
        
        print(f"\n{Colors.YELLOW}Manual Step Required:{Colors.ENDC}")
        print(f"Run this command in OpenCode:")
        print(f"{Colors.CYAN}@sdet {sdet_prompt}{Colors.ENDC}\n")
        
        response = input(f"{Colors.BOLD}Press Enter when SDET has created tests (or 'skip' to continue): {Colors.ENDC}")
        
        if response.lower() == 'skip':
            self.print_step("Skipping SDET stage", "warning")
            self.results['stages']['sdet'] = {'status': 'skipped'}
            return True
        
        # Verify tests were created
        if self.test_file.exists():
            test_size = self.test_file.stat().st_size
            self.print_step(f"Tests created: {self.test_file} ({test_size} bytes)", "success")
            
            # Try to run tests (they should fail)
            self.print_step("Running tests (expecting failures - no implementation yet)", "info")
            success, output = self.run_command(
                ['python3', '-m', 'unittest', str(self.test_file)],
                "Running test suite"
            )
            
            if not success:
                self.print_step("Tests fail as expected (no implementation yet) ✓", "success")
            else:
                self.print_step("Warning: Tests passed, but no implementation exists yet", "warning")
            
            stage_duration = time.time() - stage_start
            self.results['stages']['sdet'] = {
                'status': 'success',
                'duration': stage_duration,
                'output': str(self.test_file)
            }
            return True
        else:
            self.print_step(f"Test file not found: {self.test_file}", "error")
            self.results['stages']['sdet'] = {'status': 'failed'}
            return False
    
    def stage_implementer(self) -> bool:
        """Stage 3: Implementer creates the solution."""
        stage_start = time.time()
        self.print_header(f"STAGE 3: IMPLEMENTER - Implementing Part 1 for Day {self.day}")
        
        if not self.spec_file.exists():
            self.print_step(f"Spec file not found: {self.spec_file}", "error")
            return False
        
        if not self.test_file.exists():
            self.print_step(f"Test file not found: {self.test_file}", "error")
            self.print_step("Warning: Proceeding without tests (not recommended)", "warning")
        
        self.print_step(f"Reading spec: {self.spec_file}", "info")
        self.print_step(f"Reading tests: {self.test_file}", "info")
        self.print_step(f"Using model: {self.model}", "info")
        
        implementer_prompt = f"""
Implement the solution for day {self.day} Part 1 following TDD principles.

Files to review:
- Spec: specs/day-{self.day_str}.md
- Tests: solutions/day-{self.day_str}/test_solution.py

Your tasks:
1. Read the spec to understand requirements
2. Read the test file to understand what needs to be implemented
3. Implement the solution in solutions/day-{self.day_str}/solution.py

Implementation requirements:
- Start with parse_input() function - get parsing right first!
- Implement solve_part1() to make Part 1 tests pass
- Follow the algorithm recommendations from the spec
- Use clean, readable code with good variable names
- Add comments for complex logic
- Run tests frequently as you develop
- DO NOT implement Part 2 yet - focus on Part 1 only

Follow the Red-Green-Refactor cycle:
1. Run tests (they should fail - RED)
2. Implement minimal code to pass tests - GREEN
3. Refactor to improve code quality
4. Verify all Part 1 tests pass

Your goal: Make all Part 1 tests pass!
"""
        
        self.print_step("Invoking implementer agent", "running")
        self.print_step(f"Output: {self.solution_file}", "info")
        
        print(f"\n{Colors.YELLOW}Manual Step Required:{Colors.ENDC}")
        print(f"Run this command in OpenCode:")
        print(f"{Colors.CYAN}@implementer {implementer_prompt}{Colors.ENDC}\n")
        
        response = input(f"{Colors.BOLD}Press Enter when implementer has created solution (or 'skip' to continue): {Colors.ENDC}")
        
        if response.lower() == 'skip':
            self.print_step("Skipping implementer stage", "warning")
            self.results['stages']['implementer'] = {'status': 'skipped'}
            return True
        
        # Verify solution was created
        if self.solution_file.exists():
            solution_size = self.solution_file.stat().st_size
            self.print_step(f"Solution created: {self.solution_file} ({solution_size} bytes)", "success")
            
            # Run tests to verify Part 1 passes
            if self.test_file.exists():
                self.print_step("Running tests to verify Part 1 implementation", "info")
                success, output = self.run_command(
                    ['python3', '-m', 'unittest', str(self.test_file)],
                    "Running test suite"
                )
                
                if success:
                    self.print_step("All tests pass! Part 1 implementation successful ✓", "success")
                else:
                    self.print_step("Some tests failed - review output above", "warning")
                    print(output)
            
            stage_duration = time.time() - stage_start
            self.results['stages']['implementer'] = {
                'status': 'success',
                'duration': stage_duration,
                'output': str(self.solution_file)
            }
            return True
        else:
            self.print_step(f"Solution file not found: {self.solution_file}", "error")
            self.results['stages']['implementer'] = {'status': 'failed'}
            return False
    
    def run_workflow(self):
        """Execute the complete workflow."""
        self.print_header(f"Advent of Code {self.year} - Day {self.day} - Agentic Workflow")
        
        print(f"{Colors.BOLD}Configuration:{Colors.ENDC}")
        print(f"  Day: {self.day}")
        print(f"  Model: {self.model}")
        print(f"  Puzzle URL: {self.puzzle_url}")
        print(f"  Year: {self.year}")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Optionally fetch puzzle input
        if not self.input_file.exists():
            self.fetch_puzzle_input()
        else:
            self.print_step(f"Input file already exists: {self.input_file}", "info")
        
        # Stage 1: Architect
        if not self.stage_architect():
            self.print_step("Architect stage failed - cannot continue", "error")
            return False
        
        # Stage 2: SDET
        if not self.stage_sdet():
            self.print_step("SDET stage failed - continuing anyway", "warning")
        
        # Stage 3: Implementer
        if not self.stage_implementer():
            self.print_step("Implementer stage failed", "error")
            return False
        
        # Summary
        self.print_summary()
        return True
    
    def print_summary(self):
        """Print workflow summary."""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        
        self.print_header("WORKFLOW COMPLETE")
        
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  Day: {self.day}")
        print(f"  Model: {self.model}")
        print(f"  Total Duration: {total_duration:.1f}s")
        print()
        
        print(f"{Colors.BOLD}Generated Files:{Colors.ENDC}")
        for file_path in [self.spec_file, self.test_file, self.solution_file]:
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✓ {file_path} ({size} bytes)")
            else:
                print(f"  ✗ {file_path} (not created)")
        print()
        
        # Print PR info if available
        if 'pr_url' in self.results:
            print(f"{Colors.BOLD}Pull Request:{Colors.ENDC}")
            print(f"  {self.results['pr_url']}")
            print()
        
        print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print(f"  1. Review the pull request and generated files")
        print(f"  2. Run tests: cd {self.solution_dir} && python3 -m unittest test_solution.py")
        print(f"  3. Run solution: cd {self.solution_dir} && python3 solution.py")
        print(f"  4. Submit Part 1 answer to {self.puzzle_url}")
        print(f"  5. Merge PR after verification")
        print(f"  6. After Part 2 unlocks, update spec and repeat workflow")
        print()
        
        # Save results
        results_file = Path(f".workflow-day-{self.day_str}.json")
        self.results['total_duration'] = total_duration
        self.results['completed_at'] = datetime.now().isoformat()
        results_file.write_text(json.dumps(self.results, indent=2))
        print(f"Workflow results saved to: {results_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic workflow for solving Advent of Code puzzles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 5 gpt-4o
  %(prog)s 12 claude-3.5-sonnet
  %(prog)s 25 gemini-2.0-flash

The workflow orchestrates:
  1. Creates Git branch (day-XX)
  2. Architect - Fetches puzzle and creates comprehensive spec
  3. SDET - Reviews spec and creates comprehensive tests (TDD)
  4. Implementer - Implements Part 1 solution to make tests pass
  5. Commits changes to Git
  6. Creates pull request

Supported models:
  OpenAI: gpt-4.1, gpt-5, gpt-5-mini, gpt-5-codex, gpt-5.1, gpt-5.1-codex, 
          gpt-5.1-codex-mini, gpt-5.1-codex-max
  Anthropic: claude-haiku-4.5, claude-sonnet-4, claude-sonnet-4.5,
             claude-opus-4.1, claude-opus-4.5
  Google: gemini-2.5-pro, gemini-3-pro
  xAI: grok-code-fast-1
  Fine-tuned: raptor-mini
  OpenCode Zen: big-pickle
        """
    )
    
    parser.add_argument(
        'day',
        type=int,
        help='Day number (1-25)'
    )
    
    parser.add_argument(
        'model',
        help='AI model to use (e.g., gpt-4o, claude-3.5-sonnet)'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        default=2025,
        help='Advent of Code year (default: 2025)'
    )
    
    args = parser.parse_args()
    
    # Validate day
    if not 1 <= args.day <= 25:
        print(f"Error: Day must be between 1 and 25, got {args.day}")
        sys.exit(1)
    
    # Run workflow
    workflow = AoCWorkflow(args.day, args.model, args.year)
    success = workflow.run_workflow()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
