#!/usr/bin/env python3
"""
repo_context.py - Repository context management for Dev Environment Readyifier

This script handles the creation and management of specialized markdown files
for project documentation and repository context, following David Ondrej's
best practices for AI-assisted development.
"""

import os
import re
import subprocess
from pathlib import Path

class RepoContextManager:
    """Manages repository context and specialized markdown files."""
    
    def __init__(self, repo_path):
        """Initialize the repo context manager with the path to the repository."""
        self.repo_path = Path(repo_path)
        self.md_files = {
            "roadmap.md": "Project roadmap and future plans",
            "architecture.md": "System architecture and component relationships",
            "mvp.md": "Minimum Viable Product definition and features",
            "context.md": "Repository context for AI assistants"
        }
    
    def create_specialized_md_files(self):
        """Create specialized markdown files for project documentation."""
        results = {}
        
        for filename, description in self.md_files.items():
            file_path = self.repo_path / filename
            if not file_path.exists():
                try:
                    with open(file_path, 'w') as f:
                        f.write(self._generate_md_template(filename, description))
                    results[filename] = f"Created {filename}"
                except Exception as e:
                    results[filename] = f"Error creating {filename}: {e}"
            else:
                results[filename] = f"{filename} already exists"
        
        return results
    
    def _generate_md_template(self, filename, description):
        """Generate template content for specialized markdown files."""
        if filename == "roadmap.md":
            return self._generate_roadmap_template()
        elif filename == "architecture.md":
            return self._generate_architecture_template()
        elif filename == "mvp.md":
            return self._generate_mvp_template()
        elif filename == "context.md":
            return self._generate_context_template()
        else:
            return f"# {filename.replace('.md', '').title()}\n\n{description}\n\n"
    
    def _generate_roadmap_template(self):
        """Generate template for roadmap.md."""
        return """# Project Roadmap

## Current Version

### MVP Features
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Upcoming Releases

### Version 0.2
- [ ] Feature 4
- [ ] Feature 5

### Version 0.3
- [ ] Feature 6
- [ ] Feature 7

## Future Considerations
- [ ] Feature 8
- [ ] Feature 9

## Completed
- [x] Repository setup
"""
    
    def _generate_architecture_template(self):
        """Generate template for architecture.md."""
        return """# System Architecture

## Components

### Component 1
- Description: 
- Responsibilities:
- Dependencies:

### Component 2
- Description:
- Responsibilities:
- Dependencies:

## Data Flow
1. Step 1
2. Step 2
3. Step 3

## Technology Stack
- Frontend:
- Backend:
- Database:
- Infrastructure:

## Design Decisions
- Decision 1: Rationale
- Decision 2: Rationale
"""
    
    def _generate_mvp_template(self):
        """Generate template for mvp.md."""
        return """# Minimum Viable Product (MVP)

## Core Features
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## User Stories
1. As a [user type], I want to [action] so that [benefit]
2. As a [user type], I want to [action] so that [benefit]
3. As a [user type], I want to [action] so that [benefit]

## Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

## Out of Scope for MVP
- Feature A
- Feature B
- Feature C

## Implementation Priority
1. Highest priority
2. Medium priority
3. Lower priority
"""
    
    def _generate_context_template(self):
        """Generate template for context.md."""
        repo_name = self.repo_path.name
        
        # Try to get git remote info
        remote_url = ""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "remote", "-v"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                remote_match = re.search(r'origin\s+(\S+)', result.stdout)
                if remote_match:
                    remote_url = remote_match.group(1)
        except:
            pass
        
        # Try to get branch info
        branch = ""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "branch", "--show-current"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                branch = result.stdout.strip()
        except:
            pass
        
        return f"""# Repository Context

## Project: {repo_name}

## Repository Information
- Repository URL: {remote_url}
- Branch: {branch}

## Project Structure
```
{self._generate_directory_tree()}
```

## Key Files
- File 1: Description
- File 2: Description
- File 3: Description

## Development Workflow
1. Step 1
2. Step 2
3. Step 3

## Conventions
- Naming convention:
- Code style:
- Documentation:

## Notes for AI Assistants
- Always add filepath and filename as first entry in any file
- Keep files small and focused (< 200 lines)
- Implement features in simplest way possible
- Focus on MVP features first
- Test after every meaningful change
"""
    
    def _generate_directory_tree(self, max_depth=3):
        """Generate a simple directory tree for the repository."""
        result = []
        
        def _walk_dir(path, depth, prefix=""):
            if depth > max_depth:
                return
            
            items = sorted(os.listdir(path))
            dirs = [item for item in items if os.path.isdir(os.path.join(path, item)) and not item.startswith('.')]
            files = [item for item in items if os.path.isfile(os.path.join(path, item)) and not item.startswith('.')]
            
            for i, dir_name in enumerate(dirs):
                is_last = (i == len(dirs) - 1 and len(files) == 0)
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{dir_name}/")
                _walk_dir(
                    os.path.join(path, dir_name),
                    depth + 1,
                    prefix + ('    ' if is_last else '│   ')
                )
            
            for i, file_name in enumerate(files):
                is_last = (i == len(files) - 1)
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{file_name}")
        
        try:
            result.append(self.repo_path.name + "/")
            _walk_dir(self.repo_path, 1, "")
        except Exception as e:
            result.append(f"Error generating directory tree: {e}")
        
        return "\n".join(result)
    
    def generate_repo_prompt(self):
        """Generate a repository context prompt for AI assistants."""
        # Get repository name
        repo_name = self.repo_path.name
        
        # Try to get git info
        git_info = ""
        try:
            # Get remote URL
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "remote", "-v"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                git_info += f"Remote: {result.stdout.strip()}\n"
            
            # Get current branch
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "branch", "--show-current"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                git_info += f"Branch: {result.stdout.strip()}\n"
        except:
            git_info = "Git information not available\n"
        
        # Get file structure
        file_structure = self._generate_directory_tree()
        
        # Check for specialized MD files
        md_content = ""
        for filename in self.md_files:
            file_path = self.repo_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        md_content += f"\n## {filename}\n{content}\n"
                except:
                    md_content += f"\n## {filename}\nUnable to read file\n"
        
        # Construct the prompt
        prompt = f"""# Repository Context for {repo_name}

{git_info}

## File Structure
```
{file_structure}
```

{md_content}

## Development Guidelines
- Always add filepath and filename as first entry in any file
- Keep files small and focused (< 200 lines)
- Implement features in simplest way possible
- Focus on MVP features first
- Test after every meaningful change
"""
        
        return prompt
    
    def check_file_sizes(self):
        """Check for files exceeding the recommended 200-line limit."""
        large_files = []
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            line_count = sum(1 for _ in f)
                            if line_count > 200:
                                rel_path = os.path.relpath(file_path, self.repo_path)
                                large_files.append((rel_path, line_count))
                    except:
                        pass
        
        return large_files

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()
    
    manager = RepoContextManager(repo_path)
    
    print("Creating specialized markdown files...")
    results = manager.create_specialized_md_files()
    for filename, status in results.items():
        print(f"  - {status}")
    
    print("\nChecking file sizes...")
    large_files = manager.check_file_sizes()
    if large_files:
        print("  Files exceeding 200 lines:")
        for file_path, line_count in large_files:
            print(f"  - {file_path}: {line_count} lines")
    else:
        print("  No files exceed the 200-line limit.")
    
    print("\nRepository context prompt:")
    prompt = manager.generate_repo_prompt()
    print(f"  Generated prompt with {len(prompt)} characters")
    
    # Save prompt to file
    prompt_file = os.path.join(repo_path, "repo_prompt.md")
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    print(f"  Saved prompt to {prompt_file}")
