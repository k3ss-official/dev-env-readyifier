#!/usr/bin/env python3
"""
setup.py - Main entry point for Dev Environment Readyifier

This script integrates all components of the Dev Environment Readyifier,
including environment detection, extension management, AI rules configuration,
and repository context management.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import components
try:
    from scripts.detector import EnvironmentDetector
    from scripts.configurator import EnvironmentConfigurator
    from scripts.installer import ToolInstaller
    from scripts.gui_manager import GUIManager
    from scripts.extension_manager import ExtensionManager
    from scripts.repo_context import RepoContextManager
    from scripts.file_structure_manager import FileStructureManager
except ImportError as e:
    print(f"Error importing components: {e}")
    print("Make sure you're running this script from the repository root.")
    sys.exit(1)

def main():
    """Main entry point for the Dev Environment Readyifier."""
    parser = argparse.ArgumentParser(description="Dev Environment Readyifier")
    parser.add_argument("--no-gui", action="store_true", help="Run in command-line mode without GUI")
    parser.add_argument("--install-all", action="store_true", help="Automatically install all missing tools and extensions")
    parser.add_argument("--repo-path", type=str, help="Path to repository for context management")
    args = parser.parse_args()

    # Determine repository path
    repo_path = args.repo_path if args.repo_path else os.getcwd()
    
    # Print welcome message
    print("=" * 80)
    print("Welcome to Dev Environment Readyifier!")
    print("=" * 80)
    print(f"Repository path: {repo_path}")
    print()

    # Initialize components
    detector = EnvironmentDetector()
    configurator = EnvironmentConfigurator()
    installer = ToolInstaller()
    extension_manager = ExtensionManager(os.path.join(os.path.dirname(__file__), "templates", "recommended_extensions.json"))
    repo_context_manager = RepoContextManager(repo_path)
    file_structure_manager = FileStructureManager(repo_path)

    # Detect environments
    print("Detecting installed development environments...")
    environments = detector.detect_environments()
    print(f"Found {len(environments)} environments:")
    for env_name, env_info in environments.items():
        print(f"  - {env_name}: {env_info.get('path', 'Unknown path')}")
    print()

    # Check for missing extensions
    print("Checking for missing extensions...")
    missing_extensions = extension_manager.detect_missing_extensions()
    if missing_extensions:
        print(f"Found missing extensions in {len(missing_extensions)} environments:")
        for env_name, categories in missing_extensions.items():
            total_missing = sum(len(exts) for exts in categories.values())
            print(f"  - {env_name}: {total_missing} missing extensions")
    else:
        print("No missing extensions found.")
    print()

    # Check file sizes
    print("Checking file sizes...")
    large_files = file_structure_manager.check_file_sizes()
    if large_files:
        print(f"Found {len(large_files)} files exceeding the recommended 200-line limit:")
        for file_path, line_count in large_files[:5]:
            print(f"  - {file_path}: {line_count} lines")
        if len(large_files) > 5:
            print(f"  - ... and {len(large_files) - 5} more")
    else:
        print("No files exceed the 200-line limit.")
    print()

    # If GUI mode is enabled and tkinter is available
    if not args.no_gui:
        try:
            import tkinter
            print("Starting GUI...")
            gui = GUIManager(
                environments=environments,
                missing_extensions=missing_extensions,
                large_files=large_files,
                extension_manager=extension_manager,
                repo_context_manager=repo_context_manager,
                file_structure_manager=file_structure_manager
            )
            gui.run()
            return
        except ImportError:
            print("Tkinter not available, falling back to command-line mode.")
            print()

    # Command-line mode
    if args.install_all:
        # Install all missing extensions
        if missing_extensions:
            print("Installing all missing extensions...")
            selections = {}
            for env_name, categories in missing_extensions.items():
                selections[env_name] = {}
                for category, extensions in categories.items():
                    if env_name in ["vscode", "vscode_insiders"]:
                        selections[env_name][category] = [ext["id"] for ext in extensions if "id" in ext]
                    else:
                        selections[env_name][category] = extensions
            
            results = extension_manager.install_selected_extensions(selections)
            print("Installation results:")
            print(f"  - Successfully installed: {len(results['success'])}")
            print(f"  - Failed installations: {len(results['failed'])}")
        
        # Create specialized markdown files
        print("\nCreating specialized markdown files...")
        results = repo_context_manager.create_specialized_md_files()
        for filename, status in results.items():
            print(f"  - {status}")
        
        # Add file annotations
        print("\nAdding file annotations...")
        modified_files = file_structure_manager.add_file_annotations()
        print(f"  - Added annotations to {len(modified_files)} files")
        
        # Generate repository context prompt
        print("\nGenerating repository context prompt...")
        prompt = repo_context_manager.generate_repo_prompt()
        prompt_file = os.path.join(repo_path, "repo_prompt.md")
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        print(f"  - Saved prompt to {prompt_file}")
    else:
        print("Run with --install-all to automatically install all missing extensions and configure repository.")
        print("Run with --no-gui to use command-line mode.")
        print("Run with --repo-path to specify a different repository path.")

if __name__ == "__main__":
    main()
