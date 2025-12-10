#!/usr/bin/env python3
"""
Multi-Model Architect Runner

Runs the architect agent with multiple AI models to generate and compare
puzzle specifications.

Usage:
    python run-multi-model-architect.py <puzzle_url_or_text> --day <day_number>
    
Example:
    python run-multi-model-architect.py "https://adventofcode.com/2025/day/5" --day 5
    python run-multi-model-architect.py puzzle.txt --day 5 --models gpt-4o,claude-3.5-sonnet
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

import yaml


class MultiModelArchitect:
    """Runs architect agent with multiple models and compares results."""
    
    def __init__(self, config_path: str = ".opencode/multi-model-architect.yaml"):
        """Initialize with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.results: Dict[str, Dict[str, Any]] = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            print(f"❌ Config file not found: {self.config_path}")
            sys.exit(1)
            
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def _get_enabled_models(self, filter_models: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Get list of enabled models, optionally filtered."""
        models = [m for m in self.config['models'] if m.get('enabled', True)]
        
        if filter_models:
            models = [m for m in models if m['name'] in filter_models]
            
        return models
    
    def _read_puzzle_input(self, puzzle_source: str) -> str:
        """Read puzzle from file or URL."""
        if puzzle_source.startswith('http'):
            print(f"📥 Fetching puzzle from URL: {puzzle_source}")
            # For now, user should provide the text
            print("⚠️  URL fetching not implemented yet. Please provide puzzle text file.")
            sys.exit(1)
        
        puzzle_path = Path(puzzle_source)
        if not puzzle_path.exists():
            print(f"❌ Puzzle file not found: {puzzle_source}")
            sys.exit(1)
            
        return puzzle_path.read_text()
    
    def _get_architect_prompt(self) -> str:
        """Load architect agent prompt."""
        prompt_path = Path(self.config['agent']['prompt_file'])
        if not prompt_path.exists():
            print(f"❌ Architect prompt not found: {prompt_path}")
            sys.exit(1)
            
        return prompt_path.read_text()
    
    def _create_output_directory(self, day: int) -> Path:
        """Create output directory for multi-model comparison."""
        output_dir = Path(self.config['output']['directory'])
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def _get_output_filename(self, day: int, model_name: str) -> str:
        """Generate output filename for a model's spec."""
        model_slug = model_name.replace('.', '-').replace('_', '-').lower()
        pattern = self.config['output']['naming_pattern']
        return pattern.format(day=f"{day:02d}", model_slug=model_slug)
    
    async def _run_architect_with_model(
        self, 
        model: Dict[str, str], 
        puzzle_text: str, 
        day: int
    ) -> Dict[str, Any]:
        """Run architect agent with a specific model."""
        model_name = model['name']
        display_name = model['display_name']
        
        print(f"\n🤖 Running architect with {display_name}...")
        print(f"   Model: {model_name}")
        print(f"   Provider: {model['provider']}")
        
        # Create the prompt for the architect
        architect_prompt = self._get_architect_prompt()
        
        task_prompt = f"""
{architect_prompt}

---

# TASK

Analyze the following Advent of Code puzzle and create a comprehensive specification.

## Puzzle Text

{puzzle_text}

## Your Task

Create a detailed specification in the format described above. Include:
1. Problem description and core mechanics
2. Input/output format specifications
3. Algorithm analysis (2-3 approaches minimum)
4. Data structure recommendations
5. Comprehensive test plan
6. Implementation guidance

Generate the complete spec following the template structure.
"""

        # NOTE: This is a placeholder for actual model invocation
        # In a real implementation, you would call the OpenCode Task tool here
        # with the specific model configuration
        
        print(f"⏳ Generating spec... (this may take 30-60 seconds)")
        
        # Placeholder result
        result = {
            'model': model_name,
            'display_name': display_name,
            'status': 'pending',
            'spec': None,
            'timestamp': datetime.now().isoformat(),
            'error': None
        }
        
        # TODO: Call OpenCode task tool with model configuration
        # This would be done through the task tool with parameters like:
        # task(
        #     description=f"Generate spec with {model_name}",
        #     prompt=task_prompt,
        #     subagent_type="architect",
        #     model=model_name  # Model selection parameter
        # )
        
        print(f"⚠️  Model invocation not yet implemented")
        print(f"   To implement: Use OpenCode Task tool with model parameter")
        
        return result
    
    async def run_all_models(
        self, 
        puzzle_source: str, 
        day: int,
        filter_models: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Run architect agent with all enabled models."""
        print(f"\n{'='*60}")
        print(f"Multi-Model Architect Runner - Day {day}")
        print(f"{'='*60}")
        
        # Read puzzle input
        puzzle_text = self._read_puzzle_input(puzzle_source)
        print(f"✓ Loaded puzzle ({len(puzzle_text)} characters)")
        
        # Get enabled models
        models = self._get_enabled_models(filter_models)
        print(f"✓ Found {len(models)} enabled models")
        
        # Create output directory
        output_dir = self._create_output_directory(day)
        print(f"✓ Output directory: {output_dir}")
        
        # Run architect with each model
        for model in models:
            result = await self._run_architect_with_model(model, puzzle_text, day)
            self.results[model['name']] = result
            
            # Save spec if generated
            if result['spec']:
                output_file = output_dir / self._get_output_filename(day, model['name'])
                output_file.write_text(result['spec'])
                print(f"✓ Saved spec to {output_file}")
        
        return self.results
    
    def generate_comparison_report(self, day: int) -> str:
        """Generate comparison report of all model outputs."""
        if not self.results:
            return "No results to compare"
        
        report_lines = [
            f"# Multi-Model Architect Comparison - Day {day:02d}",
            f"",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Models Tested",
            f""
        ]
        
        for model_name, result in self.results.items():
            report_lines.append(f"- **{result['display_name']}**")
            report_lines.append(f"  - Model: `{model_name}`")
            report_lines.append(f"  - Status: {result['status']}")
            report_lines.append(f"  - Timestamp: {result['timestamp']}")
            if result['error']:
                report_lines.append(f"  - Error: {result['error']}")
            report_lines.append("")
        
        report_lines.extend([
            "## Comparison Metrics",
            "",
            "### Completeness",
            "How well did each model cover all required sections?",
            "",
            "| Model | Problem Desc | Algorithm Analysis | Test Plan | Implementation Guide | Score |",
            "|-------|--------------|-------------------|-----------|---------------------|-------|",
            "| TBD   | -            | -                 | -         | -                   | -     |",
            "",
            "### Detail Level",
            "How detailed and thorough were the specifications?",
            "",
            "| Model | Depth | Examples | Complexity Analysis | Edge Cases |",
            "|-------|-------|----------|-------------------|------------|",
            "| TBD   | -     | -        | -                 | -          |",
            "",
            "## Recommendations",
            "",
            "Based on this comparison:",
            "- **Best Overall**: TBD",
            "- **Most Detailed**: TBD", 
            "- **Best Algorithm Analysis**: TBD",
            "- **Best Test Coverage**: TBD",
            "",
            "## Next Steps",
            "",
            "1. Review each model's spec manually",
            "2. Choose the best spec or merge insights from multiple specs",
            "3. Use the chosen spec for implementation with @aoc-helper",
            ""
        ])
        
        return "\n".join(report_lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run architect agent with multiple models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s puzzle.txt --day 5
  %(prog)s puzzle.txt --day 5 --models gpt-4o,claude-3.5-sonnet
  %(prog)s puzzle.txt --day 5 --no-report
        """
    )
    
    parser.add_argument(
        'puzzle_source',
        help='Path to puzzle text file or URL'
    )
    
    parser.add_argument(
        '--day', '-d',
        type=int,
        required=True,
        help='Day number (1-25)'
    )
    
    parser.add_argument(
        '--models', '-m',
        help='Comma-separated list of model names to test (default: all enabled)'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip generating comparison report'
    )
    
    parser.add_argument(
        '--config', '-c',
        default='.opencode/multi-model-architect.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    # Parse models filter
    filter_models = None
    if args.models:
        filter_models = [m.strip() for m in args.models.split(',')]
    
    # Run multi-model architect
    runner = MultiModelArchitect(args.config)
    
    try:
        results = asyncio.run(
            runner.run_all_models(args.puzzle_source, args.day, filter_models)
        )
        
        # Generate comparison report
        if not args.no_report:
            print(f"\n📊 Generating comparison report...")
            report = runner.generate_comparison_report(args.day)
            
            report_dir = Path(runner.config['output']['directory'])
            report_file = report_dir / f"comparison-day-{args.day:02d}.md"
            report_file.write_text(report)
            print(f"✓ Report saved to {report_file}")
        
        print(f"\n✅ Multi-model architect run complete!")
        print(f"\nResults:")
        for model_name, result in results.items():
            status_icon = "✓" if result['status'] == 'success' else "⚠️"
            print(f"  {status_icon} {result['display_name']}: {result['status']}")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
