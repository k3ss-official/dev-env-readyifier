#!/usr/bin/env python3
"""
installer.py - Tool installation and configuration module for Dev Environment Readyifier

This module handles the installation of missing tools and extensions,
as well as applying configurations to selected tools.
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class ToolInstaller:
    """Handles installation of tools and extensions."""
    
    def __init__(self, detection_results: Dict, config_choices: Dict):
        self.detection_results = detection_results
        self.config_choices = config_choices
        self.os_type = platform.system()
        self.install_results = {
            "success": [],
            "failed": [],
            "skipped": []
        }
    
    def install_missing_tools(self, tools_to_install: List[str]) -> Dict:
        """Install missing tools from the provided list."""
        print("\n" + "="*60)
        print("  INSTALLING MISSING TOOLS")
        print("="*60)
        
        for tool in tools_to_install:
            print(f"\nAttempting to install {tool}...")
            success = self._install_tool(tool)
            
            if success:
                print(f"✓ Successfully installed {tool}")
                self.install_results["success"].append(tool)
            else:
                print(f"✗ Failed to install {tool}")
                self.install_results["failed"].append(tool)
        
        return self.install_results
    
    def install_extensions(self, ide: str, extensions: List[str]) -> Dict:
        """Install extensions for the specified IDE."""
        print(f"\nInstalling extensions for {ide.upper()}...")
        
        extension_results = {
            "success": [],
            "failed": []
        }
        
        for extension in extensions:
            print(f"  Installing {extension}...")
            success = self._install_extension(ide, extension)
            
            if success:
                print(f"  ✓ Successfully installed {extension}")
                extension_results["success"].append(extension)
            else:
                print(f"  ✗ Failed to install {extension}")
                extension_results["failed"].append(extension)
        
        return extension_results
    
    def apply_configurations(self) -> Dict:
        """Apply configurations to selected tools."""
        print("\n" + "="*60)
        print("  APPLYING CONFIGURATIONS")
        print("="*60)
        
        config_results = {
            "success": [],
            "failed": []
        }
        
        # Apply configurations for each selected tool
        for tool, selected in self.config_choices.get("selected_tools", {}).items():
            if not selected:
                continue
                
            print(f"\nConfiguring {tool.upper()}...")
            success = self._apply_tool_config(tool)
            
            if success:
                print(f"✓ Successfully configured {tool}")
                config_results["success"].append(tool)
            else:
                print(f"✗ Failed to configure {tool}")
                config_results["failed"].append(tool)
        
        # Set up reference structure if selected
        if self.config_choices.get("reference_structure", False):
            print("\nSetting up reference data structure...")
            success = self._setup_reference_structure()
            
            if success:
                print("✓ Successfully set up reference structure")
                config_results["success"].append("reference_structure")
            else:
                print("✗ Failed to set up reference structure")
                config_results["failed"].append("reference_structure")
        
        return config_results
    
    def _install_tool(self, tool: str) -> bool:
        """Install a specific tool."""
        try:
            if tool == "vscode":
                return self._install_vscode()
            elif tool == "vscode_insiders":
                return self._install_vscode_insiders()
            elif tool == "trae":
                return self._install_trae()
            elif tool == "void":
                return self._install_void()
            elif tool == "cline":
                return self._install_cline()
            elif tool == "roo":
                return self._install_roo()
            elif tool == "aider":
                return self._install_aider()
            else:
                print(f"Unknown tool: {tool}")
                return False
        except Exception as e:
            print(f"Error installing {tool}: {e}")
            return False
    
    def _install_vscode(self) -> bool:
        """Install Visual Studio Code."""
        try:
            if self.os_type == "Darwin":  # macOS
                return self._run_command("brew install --cask visual-studio-code")
            elif self.os_type == "Linux":
                # This is a simplified version - would need distro detection in real implementation
                return self._run_command(
                    "curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.gpg && "
                    "sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg && "
                    "sudo sh -c 'echo \"deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list' && "
                    "sudo apt update && sudo apt install -y code"
                )
            elif self.os_type == "Windows":
                # For Windows, we'd typically use winget or chocolatey
                # This is a placeholder
                print("For Windows, please download VS Code from https://code.visualstudio.com/download")
                return False
            
            return False
        except Exception as e:
            print(f"Error installing VS Code: {e}")
            return False
    
    def _install_vscode_insiders(self) -> bool:
        """Install Visual Studio Code Insiders."""
        try:
            if self.os_type == "Darwin":  # macOS
                return self._run_command("brew install --cask visual-studio-code-insiders")
            elif self.os_type == "Linux":
                # Similar to VS Code but for Insiders
                return self._run_command(
                    "curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.gpg && "
                    "sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg && "
                    "sudo sh -c 'echo \"deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list' && "
                    "sudo apt update && sudo apt install -y code-insiders"
                )
            elif self.os_type == "Windows":
                print("For Windows, please download VS Code Insiders from https://code.visualstudio.com/insiders/")
                return False
            
            return False
        except Exception as e:
            print(f"Error installing VS Code Insiders: {e}")
            return False
    
    def _install_trae(self) -> bool:
        """Install Trae IDE."""
        # This is a placeholder - would need actual installation instructions
        print("Trae IDE installation is not yet automated.")
        print("Please visit the Trae IDE website for installation instructions.")
        return False
    
    def _install_void(self) -> bool:
        """Install VOID IDE."""
        # This is a placeholder - would need actual installation instructions
        print("VOID IDE installation is not yet automated.")
        print("Please visit the VOID IDE website for installation instructions.")
        return False
    
    def _install_cline(self) -> bool:
        """Install Cline."""
        try:
            # Assuming Cline is a Python package
            return self._run_command("pip install --upgrade cline")
        except Exception as e:
            print(f"Error installing Cline: {e}")
            return False
    
    def _install_roo(self) -> bool:
        """Install Roo Code."""
        try:
            # Assuming Roo is a Python package
            return self._run_command("pip install --upgrade roo-code")
        except Exception as e:
            print(f"Error installing Roo Code: {e}")
            return False
    
    def _install_aider(self) -> bool:
        """Install Aider."""
        try:
            # Aider is a Python package
            return self._run_command("pip install --upgrade aider-chat")
        except Exception as e:
            print(f"Error installing Aider: {e}")
            return False
    
    def _install_extension(self, ide: str, extension: str) -> bool:
        """Install an extension for the specified IDE."""
        try:
            if ide == "vscode" or ide == "vscode_insiders":
                cmd = "code"
                if ide == "vscode_insiders":
                    cmd = "code-insiders"
                
                return self._run_command(f"{cmd} --install-extension {extension}")
            else:
                print(f"Extension installation not supported for {ide}")
                return False
        except Exception as e:
            print(f"Error installing extension {extension} for {ide}: {e}")
            return False
    
    def _apply_tool_config(self, tool: str) -> bool:
        """Apply configuration for a specific tool."""
        try:
            # Get the base directory for configurations
            base_dir = self._get_repo_base_dir()
            if not base_dir:
                print("Could not determine repository base directory")
                return False
            
            # Get the template directory
            template_dir = os.path.join(base_dir, "templates")
            
            # Get the security level
            security_level = self.config_choices.get("security_level", "standard")
            
            # Apply AI rules
            if tool in ["vscode", "vscode_insiders", "trae", "void"]:
                # Copy .cursorrules to appropriate location
                cursorrules_src = os.path.join(template_dir, "ai_rules", ".cursorrules")
                cursorrules_dest = self._get_tool_config_dir(tool)
                
                if cursorrules_dest:
                    os.makedirs(cursorrules_dest, exist_ok=True)
                    shutil.copy(cursorrules_src, os.path.join(cursorrules_dest, ".cursorrules"))
                    print(f"  ✓ Applied .cursorrules to {tool}")
                else:
                    print(f"  ✗ Could not determine config directory for {tool}")
                    return False
            
            # Apply security configurations
            security_src = os.path.join(template_dir, "security", f"{security_level}.json")
            if os.path.exists(security_src):
                security_dest = self._get_tool_config_dir(tool)
                if security_dest:
                    os.makedirs(security_dest, exist_ok=True)
                    shutil.copy(security_src, os.path.join(security_dest, "security_config.json"))
                    print(f"  ✓ Applied {security_level} security config to {tool}")
                else:
                    print(f"  ✗ Could not determine config directory for {tool}")
                    return False
            
            # Apply tool-specific configurations
            tool_config_src = os.path.join(base_dir, "configs", tool)
            if os.path.exists(tool_config_src):
                tool_config_dest = self._get_tool_config_dir(tool)
                if tool_config_dest:
                    # Copy all files from tool config directory
                    for item in os.listdir(tool_config_src):
                        s = os.path.join(tool_config_src, item)
                        d = os.path.join(tool_config_dest, item)
                        if os.path.isfile(s):
                            shutil.copy2(s, d)
                        elif os.path.isdir(s):
                            shutil.copytree(s, d, dirs_exist_ok=True)
                    
                    print(f"  ✓ Applied tool-specific configs to {tool}")
                else:
                    print(f"  ✗ Could not determine config directory for {tool}")
                    return False
            
            return True
        except Exception as e:
            print(f"Error applying configuration for {tool}: {e}")
            return False
    
    def _setup_reference_structure(self) -> bool:
        """Set up reference data structure."""
        try:
            # Get the base directory for the user's projects
            projects_dir = self._get_projects_dir()
            if not projects_dir:
                print("Could not determine projects directory")
                return False
            
            # Get the template directory
            base_dir = self._get_repo_base_dir()
            if not base_dir:
                print("Could not determine repository base directory")
                return False
            
            template_dir = os.path.join(base_dir, "templates", "reference")
            
            # Create reference structure
            reference_dir = os.path.join(projects_dir, "reference")
            os.makedirs(reference_dir, exist_ok=True)
            
            # Create subdirectories
            subdirs = ["org", "tech", "security", "api", "workflow"]
            for subdir in subdirs:
                os.makedirs(os.path.join(reference_dir, subdir), exist_ok=True)
            
            # Copy template files if they exist
            if os.path.exists(template_dir):
                for item in os.listdir(template_dir):
                    s = os.path.join(template_dir, item)
                    d = os.path.join(reference_dir, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                    elif os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
            
            print(f"  ✓ Created reference structure at {reference_dir}")
            return True
        except Exception as e:
            print(f"Error setting up reference structure: {e}")
            return False
    
    def _get_repo_base_dir(self) -> Optional[str]:
        """Get the base directory of the repository."""
        try:
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Go up one level to get the repo base directory
            return os.path.dirname(script_dir)
        except Exception:
            return None
    
    def _get_tool_config_dir(self, tool: str) -> Optional[str]:
        """Get the configuration directory for a specific tool."""
        try:
            if tool == "vscode" or tool == "vscode_insiders":
                if self.os_type == "Darwin":  # macOS
                    return os.path.join(str(Path.home()), "Library", "Application Support", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
                elif self.os_type == "Linux":
                    return os.path.join(str(Path.home()), ".config", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
                elif self.os_type == "Windows":
                    return os.path.join(str(Path.home()), "AppData", "Roaming", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
            elif tool == "trae":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "trae")
            elif tool == "void":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "void")
            elif tool == "cline":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "cline")
            elif tool == "roo":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "roo")
            elif tool == "aider":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "aider")
            
            return None
        except Exception:
            return None
    
    def _get_projects_dir(self) -> str:
        """Get the user's projects directory."""
        # Default to home directory
        projects_dir = str(Path.home())
        
        # Check for common project directories
        common_dirs = [
            os.path.join(str(Path.home()), "projects"),
            os.path.join(str(Path.home()), "Documents", "projects"),
            os.path.join(str(Path.home()), "dev")
        ]
        
        for dir_path in common_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                projects_dir = dir_path
                break
        
        return projects_dir
    
    def _run_command(self, command: str) -> bool:
        """Run a shell command and return success status."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Command failed: {command}")
                print(f"Error: {result.stderr}")
                return False
            
            return True
        except Exception as e:
            print(f"Error running command: {e}")
            return False


if __name__ == "__main__":
    # For testing purposes, create sample data
    sample_detection = {
        "os_info": {
            "system": "Darwin",
            "release": "21.6.0",
            "python_version": "3.9.7"
        },
        "ides": {
            "vscode": {"version": "1.77.0"}
        },
        "ai_tools": {
            "aider": {"version": "0.14.1"}
        }
    }
    
    sample_config = {
        "selected_tools": {
            "vscode": True,
            "aider": True
        },
        "security_level": "standard",
        "ai_personality": "default",
        "reference_structure": True
    }
    
    # Create installer and test
    installer = ToolInstaller(sample_detection, sample_config)
    
    # Test installing missing tools
    print("Testing tool installation...")
    install_results = installer.install_missing_tools(["cline", "roo"])
    print(f"Installation results: {json.dumps(install_results, indent=2)}")
    
    # Test applying configurations
    print("\nTesting configuration application...")
    config_results = installer.apply_configurations()
    print(f"Configuration results: {json.dumps(config_results, indent=2)}")
    
    print("\nInstallation and configuration complete!")
