#!/usr/bin/env python3
"""
Quick Refactoring Analyzer - Fast version for quick estimates
"""

import os
import re
import sys
from pathlib import Path

def quick_analyze(directory):
    """Quick analysis of refactoring opportunities."""
    issues = {
        'self_as_arg': 0,
        'incorrect_self': 0,
        'func_with_self': 0,
        'files_with_issues': set()
    }
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for self.method(self, ...) pattern
            self_as_arg_matches = re.findall(r'self\.\w+\s*\(\s*self\s*(?:,|\))', content)
            if self_as_arg_matches:
                issues['self_as_arg'] += len(self_as_arg_matches)
                issues['files_with_issues'].add(file_path)
            
            # Check for incorrect self usage like self[0]
            incorrect_self_matches = re.findall(r'self\s*\[', content)
            if incorrect_self_matches:
                issues['incorrect_self'] += len(incorrect_self_matches)
                issues['files_with_issues'].add(file_path)
            
            # Check for functions with "self" parameter (not methods)
            # Look for def function_name(..., self, ...) patterns
            func_with_self_matches = re.findall(r'def\s+\w+\s*\([^)]*,\s*self\s*[,)]', content)
            if func_with_self_matches:
                issues['func_with_self'] += len(func_with_self_matches)
                issues['files_with_issues'].add(file_path)
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return issues

def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Fixed: Use string path instead of Path object concatenation
        directory = os.path.join(os.getcwd(), "osdag_core")
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
    
    print(f"Analyzing: {directory}")
    issues = quick_analyze(directory)
    
    print("\n" + "="*50)
    print("QUICK REFACTORING ANALYSIS")
    print("="*50)
    print(f"self calling itself as argument: {issues['self_as_arg']}")
    print(f"Incorrect self usage (like self[0]): {issues['incorrect_self']}")
    print(f"Functions with self parameter: {issues['func_with_self']}")
    print(f"Files with issues: {len(issues['files_with_issues'])}")
    
    if issues['files_with_issues']:
        print(f"\nFiles to check:")
        for file_path in sorted(issues['files_with_issues']):
            print(f"  {file_path}")

if __name__ == "__main__":
    main()