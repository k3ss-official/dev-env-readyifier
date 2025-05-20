#!/usr/bin/env python3
"""
detector.py - Tool detection module for Dev Environment Readyifier

This module scans the system for installed IDEs, AI tools, and extensions.
It provides a comprehensive inventory of what's available for configuration.
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class EnvironmentDetector:
    """Detects installed development tools and environments."""
    
    def __init__(self):
        self.os_type = platform.system()
        self.detected_tools = {}
        self.conda_environments = []
        self.vscode_extensions = []
        
    def detect_all(self) -> Dict:
        """Run all detection methods and return comprehensive results."""
        print("Scanning system for installed development tools...")
        
        self.detect_os_info()
        self.detect_ides()
        self.detect_ai_tools()
        self.detect_conda_environments()
        self.detect_vscode_extensions()
        
        return {
            "os_info": self.os_info,
            "ides": self.detected_tools.get("ides", {}),
            "ai_tools": self.detected_tools.get("ai_tools", {}),
            "conda_environments": self.conda_environments,
            "vscode_extensions": self.vscode_extensions
        }
    
    def detect_os_info(self) -> Dict:
        """Detect operating system information."""
        self.os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
        return self.os_info
    
    def detect_ides(self) -> Dict:
        """Detect installed IDEs."""
        ides = {}
        
        # VS Code detection
        vscode_paths = self._find_vscode_installations()
        if vscode_paths:
            ides["vscode"] = {
                "installed": True,
                "paths": vscode_paths,
                "version": self._get_vscode_version(vscode_paths[0]) if vscode_paths else None
            }
        
        # VS Code Insiders detection
        vscode_insiders_paths = self._find_vscode_insiders_installations()
        if vscode_insiders_paths:
            ides["vscode_insiders"] = {
                "installed": True,
                "paths": vscode_insiders_paths,
                "version": self._get_vscode_version(vscode_insiders_paths[0]) if vscode_insiders_paths else None
            }
        
        # Trae IDE detection
        trae_paths = self._find_trae_installations()
        if trae_paths:
            ides["trae"] = {
                "installed": True,
                "paths": trae_paths,
                "version": self._get_generic_version("trae")
            }
        
        # VOID IDE detection
        void_paths = self._find_void_installations()
        if void_paths:
            ides["void"] = {
                "installed": True,
                "paths": void_paths,
                "version": self._get_generic_version("void")
            }
        
        self.detected_tools["ides"] = ides
        return ides
    
    def detect_ai_tools(self) -> Dict:
        """Detect installed AI coding tools."""
        ai_tools = {}
        
        # Cline detection
        cline_path = self._find_executable("cline")
        if cline_path:
            ai_tools["cline"] = {
                "installed": True,
                "path": cline_path,
                "version": self._get_cli_version("cline --version")
            }
        
        # Roo Code detection
        roo_path = self._find_executable("roo")
        if roo_path:
            ai_tools["roo"] = {
                "installed": True,
                "path": roo_path,
                "version": self._get_cli_version("roo --version")
            }
        
        # Aider detection
        aider_path = self._find_executable("aider")
        if aider_path:
            ai_tools["aider"] = {
                "installed": True,
                "path": aider_path,
                "version": self._get_cli_version("aider --version")
            }
        
        self.detected_tools["ai_tools"] = ai_tools
        return ai_tools
    
    def detect_conda_environments(self) -> List[Dict]:
        """Detect Conda environments."""
        try:
            # Check if conda is installed
            conda_path = self._find_executable("conda")
            if not conda_path:
                return []
            
            # Get list of conda environments
            result = subprocess.run(
                ["conda", "env", "list", "--json"], 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if result.returncode == 0:
                env_data = json.loads(result.stdout)
                self.conda_environments = [
                    {
                        "name": env.split('/')[-1] if '/' in env else env,
                        "path": env
                    }
                    for env in env_data.get("envs", [])
                ]
            
            return self.conda_environments
        except Exception as e:
            print(f"Error detecting conda environments: {e}")
            return []
    
    def detect_vscode_extensions(self) -> List[Dict]:
        """Detect installed VS Code extensions."""
        try:
            vscode_paths = self._find_vscode_installations()
            if not vscode_paths:
                return []
            
            # Try to get extensions using code CLI
            result = subprocess.run(
                ["code", "--list-extensions"], 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if result.returncode == 0:
                extensions = result.stdout.strip().split('\n')
                self.vscode_extensions = [
                    {"id": ext, "name": ext.split('.')[-1]} 
                    for ext in extensions if ext
                ]
            
            return self.vscode_extensions
        except Exception as e:
            print(f"Error detecting VS Code extensions: {e}")
            return []
    
    def _find_vscode_installations(self) -> List[str]:
        """Find VS Code installation paths."""
        paths = []
        
        if self.os_type == "Darwin":  # macOS
            app_paths = [
                "/Applications/Visual Studio Code.app",
                str(Path.home() / "Applications/Visual Studio Code.app")
            ]
            paths = [p for p in app_paths if os.path.exists(p)]
            
        elif self.os_type == "Linux":
            # Check common Linux installation paths
            possible_paths = [
                "/usr/bin/code",
                "/usr/local/bin/code",
                str(Path.home() / ".local/bin/code")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
            
        elif self.os_type == "Windows":
            # Check common Windows installation paths
            possible_paths = [
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                str(Path.home() / "AppData/Local/Programs/Microsoft VS Code/Code.exe")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
        
        return paths
    
    def _find_vscode_insiders_installations(self) -> List[str]:
        """Find VS Code Insiders installation paths."""
        paths = []
        
        if self.os_type == "Darwin":  # macOS
            app_paths = [
                "/Applications/Visual Studio Code - Insiders.app",
                str(Path.home() / "Applications/Visual Studio Code - Insiders.app")
            ]
            paths = [p for p in app_paths if os.path.exists(p)]
            
        elif self.os_type == "Linux":
            # Check common Linux installation paths
            possible_paths = [
                "/usr/bin/code-insiders",
                "/usr/local/bin/code-insiders",
                str(Path.home() / ".local/bin/code-insiders")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
            
        elif self.os_type == "Windows":
            # Check common Windows installation paths
            possible_paths = [
                r"C:\Program Files\Microsoft VS Code Insiders\Code - Insiders.exe",
                r"C:\Program Files (x86)\Microsoft VS Code Insiders\Code - Insiders.exe",
                str(Path.home() / "AppData/Local/Programs/Microsoft VS Code Insiders/Code - Insiders.exe")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
        
        return paths
    
    def _find_trae_installations(self) -> List[str]:
        """Find Trae IDE installation paths."""
        # This is a placeholder - adjust based on actual Trae IDE installation paths
        paths = []
        
        if self.os_type == "Darwin":  # macOS
            app_paths = [
                "/Applications/Trae.app",
                str(Path.home() / "Applications/Trae.app")
            ]
            paths = [p for p in app_paths if os.path.exists(p)]
            
        elif self.os_type == "Linux":
            # Check common Linux installation paths
            possible_paths = [
                "/usr/bin/trae",
                "/usr/local/bin/trae",
                str(Path.home() / ".local/bin/trae")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
            
        elif self.os_type == "Windows":
            # Check common Windows installation paths
            possible_paths = [
                r"C:\Program Files\Trae\Trae.exe",
                r"C:\Program Files (x86)\Trae\Trae.exe",
                str(Path.home() / "AppData/Local/Programs/Trae/Trae.exe")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
        
        return paths
    
    def _find_void_installations(self) -> List[str]:
        """Find VOID IDE installation paths."""
        # This is a placeholder - adjust based on actual VOID IDE installation paths
        paths = []
        
        if self.os_type == "Darwin":  # macOS
            app_paths = [
                "/Applications/VOID.app",
                str(Path.home() / "Applications/VOID.app")
            ]
            paths = [p for p in app_paths if os.path.exists(p)]
            
        elif self.os_type == "Linux":
            # Check common Linux installation paths
            possible_paths = [
                "/usr/bin/void",
                "/usr/local/bin/void",
                str(Path.home() / ".local/bin/void")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
            
        elif self.os_type == "Windows":
            # Check common Windows installation paths
            possible_paths = [
                r"C:\Program Files\VOID\VOID.exe",
                r"C:\Program Files (x86)\VOID\VOID.exe",
                str(Path.home() / "AppData/Local/Programs/VOID/VOID.exe")
            ]
            paths = [p for p in possible_paths if os.path.exists(p)]
        
        return paths
    
    def _find_executable(self, name: str) -> Optional[str]:
        """Find an executable in PATH."""
        try:
            if self.os_type == "Windows":
                # On Windows, check if the command exists using where
                result = subprocess.run(
                    ["where", name], 
                    capture_output=True, 
                    text=True, 
                    check=False
                )
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            else:
                # On Unix-like systems, use which
                result = subprocess.run(
                    ["which", name], 
                    capture_output=True, 
                    text=True, 
                    check=False
                )
                if result.returncode == 0:
                    return result.stdout.strip()
        except Exception:
            pass
        
        return None
    
    def _get_vscode_version(self, path: str) -> Optional[str]:
        """Get VS Code version."""
        try:
            if os.path.isdir(path):  # macOS .app bundle
                # For macOS, the executable is inside the .app bundle
                if self.os_type == "Darwin":
                    code_path = os.path.join(path, "Contents/Resources/app/bin/code")
                    if not os.path.exists(code_path):
                        return None
                    
                    result = subprocess.run(
                        [code_path, "--version"], 
                        capture_output=True, 
                        text=True, 
                        check=False
                    )
                    if result.returncode == 0:
                        return result.stdout.strip().split('\n')[0]
            else:
                # Direct executable path
                result = subprocess.run(
                    [path, "--version"], 
                    capture_output=True, 
                    text=True, 
                    check=False
                )
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
        except Exception:
            pass
        
        return None
    
    def _get_cli_version(self, command: str) -> Optional[str]:
        """Get version from CLI tool."""
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True, 
                check=False
            )
            if result.returncode == 0:
                # Try to extract version number (assumes version is in the first line)
                version_line = result.stdout.strip().split('\n')[0]
                return version_line
        except Exception:
            pass
        
        return None
    
    def _get_generic_version(self, name: str) -> Optional[str]:
        """Get version for tools without standard version flags."""
        # This is a placeholder - implement specific version detection logic
        # for tools that don't follow standard --version pattern
        return "Unknown"


if __name__ == "__main__":
    detector = EnvironmentDetector()
    results = detector.detect_all()
    
    print("\n=== System Detection Results ===\n")
    print(f"OS: {results['os_info']['system']} {results['os_info']['release']}")
    print(f"Python: {results['os_info']['python_version']}")
    
    print("\n=== Detected IDEs ===")
    for ide, info in results['ides'].items():
        print(f"✓ {ide.upper()}: {info.get('version', 'Unknown version')}")
    
    print("\n=== Detected AI Tools ===")
    for tool, info in results['ai_tools'].items():
        print(f"✓ {tool.upper()}: {info.get('version', 'Unknown version')}")
    
    print("\n=== Conda Environments ===")
    for env in results['conda_environments']:
        print(f"✓ {env['name']}")
    
    print("\n=== VS Code Extensions ===")
    for ext in results['vscode_extensions'][:5]:  # Show only first 5
        print(f"✓ {ext['id']}")
    
    if len(results['vscode_extensions']) > 5:
        print(f"  ... and {len(results['vscode_extensions']) - 5} more")
    
    print("\nDetection complete!")
