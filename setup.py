#!/usr/bin/env python3
"""
setup.py - Main setup script for Dev Environment Readyifier

This script serves as the entry point for the Dev Environment Readyifier tool.
It launches the GUI interface and orchestrates the detection, configuration,
and installation processes.
"""

import os
import sys
import tkinter as tk
from pathlib import Path

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

try:
    from scripts.gui_manager import ReadyifierGUI
except ImportError:
    print("Error: Required modules not found.")
    print("Please ensure you have the required dependencies installed.")
    print("Try running: pip install tkinter")
    sys.exit(1)

def main():
    """Main entry point for the application."""
    print("Starting Dev Environment Readyifier...")
    
    # Check if running in GUI mode or CLI mode
    gui_mode = True
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        gui_mode = False
    
    if gui_mode:
        try:
            root = tk.Tk()
            app = ReadyifierGUI(root)
            root.mainloop()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("Falling back to CLI mode...")
            gui_mode = False
    
    if not gui_mode:
        print("CLI mode not yet implemented.")
        print("Please run without the --cli flag to use the GUI interface.")
        sys.exit(1)

if __name__ == "__main__":
    main()
