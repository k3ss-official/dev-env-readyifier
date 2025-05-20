#!/usr/bin/env python3
"""
file_structure_manager.py - File structure management for Dev Environment Readyifier

This script handles file structure annotation and size checking, following
David Ondrej's best practices for AI-assisted development.
"""

import os
import re
from pathlib import Path

class FileStructureManager:
    """Manages file structure annotation and size checking."""
    
    def __init__(self, repo_path):
        """Initialize the file structure manager with the path to the repository."""
        self.repo_path = Path(repo_path)
        self.code_extensions = {
            '.py': '# ',
            '.js': '// ',
            '.ts': '// ',
            '.jsx': '// ',
            '.tsx': '// ',
            '.java': '// ',
            '.c': '// ',
            '.cpp': '// ',
            '.h': '// ',
            '.hpp': '// ',
            '.css': '/* ',
            '.scss': '/* ',
            '.html': '<!-- ',
            '.xml': '<!-- ',
            '.md': '',
            '.json': '',
            '.yaml': '# ',
            '.yml': '# ',
            '.sh': '# ',
            '.bash': '# ',
            '.zsh': '# ',
            '.sql': '-- ',
        }
        self.code_extensions_end = {
            '.css': ' */',
            '.scss': ' */',
            '.html': ' -->',
            '.xml': ' -->',
        }
        self.max_line_count = 200
    
    def check_file_sizes(self):
        """Check for files exceeding the recommended line limit."""
        large_files = []
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.code_extensions:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            line_count = sum(1 for _ in f)
                            if line_count > self.max_line_count:
                                rel_path = os.path.relpath(file_path, self.repo_path)
                                large_files.append((rel_path, line_count))
                    except:
                        pass
        
        return large_files
    
    def add_file_annotations(self):
        """Add filepath and filename annotations to files that don't have them."""
        modified_files = []
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.code_extensions:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repo_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Skip if file is empty
                        if not content.strip():
                            continue
                        
                        # Check if file already has a path annotation
                        has_annotation = False
                        first_lines = content.split('\n', 5)[:5]
                        for line in first_lines:
                            if re.search(r'File:.*' + re.escape(file), line, re.IGNORECASE) or \
                               re.search(r'Path:.*' + re.escape(os.path.dirname(rel_path)), line, re.IGNORECASE) or \
                               re.search(r'filepath:.*' + re.escape(rel_path), line, re.IGNORECASE):
                                has_annotation = True
                                break
                        
                        if not has_annotation:
                            # Prepare annotation
                            comment_start = self.code_extensions[ext]
                            comment_end = self.code_extensions_end.get(ext, '')
                            
                            if ext == '.md':
                                annotation = f"# File: {rel_path}\n\n"
                            elif ext == '.json':
                                # For JSON, we'll add as a comment at the top, but need to ensure valid JSON
                                # We'll skip JSON files for now as they require special handling
                                continue
                            else:
                                annotation = f"{comment_start}File: {rel_path}{comment_end}\n\n"
                            
                            # Add annotation
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(annotation + content)
                            
                            modified_files.append(rel_path)
                    except:
                        pass
        
        return modified_files
    
    def suggest_file_splits(self):
        """Suggest how to split files that exceed the recommended line limit."""
        suggestions = []
        
        large_files = self.check_file_sizes()
        for file_path, line_count in large_files:
            full_path = os.path.join(self.repo_path, file_path)
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Analyze file content to suggest logical split points
                suggestion = self._analyze_for_split(file_path, content, line_count)
                suggestions.append(suggestion)
            except:
                pass
        
        return suggestions
    
    def _analyze_for_split(self, file_path, content, line_count):
        """Analyze file content to suggest logical split points."""
        ext = os.path.splitext(file_path)[1]
        
        # Default suggestion
        suggestion = {
            'file': file_path,
            'line_count': line_count,
            'split_suggestion': f"Consider splitting into {line_count // 200 + 1} smaller files"
        }
        
        # Python-specific analysis
        if ext == '.py':
            classes = re.findall(r'class\s+(\w+)', content)
            functions = re.findall(r'def\s+(\w+)', content)
            
            if classes:
                suggestion['split_suggestion'] = f"Consider splitting into separate files for each class: {', '.join(classes)}"
            elif len(functions) > 5:
                suggestion['split_suggestion'] = f"Consider grouping related functions into separate modules"
        
        # JavaScript/TypeScript analysis
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            components = re.findall(r'(function|class|const)\s+(\w+)', content)
            if components:
                suggestion['split_suggestion'] = f"Consider splitting into separate files for components/functions"
        
        return suggestion

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()
    
    manager = FileStructureManager(repo_path)
    
    print("Checking file sizes...")
    large_files = manager.check_file_sizes()
    if large_files:
        print("  Files exceeding 200 lines:")
        for file_path, line_count in large_files:
            print(f"  - {file_path}: {line_count} lines")
    else:
        print("  No files exceed the 200-line limit.")
    
    print("\nAdding file annotations...")
    modified_files = manager.add_file_annotations()
    if modified_files:
        print(f"  Added annotations to {len(modified_files)} files:")
        for file_path in modified_files[:5]:
            print(f"  - {file_path}")
        if len(modified_files) > 5:
            print(f"  - ... and {len(modified_files) - 5} more")
    else:
        print("  No files needed annotations.")
    
    print("\nSuggesting file splits...")
    suggestions = manager.suggest_file_splits()
    if suggestions:
        print(f"  Split suggestions for {len(suggestions)} files:")
        for suggestion in suggestions:
            print(f"  - {suggestion['file']}: {suggestion['split_suggestion']}")
    else:
        print("  No split suggestions.")
