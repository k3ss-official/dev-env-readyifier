#!/usr/bin/env python3
"""
configurator.py - Interactive configuration module for Dev Environment Readyifier

This module provides an interactive interface for selecting which tools to configure
and what settings to apply to each.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class ConfigurationManager:
    """Manages the interactive configuration process."""
    
    def __init__(self, detection_results: Dict):
        self.detection_results = detection_results
        self.selected_tools = {}
        self.config_options = {}
        self.security_level = "standard"
        
    def run_interactive_setup(self) -> Dict:
        """Run the interactive setup process and return configuration choices."""
        self._print_welcome()
        self._display_detected_tools()
        self._select_tools_to_configure()
        self._configure_security_level()
        self._configure_ai_personality()
        self._confirm_selections()
        
        return {
            "selected_tools": self.selected_tools,
            "security_level": self.security_level,
            "ai_personality": self.config_options.get("ai_personality", "default"),
            "reference_structure": self.config_options.get("reference_structure", True)
        }
    
    def _print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*60)
        print("  DEVELOPMENT ENVIRONMENT READYIFIER - CONFIGURATION")
        print("="*60)
        print("\nThis wizard will help you configure your development environment.")
        print("We've detected your installed tools and will help you set them up with")
        print("optimal settings, security hardening, and AI assistant configurations.")
        print("\nPress Enter to continue...")
        input()
    
    def _display_detected_tools(self):
        """Display all detected tools."""
        print("\n" + "="*60)
        print("  DETECTED DEVELOPMENT TOOLS")
        print("="*60)
        
        # Display IDEs
        print("\nIDEs:")
        if not self.detection_results.get('ides'):
            print("  No IDEs detected")
        else:
            for ide, info in self.detection_results['ides'].items():
                print(f"  ✓ {ide.upper()}: {info.get('version', 'Unknown version')}")
        
        # Display AI Tools
        print("\nAI Tools:")
        if not self.detection_results.get('ai_tools'):
            print("  No AI tools detected")
        else:
            for tool, info in self.detection_results['ai_tools'].items():
                print(f"  ✓ {tool.upper()}: {info.get('version', 'Unknown version')}")
        
        # Display Conda Environments
        print("\nConda Environments:")
        if not self.detection_results.get('conda_environments'):
            print("  No Conda environments detected")
        else:
            for env in self.detection_results['conda_environments']:
                print(f"  ✓ {env['name']}")
        
        # Display VS Code Extensions (if any)
        if self.detection_results.get('vscode_extensions'):
            print("\nVS Code Extensions:")
            print(f"  {len(self.detection_results['vscode_extensions'])} extensions detected")
        
        print("\nPress Enter to continue...")
        input()
    
    def _select_tools_to_configure(self):
        """Allow user to select which tools to configure."""
        print("\n" + "="*60)
        print("  SELECT TOOLS TO CONFIGURE")
        print("="*60)
        print("\nSelect which tools you want to configure (y/n for each):")
        
        # Select IDEs
        if self.detection_results.get('ides'):
            print("\nIDEs:")
            for ide in self.detection_results['ides'].keys():
                while True:
                    response = input(f"  Configure {ide.upper()}? (y/n): ").lower()
                    if response in ['y', 'n']:
                        self.selected_tools[ide] = (response == 'y')
                        break
                    print("  Please enter 'y' or 'n'")
        
        # Select AI Tools
        if self.detection_results.get('ai_tools'):
            print("\nAI Tools:")
            for tool in self.detection_results['ai_tools'].keys():
                while True:
                    response = input(f"  Configure {tool.upper()}? (y/n): ").lower()
                    if response in ['y', 'n']:
                        self.selected_tools[tool] = (response == 'y')
                        break
                    print("  Please enter 'y' or 'n'")
        
        # Ask about reference structure
        print("\nReference Data:")
        while True:
            response = input("  Create reference data structure? (y/n): ").lower()
            if response in ['y', 'n']:
                self.config_options["reference_structure"] = (response == 'y')
                break
            print("  Please enter 'y' or 'n'")
    
    def _configure_security_level(self):
        """Configure security level."""
        print("\n" + "="*60)
        print("  SECURITY CONFIGURATION")
        print("="*60)
        print("\nSelect security level:")
        print("  1. Standard - Recommended security practices")
        print("  2. Enhanced - Additional security measures and hardening")
        
        while True:
            response = input("\nSelect security level (1/2): ")
            if response in ['1', '2']:
                self.security_level = "standard" if response == '1' else "enhanced"
                break
            print("  Please enter '1' or '2'")
    
    def _configure_ai_personality(self):
        """Configure AI assistant personality."""
        print("\n" + "="*60)
        print("  AI ASSISTANT CONFIGURATION")
        print("="*60)
        print("\nSelect AI assistant personality profile:")
        print("  1. Default - Based on provided personality profile")
        print("  2. Custom - Modify personality traits")
        
        while True:
            response = input("\nSelect personality profile (1/2): ")
            if response in ['1', '2']:
                if response == '1':
                    self.config_options["ai_personality"] = "default"
                else:
                    self._customize_ai_personality()
                break
            print("  Please enter '1' or '2'")
    
    def _customize_ai_personality(self):
        """Allow customization of AI personality traits."""
        print("\nCustomize AI personality traits:")
        print("  This will create a custom personality profile.")
        
        # Placeholder for actual customization
        # In a real implementation, this would allow detailed customization
        print("  Using default personality profile for now.")
        print("  (Full customization will be implemented in a future version)")
        
        self.config_options["ai_personality"] = "default"
    
    def _confirm_selections(self):
        """Confirm all selections before proceeding."""
        print("\n" + "="*60)
        print("  CONFIGURATION SUMMARY")
        print("="*60)
        
        print("\nSelected tools to configure:")
        for tool, selected in self.selected_tools.items():
            if selected:
                print(f"  ✓ {tool.upper()}")
        
        print(f"\nSecurity level: {self.security_level.upper()}")
        print(f"AI personality: {self.config_options.get('ai_personality', 'default').upper()}")
        print(f"Reference structure: {'Yes' if self.config_options.get('reference_structure', True) else 'No'}")
        
        print("\nReady to apply these configurations?")
        while True:
            response = input("Proceed with configuration? (y/n): ").lower()
            if response == 'y':
                print("\nProceeding with configuration...")
                return
            elif response == 'n':
                print("\nConfiguration cancelled. Exiting...")
                sys.exit(0)
            else:
                print("  Please enter 'y' or 'n'")


if __name__ == "__main__":
    # For testing purposes, create a sample detection result
    sample_detection = {
        "os_info": {
            "system": "Darwin",
            "release": "21.6.0",
            "python_version": "3.9.7"
        },
        "ides": {
            "vscode": {"version": "1.77.0"},
            "vscode_insiders": {"version": "1.78.0-insider"}
        },
        "ai_tools": {
            "cline": {"version": "0.5.2"},
            "aider": {"version": "0.14.1"}
        },
        "conda_environments": [
            {"name": "base", "path": "/opt/conda"},
            {"name": "project1", "path": "/opt/conda/envs/project1"}
        ],
        "vscode_extensions": [
            {"id": "ms-python.python", "name": "python"},
            {"id": "github.copilot", "name": "copilot"}
        ]
    }
    
    # Run the configuration manager with sample data
    config_manager = ConfigurationManager(sample_detection)
    config = config_manager.run_interactive_setup()
    
    print("\nConfiguration complete!")
    print(f"Configuration: {json.dumps(config, indent=2)}")
