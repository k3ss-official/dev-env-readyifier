#!/usr/bin/env python3
"""
validate.py - Validation script for Dev Environment Readyifier

This script performs manual validation of the key features implemented
in the Dev Environment Readyifier, including:
1. File structure annotation
2. Specialized markdown file creation
3. Repository context prompting
4. File size checking

Usage:
    python tests/validate.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components
try:
    from scripts.repo_context import RepoContextManager
    from scripts.file_structure_manager import FileStructureManager
except ImportError as e:
    print(f"Error importing components: {e}")
    print("Make sure you're running this script from the repository root.")
    sys.exit(1)

def create_test_files(test_dir):
    """Create test files for validation."""
    # Create a Python file
    with open(os.path.join(test_dir, "test_file.py"), "w") as f:
        f.write("""def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
""")
    
    # Create a JavaScript file
    with open(os.path.join(test_dir, "test_file.js"), "w") as f:
        f.write("""function helloWorld() {
    console.log("Hello, World!");
}

helloWorld();
""")
    
    # Create a large file
    with open(os.path.join(test_dir, "large_file.py"), "w") as f:
        f.write("# This is a large file\n\n")
        for i in range(250):
            f.write(f"print('Line {i}')\n")
    
    # Create a subdirectory
    os.makedirs(os.path.join(test_dir, "subdir"), exist_ok=True)
    
    # Create a file in the subdirectory
    with open(os.path.join(test_dir, "subdir", "nested_file.py"), "w") as f:
        f.write("""def nested_function():
    print("I'm nested!")

nested_function()
""")

def validate_file_structure_annotation(test_dir):
    """Validate file structure annotation."""
    print("\n=== Validating File Structure Annotation ===")
    
    # Initialize file structure manager
    manager = FileStructureManager(test_dir)
    
    # Check file sizes
    print("Checking file sizes...")
    large_files = manager.check_file_sizes()
    if large_files:
        print(f"✓ Successfully detected {len(large_files)} large files:")
        for file_path, line_count in large_files:
            print(f"  - {file_path}: {line_count} lines")
    else:
        print("✗ Failed to detect large files")
        return False
    
    # Add file annotations
    print("\nAdding file annotations...")
    modified_files = manager.add_file_annotations()
    if modified_files:
        print(f"✓ Successfully added annotations to {len(modified_files)} files:")
        for file_path in modified_files:
            print(f"  - {file_path}")
        
        # Verify annotations were added
        for file_path in modified_files:
            full_path = os.path.join(test_dir, file_path)
            with open(full_path, "r") as f:
                content = f.read()
                if "File:" in content and file_path in content:
                    print(f"  ✓ Verified annotation in {file_path}")
                else:
                    print(f"  ✗ Failed to verify annotation in {file_path}")
                    return False
    else:
        print("✗ Failed to add file annotations")
        return False
    
    # Suggest file splits
    print("\nSuggesting file splits...")
    suggestions = manager.suggest_file_splits()
    if suggestions:
        print(f"✓ Successfully generated {len(suggestions)} split suggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion['file']}: {suggestion['split_suggestion']}")
    else:
        print("✗ Failed to generate split suggestions")
        return False
    
    return True

def validate_repo_context(test_dir):
    """Validate repository context management."""
    print("\n=== Validating Repository Context Management ===")
    
    # Initialize repo context manager
    manager = RepoContextManager(test_dir)
    
    # Create specialized markdown files
    print("Creating specialized markdown files...")
    results = manager.create_specialized_md_files()
    success = True
    for filename, status in results.items():
        print(f"  - {status}")
        if "Error" in status:
            success = False
    
    if success:
        print("✓ Successfully created specialized markdown files")
        
        # Verify files were created
        for filename in manager.md_files:
            file_path = os.path.join(test_dir, filename)
            if os.path.exists(file_path):
                print(f"  ✓ Verified {filename} exists")
            else:
                print(f"  ✗ Failed to verify {filename} exists")
                success = False
    else:
        print("✗ Failed to create specialized markdown files")
        return False
    
    # Generate repository context prompt
    print("\nGenerating repository context prompt...")
    prompt = manager.generate_repo_prompt()
    if prompt and len(prompt) > 100:  # Simple check that prompt has content
        print(f"✓ Successfully generated prompt with {len(prompt)} characters")
        
        # Save prompt to file
        prompt_file = os.path.join(test_dir, "repo_prompt.md")
        with open(prompt_file, "w") as f:
            f.write(prompt)
        print(f"  ✓ Saved prompt to {prompt_file}")
        
        # Verify prompt contains expected sections
        expected_sections = ["File Structure", "Development Guidelines"]
        for section in expected_sections:
            if section in prompt:
                print(f"  ✓ Verified prompt contains '{section}' section")
            else:
                print(f"  ✗ Failed to verify prompt contains '{section}' section")
                success = False
    else:
        print("✗ Failed to generate repository context prompt")
        return False
    
    return success

def validate_mac_compatibility():
    """Validate Mac compatibility."""
    print("\n=== Validating Mac Compatibility ===")
    
    # Check for Mac-specific paths in detector.py
    print("Checking for Mac-specific paths in detector.py...")
    detector_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "detector.py")
    
    if not os.path.exists(detector_path):
        print("✗ detector.py not found")
        return False
    
    with open(detector_path, "r") as f:
        content = f.read()
    
    mac_paths = [
        "/Applications/",
        ".app/Contents/",
        "~/Library/"
    ]
    
    found_paths = []
    for path in mac_paths:
        if path in content:
            found_paths.append(path)
    
    if found_paths:
        print(f"✓ Found {len(found_paths)} Mac-specific paths:")
        for path in found_paths:
            print(f"  - {path}")
    else:
        print("✗ No Mac-specific paths found")
        return False
    
    # Check for Trae IDE detection
    print("\nChecking for Trae IDE detection...")
    if "Trae" in content or "trae" in content:
        print("✓ Found Trae IDE detection code")
    else:
        print("✗ No Trae IDE detection code found")
        return False
    
    return True

def main():
    """Main validation function."""
    print("=== Dev Environment Readyifier Validation ===")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary test directory: {temp_dir}")
        
        # Create test files
        create_test_files(temp_dir)
        print("Created test files")
        
        # Validate file structure annotation
        file_structure_success = validate_file_structure_annotation(temp_dir)
        
        # Validate repository context
        repo_context_success = validate_repo_context(temp_dir)
    
    # Validate Mac compatibility
    mac_compatibility_success = validate_mac_compatibility()
    
    # Print summary
    print("\n=== Validation Summary ===")
    print(f"File Structure Annotation: {'✓ PASS' if file_structure_success else '✗ FAIL'}")
    print(f"Repository Context: {'✓ PASS' if repo_context_success else '✗ FAIL'}")
    print(f"Mac Compatibility: {'✓ PASS' if mac_compatibility_success else '✗ FAIL'}")
    
    overall_success = file_structure_success and repo_context_success and mac_compatibility_success
    print(f"\nOverall Validation: {'✓ PASS' if overall_success else '✗ FAIL'}")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    sys.exit(main())
