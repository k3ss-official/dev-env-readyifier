#!/usr/bin/env python3
"""
extension_manager.py - Extension detection and installation for Dev Environment Readyifier

This script handles the detection, selection, and installation of recommended extensions
for various development environments including VSCode, VSCode Insiders, Trae IDE, VOID IDE,
and CLI tools like Aider.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

class ExtensionManager:
    """Manages extension detection and installation for various development environments."""
    
    def __init__(self, config_path):
        """Initialize the extension manager with the path to the extension configuration."""
        self.config_path = config_path
        self.extensions = self._load_extensions()
        self.installed_extensions = {}
        self.missing_extensions = {}
    
    def _load_extensions(self):
        """Load the recommended extensions from the JSON configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading extensions configuration: {e}")
            return {}
    
    def detect_vscode(self):
        """Detect if VSCode is installed and return the path."""
        # Check common installation paths
        paths = [
            # Linux
            "/usr/bin/code",
            "/usr/local/bin/code",
            # macOS
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
            # Windows (via WSL)
            "/mnt/c/Program Files/Microsoft VS Code/bin/code",
            "/mnt/c/Users/*/AppData/Local/Programs/Microsoft VS Code/bin/code"
        ]
        
        for path in paths:
            if "*" in path:
                # Handle wildcard paths
                import glob
                for match in glob.glob(path):
                    if os.path.exists(match):
                        return match
            elif os.path.exists(path):
                return path
        
        # Try using 'which' command
        try:
            result = subprocess.run(["which", "code"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def detect_vscode_insiders(self):
        """Detect if VSCode Insiders is installed and return the path."""
        # Similar to detect_vscode but for Insiders
        paths = [
            # Linux
            "/usr/bin/code-insiders",
            "/usr/local/bin/code-insiders",
            # macOS
            "/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code",
            # Windows (via WSL)
            "/mnt/c/Program Files/Microsoft VS Code Insiders/bin/code-insiders",
            "/mnt/c/Users/*/AppData/Local/Programs/Microsoft VS Code Insiders/bin/code-insiders"
        ]
        
        for path in paths:
            if "*" in path:
                # Handle wildcard paths
                import glob
                for match in glob.glob(path):
                    if os.path.exists(match):
                        return match
            elif os.path.exists(path):
                return path
        
        # Try using 'which' command
        try:
            result = subprocess.run(["which", "code-insiders"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def detect_trae_ide(self):
        """Detect if Trae IDE is installed and return the path."""
        # Paths for Trae IDE
        paths = [
            # Common installation paths
            "/usr/bin/trae",
            "/usr/local/bin/trae",
            "/Applications/Trae.app/Contents/Resources/app/bin/trae",
            "/mnt/c/Program Files/Trae/bin/trae",
            "/mnt/c/Users/*/AppData/Local/Programs/Trae/bin/trae"
        ]
        
        for path in paths:
            if "*" in path:
                import glob
                for match in glob.glob(path):
                    if os.path.exists(match):
                        return match
            elif os.path.exists(path):
                return path
        
        # Try using 'which' command
        try:
            result = subprocess.run(["which", "trae"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def detect_void_ide(self):
        """Detect if VOID IDE is installed and return the path."""
        # Paths for VOID IDE
        paths = [
            # Common installation paths
            "/usr/bin/void",
            "/usr/local/bin/void",
            "/Applications/VOID.app/Contents/Resources/app/bin/void",
            "/mnt/c/Program Files/VOID/bin/void",
            "/mnt/c/Users/*/AppData/Local/Programs/VOID/bin/void"
        ]
        
        for path in paths:
            if "*" in path:
                import glob
                for match in glob.glob(path):
                    if os.path.exists(match):
                        return match
            elif os.path.exists(path):
                return path
        
        # Try using 'which' command
        try:
            result = subprocess.run(["which", "void"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def detect_aider(self):
        """Detect if Aider is installed and return the path."""
        # Try using 'which' command
        try:
            result = subprocess.run(["which", "aider"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Check if it's installed via pip
        try:
            result = subprocess.run(["pip", "show", "aider-chat"], capture_output=True, text=True)
            if result.returncode == 0:
                return "aider-chat (pip package)"
        except:
            pass
        
        return None
    
    def detect_cline(self):
        """Detect if Cline is installed and return the path."""
        # Check for Cline extension in VSCode
        vscode_path = self.detect_vscode()
        if vscode_path:
            try:
                result = subprocess.run([vscode_path, "--list-extensions"], capture_output=True, text=True)
                if "Cline.cline" in result.stdout:
                    return "Cline (VSCode extension)"
            except:
                pass
        
        return None
    
    def detect_roo_code(self):
        """Detect if Roo Code is installed and return the path."""
        # Check for Roo Code extension in VSCode
        vscode_path = self.detect_vscode()
        if vscode_path:
            try:
                result = subprocess.run([vscode_path, "--list-extensions"], capture_output=True, text=True)
                if "RooCode.roocode" in result.stdout:
                    return "Roo Code (VSCode extension)"
            except:
                pass
        
        return None
    
    def get_installed_vscode_extensions(self, vscode_path):
        """Get a list of installed VSCode extensions."""
        if not vscode_path:
            return []
        
        try:
            result = subprocess.run([vscode_path, "--list-extensions"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
            return []
        except:
            return []
    
    def detect_all_environments(self):
        """Detect all supported development environments."""
        environments = {
            "vscode": self.detect_vscode(),
            "vscode_insiders": self.detect_vscode_insiders(),
            "trae_ide": self.detect_trae_ide(),
            "void_ide": self.detect_void_ide(),
            "aider": self.detect_aider(),
            "cline": self.detect_cline(),
            "roo_code": self.detect_roo_code()
        }
        
        # Filter out uninstalled environments
        return {k: v for k, v in environments.items() if v}
    
    def detect_missing_extensions(self):
        """Detect which recommended extensions are missing from each environment."""
        environments = self.detect_all_environments()
        
        for env_name, env_path in environments.items():
            if env_name == "vscode":
                installed = self.get_installed_vscode_extensions(env_path)
                self.installed_extensions[env_name] = installed
                
                # Check which recommended extensions are missing
                if env_name in self.extensions:
                    missing = {}
                    for category, exts in self.extensions[env_name].items():
                        missing_in_category = []
                        for ext in exts:
                            if "id" in ext and ext["id"] not in installed:
                                missing_in_category.append(ext)
                        if missing_in_category:
                            missing[category] = missing_in_category
                    
                    if missing:
                        self.missing_extensions[env_name] = missing
            
            elif env_name == "vscode_insiders":
                installed = self.get_installed_vscode_extensions(env_path)
                self.installed_extensions[env_name] = installed
                
                # Check which recommended extensions are missing
                if env_name in self.extensions:
                    missing = {}
                    for category, exts in self.extensions[env_name].items():
                        missing_in_category = []
                        for ext in exts:
                            if "id" in ext and ext["id"] not in installed:
                                missing_in_category.append(ext)
                        if missing_in_category:
                            missing[category] = missing_in_category
                    
                    if missing:
                        self.missing_extensions[env_name] = missing
            
            # For CLI tools like Aider, we'd need a different approach
            elif env_name == "aider" and "cli_tools" in self.extensions and "aider" in self.extensions["cli_tools"]:
                # For CLI tools, we'd need to check if Python packages are installed
                # This is a simplified version - in a real implementation, you'd check each package
                self.missing_extensions[env_name] = self.extensions["cli_tools"]["aider"]
        
        return self.missing_extensions
    
    def install_vscode_extension(self, vscode_path, extension_id):
        """Install a VSCode extension."""
        try:
            print(f"Installing extension: {extension_id}")
            result = subprocess.run([vscode_path, "--install-extension", extension_id], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Successfully installed {extension_id}")
                return True
            else:
                print(f"Failed to install {extension_id}: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error installing {extension_id}: {e}")
            return False
    
    def install_cli_tool(self, tool_name, install_command):
        """Install a CLI tool."""
        try:
            print(f"Installing tool: {tool_name}")
            result = subprocess.run(install_command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Successfully installed {tool_name}")
                return True
            else:
                print(f"Failed to install {tool_name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error installing {tool_name}: {e}")
            return False
    
    def install_selected_extensions(self, selections):
        """Install the selected extensions."""
        results = {"success": [], "failed": []}
        
        for env_name, categories in selections.items():
            if env_name == "vscode":
                vscode_path = self.detect_vscode()
                if not vscode_path:
                    print("VSCode not found, skipping extension installation")
                    continue
                
                for category, extensions in categories.items():
                    for ext_id in extensions:
                        if self.install_vscode_extension(vscode_path, ext_id):
                            results["success"].append(f"VSCode: {ext_id}")
                        else:
                            results["failed"].append(f"VSCode: {ext_id}")
            
            elif env_name == "vscode_insiders":
                vscode_path = self.detect_vscode_insiders()
                if not vscode_path:
                    print("VSCode Insiders not found, skipping extension installation")
                    continue
                
                for category, extensions in categories.items():
                    for ext_id in extensions:
                        if self.install_vscode_extension(vscode_path, ext_id):
                            results["success"].append(f"VSCode Insiders: {ext_id}")
                        else:
                            results["failed"].append(f"VSCode Insiders: {ext_id}")
            
            elif env_name == "aider":
                for category, tools in categories.items():
                    for tool in tools:
                        if self.install_cli_tool(tool["name"], tool["install_command"]):
                            results["success"].append(f"Aider: {tool['name']}")
                        else:
                            results["failed"].append(f"Aider: {tool['name']}")
        
        return results

# Example usage
if __name__ == "__main__":
    # Path to the extensions configuration file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "recommended_extensions.json")
    
    # Initialize the extension manager
    manager = ExtensionManager(config_path)
    
    # Detect installed environments
    environments = manager.detect_all_environments()
    print("Detected environments:")
    for env_name, env_path in environments.items():
        print(f"  - {env_name}: {env_path}")
    
    # Detect missing extensions
    missing = manager.detect_missing_extensions()
    print("\nMissing extensions:")
    for env_name, categories in missing.items():
        print(f"  {env_name}:")
        for category, extensions in categories.items():
            print(f"    {category}:")
            for ext in extensions:
                if "id" in ext:
                    print(f"      - {ext['name']} ({ext['id']})")
                else:
                    print(f"      - {ext['name']}")
    
    # In a real implementation, you'd prompt the user to select which extensions to install
    # For this example, we'll just print the detection results
    print("\nRun this script with the --install flag to install missing extensions")
    
    # Check if --install flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        # In a real implementation, you'd prompt the user to select which extensions to install
        # For this example, we'll install all missing extensions
        selections = {}
        for env_name, categories in missing.items():
            selections[env_name] = {}
            for category, extensions in categories.items():
                if env_name in ["vscode", "vscode_insiders"]:
                    selections[env_name][category] = [ext["id"] for ext in extensions if "id" in ext]
                else:
                    selections[env_name][category] = extensions
        
        # Install selected extensions
        results = manager.install_selected_extensions(selections)
        
        print("\nInstallation results:")
        print("  Successful installations:")
        for ext in results["success"]:
            print(f"    - {ext}")
        
        print("  Failed installations:")
        for ext in results["failed"]:
            print(f"    - {ext}")
