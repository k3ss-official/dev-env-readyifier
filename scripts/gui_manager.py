#!/usr/bin/env python3
"""
gui_manager.py - GUI interface for Dev Environment Readyifier

This module provides a graphical user interface for the setup process,
allowing users to visually select tools, view installation status,
and manage the configuration process.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Dict, List, Any, Optional, Callable

# Add parent directory to path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.detector import EnvironmentDetector
from scripts.configurator import ConfigurationManager
from scripts.installer import ToolInstaller

class ReadyifierGUI:
    """GUI interface for the Dev Environment Readyifier."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dev Environment Readyifier")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Set up styles
        self.setup_styles()
        
        # Initialize variables
        self.detection_results = {}
        self.config_choices = {
            "selected_tools": {},
            "tools_to_install": {},
            "security_level": "standard",
            "ai_personality": "default",
            "reference_structure": True
        }
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create content area with notebook
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.create_welcome_tab()
        self.create_detection_tab()
        self.create_selection_tab()
        self.create_configuration_tab()
        self.create_installation_tab()
        self.create_summary_tab()
        
        # Disable all tabs except welcome
        for i in range(1, self.notebook.index("end")):
            self.notebook.tab(i, state="disabled")
        
        # Create footer with navigation buttons
        self.create_footer()
        
        # Initialize detector
        self.detector = EnvironmentDetector()
    
    def setup_styles(self):
        """Set up styles for the GUI."""
        self.style = ttk.Style()
        
        # Configure colors
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5")
        self.style.configure("TNotebook", background="#f5f5f5")
        self.style.configure("TNotebook.Tab", padding=[10, 5], font=('Arial', 10))
        
        # Configure button styles
        self.style.configure("TButton", padding=10, font=('Arial', 10))
        self.style.configure("Primary.TButton", background="#4a86e8")
        
        # Configure header styles
        self.style.configure("Header.TLabel", font=('Arial', 16, 'bold'))
        self.style.configure("Subheader.TLabel", font=('Arial', 12))
        
        # Configure tool item styles
        self.style.configure("Tool.TFrame", padding=10, relief="solid", borderwidth=1)
        self.style.configure("ToolName.TLabel", font=('Arial', 12, 'bold'))
        self.style.configure("ToolVersion.TLabel", font=('Arial', 10))
        self.style.configure("ToolStatus.TLabel", font=('Arial', 10, 'italic'))
    
    def create_header(self):
        """Create the header section."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame, 
            text="Development Environment Readyifier", 
            style="Header.TLabel"
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            header_frame, 
            text="Configure your development environment with optimal settings, security, and AI rules", 
            style="Subheader.TLabel"
        )
        subtitle_label.pack()
    
    def create_footer(self):
        """Create the footer with navigation buttons."""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Back button
        self.back_button = ttk.Button(
            footer_frame, 
            text="Back", 
            command=self.go_back,
            state="disabled"
        )
        self.back_button.pack(side=tk.LEFT)
        
        # Next button
        self.next_button = ttk.Button(
            footer_frame, 
            text="Next", 
            command=self.go_next,
            style="Primary.TButton"
        )
        self.next_button.pack(side=tk.RIGHT)
    
    def create_welcome_tab(self):
        """Create the welcome tab."""
        welcome_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(welcome_frame, text="Welcome")
        
        # Welcome message
        welcome_label = ttk.Label(
            welcome_frame, 
            text="Welcome to the Development Environment Readyifier!",
            style="Header.TLabel"
        )
        welcome_label.pack(pady=(0, 20))
        
        welcome_text = (
            "This tool will help you set up your development environment with optimal "
            "settings, security hardening, and AI assistant configurations.\n\n"
            "The process includes:\n"
            "1. Detecting installed tools and environments\n"
            "2. Selecting which tools to configure or install\n"
            "3. Customizing security and AI assistant settings\n"
            "4. Installing missing tools and applying configurations\n\n"
            "Click 'Next' to begin the detection process."
        )
        
        description_label = ttk.Label(
            welcome_frame, 
            text=welcome_text,
            wraplength=700,
            justify="left"
        )
        description_label.pack(fill=tk.BOTH, expand=True)
    
    def create_detection_tab(self):
        """Create the detection tab."""
        detection_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(detection_frame, text="Detection")
        
        # Header
        header_label = ttk.Label(
            detection_frame, 
            text="Detecting Your Environment",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Progress frame
        progress_frame = ttk.Frame(detection_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(
            progress_frame, 
            text="Preparing to scan your system...",
        )
        self.progress_label.pack(side=tk.LEFT, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            orient="horizontal", 
            length=300, 
            mode="determinate"
        )
        self.progress_bar.pack(side=tk.RIGHT, pady=5)
        
        # Results frame (will be populated during detection)
        self.detection_results_frame = ttk.Frame(detection_frame)
        self.detection_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def create_selection_tab(self):
        """Create the tool selection tab."""
        selection_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(selection_frame, text="Tool Selection")
        
        # Header
        header_label = ttk.Label(
            selection_frame, 
            text="Select Tools to Configure or Install",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Description
        description_label = ttk.Label(
            selection_frame, 
            text="Select which tools you want to configure. You can also choose to install missing tools.",
            wraplength=700
        )
        description_label.pack(pady=(0, 10))
        
        # Create scrollable frame for tools
        tools_canvas = tk.Canvas(selection_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=tools_canvas.yview)
        
        tools_canvas.configure(yscrollcommand=scrollbar.set)
        tools_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tools_frame = ttk.Frame(tools_canvas)
        tools_canvas.create_window((0, 0), window=self.tools_frame, anchor="nw")
        
        self.tools_frame.bind(
            "<Configure>",
            lambda e: tools_canvas.configure(
                scrollregion=tools_canvas.bbox("all"),
                width=selection_frame.winfo_width() - 30
            )
        )
        
        # Add "Select All" buttons
        select_all_frame = ttk.Frame(self.tools_frame)
        select_all_frame.pack(fill=tk.X, pady=(0, 10))
        
        select_all_config_button = ttk.Button(
            select_all_frame,
            text="Select All for Configuration",
            command=lambda: self.select_all_tools(True, "config")
        )
        select_all_config_button.pack(side=tk.LEFT, padx=5)
        
        select_all_install_button = ttk.Button(
            select_all_frame,
            text="Select All for Installation",
            command=lambda: self.select_all_tools(True, "install")
        )
        select_all_install_button.pack(side=tk.LEFT, padx=5)
        
        clear_all_button = ttk.Button(
            select_all_frame,
            text="Clear All Selections",
            command=lambda: self.select_all_tools(False, "both")
        )
        clear_all_button.pack(side=tk.RIGHT, padx=5)
    
    def create_configuration_tab(self):
        """Create the configuration tab."""
        config_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(config_frame, text="Configuration")
        
        # Header
        header_label = ttk.Label(
            config_frame, 
            text="Configure Settings",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Security level
        security_frame = ttk.LabelFrame(config_frame, text="Security Level", padding=10)
        security_frame.pack(fill=tk.X, pady=10)
        
        self.security_var = tk.StringVar(value="standard")
        
        standard_radio = ttk.Radiobutton(
            security_frame,
            text="Standard - Recommended security practices",
            variable=self.security_var,
            value="standard"
        )
        standard_radio.pack(anchor=tk.W, pady=5)
        
        enhanced_radio = ttk.Radiobutton(
            security_frame,
            text="Enhanced - Additional security measures and hardening",
            variable=self.security_var,
            value="enhanced"
        )
        enhanced_radio.pack(anchor=tk.W, pady=5)
        
        # AI Personality
        ai_frame = ttk.LabelFrame(config_frame, text="AI Assistant Personality", padding=10)
        ai_frame.pack(fill=tk.X, pady=10)
        
        self.ai_var = tk.StringVar(value="default")
        
        default_radio = ttk.Radiobutton(
            ai_frame,
            text="Default - Based on provided personality profile",
            variable=self.ai_var,
            value="default"
        )
        default_radio.pack(anchor=tk.W, pady=5)
        
        custom_radio = ttk.Radiobutton(
            ai_frame,
            text="Custom - Modify personality traits",
            variable=self.ai_var,
            value="custom",
            command=self.show_custom_personality_dialog
        )
        custom_radio.pack(anchor=tk.W, pady=5)
        
        # Reference Structure
        ref_frame = ttk.LabelFrame(config_frame, text="Reference Data Structure", padding=10)
        ref_frame.pack(fill=tk.X, pady=10)
        
        self.ref_var = tk.BooleanVar(value=True)
        
        ref_check = ttk.Checkbutton(
            ref_frame,
            text="Create reference data structure for projects",
            variable=self.ref_var
        )
        ref_check.pack(anchor=tk.W, pady=5)
        
        ref_description = ttk.Label(
            ref_frame,
            text="This will create a standardized directory structure for organizing reference data, including organization info, technical specifications, security policies, API documentation, and workflow processes.",
            wraplength=700
        )
        ref_description.pack(anchor=tk.W, pady=5)
    
    def create_installation_tab(self):
        """Create the installation tab."""
        install_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(install_frame, text="Installation")
        
        # Header
        header_label = ttk.Label(
            install_frame, 
            text="Installing and Configuring",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Progress frame
        progress_frame = ttk.Frame(install_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.install_progress_label = ttk.Label(
            progress_frame, 
            text="Preparing installation...",
        )
        self.install_progress_label.pack(side=tk.LEFT, pady=5)
        
        self.install_progress_bar = ttk.Progressbar(
            progress_frame, 
            orient="horizontal", 
            length=300, 
            mode="determinate"
        )
        self.install_progress_bar.pack(side=tk.RIGHT, pady=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(install_frame, text="Installation Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.config(state=tk.DISABLED)
    
    def create_summary_tab(self):
        """Create the summary tab."""
        summary_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(summary_frame, text="Summary")
        
        # Header
        header_label = ttk.Label(
            summary_frame, 
            text="Setup Complete",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Summary text
        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD, height=20)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        summary_scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=self.summary_text.yview)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
        self.summary_text.config(state=tk.DISABLED)
    
    def go_next(self):
        """Handle next button click."""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # Welcome tab
            self.start_detection()
        elif current_tab == 1:  # Detection tab
            self.populate_selection_tab()
            self.notebook.tab(2, state="normal")
            self.notebook.select(2)
            self.back_button.config(state="normal")
        elif current_tab == 2:  # Selection tab
            self.update_config_from_selection()
            self.notebook.tab(3, state="normal")
            self.notebook.select(3)
        elif current_tab == 3:  # Configuration tab
            self.update_config_from_settings()
            self.notebook.tab(4, state="normal")
            self.notebook.select(4)
            self.start_installation()
        elif current_tab == 4:  # Installation tab
            self.notebook.tab(5, state="normal")
            self.notebook.select(5)
            self.next_button.config(text="Finish", command=self.finish)
        
    def go_back(self):
        """Handle back button click."""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab > 0:
            self.notebook.select(current_tab - 1)
            
            if current_tab - 1 == 0:
                self.back_button.config(state="disabled")
            
            if current_tab == 5:
                self.next_button.config(text="Next", command=self.go_next)
    
    def start_detection(self):
        """Start the detection process."""
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)
        self.back_button.config(state="normal")
        
        # Update progress
        self.progress_label.config(text="Scanning your system...")
        self.progress_bar["value"] = 10
        self.root.update()
        
        # Run detection
        self.detection_results = self.detector.detect_all()
        
        # Update progress
        self.progress_bar["value"] = 100
        self.progress_label.config(text="Detection complete!")
        
        # Display results
        self.display_detection_results()
    
    def display_detection_results(self):
        """Display detection results in the detection tab."""
        # Clear previous results
        for widget in self.detection_results_frame.winfo_children():
            widget.destroy()
        
        # OS Info
        os_frame = ttk.LabelFrame(self.detection_results_frame, text="System Information", padding=10)
        os_frame.pack(fill=tk.X, pady=5)
        
        os_info = self.detection_results.get("os_info", {})
        os_text = f"OS: {os_info.get('system', 'Unknown')} {os_info.get('release', '')}\n"
        os_text += f"Python: {os_info.get('python_version', 'Unknown')}"
        
        os_label = ttk.Label(os_frame, text=os_text)
        os_label.pack(anchor=tk.W)
        
        # IDEs
        ide_frame = ttk.LabelFrame(self.detection_results_frame, text="Detected IDEs", padding=10)
        ide_frame.pack(fill=tk.X, pady=5)
        
        ides = self.detection_results.get("ides", {})
        if not ides:
            ttk.Label(ide_frame, text="No IDEs detected").pack(anchor=tk.W)
        else:
            for ide, info in ides.items():
                ide_text = f"{ide.upper()}: {info.get('version', 'Unknown version')}"
                ttk.Label(ide_frame, text=ide_text).pack(anchor=tk.W)
        
        # AI Tools
        ai_frame = ttk.LabelFrame(self.detection_results_frame, text="Detected AI Tools", padding=10)
        ai_frame.pack(fill=tk.X, pady=5)
        
        ai_tools = self.detection_results.get("ai_tools", {})
        if not ai_tools:
            ttk.Label(ai_frame, text="No AI tools detected").pack(anchor=tk.W)
        else:
            for tool, info in ai_tools.items():
                tool_text = f"{tool.upper()}: {info.get('version', 'Unknown version')}"
                ttk.Label(ai_frame, text=tool_text).pack(anchor=tk.W)
        
        # Conda Environments
        conda_frame = ttk.LabelFrame(self.detection_results_frame, text="Conda Environments", padding=10)
        conda_frame.pack(fill=tk.X, pady=5)
        
        conda_envs = self.detection_results.get("conda_environments", [])
        if not conda_envs:
            ttk.Label(conda_frame, text="No Conda environments detected").pack(anchor=tk.W)
        else:
            for env in conda_envs:
                env_text = f"{env.get('name', 'Unknown')}"
                ttk.Label(conda_frame, text=env_text).pack(anchor=tk.W)
        
        # VS Code Extensions
        if self.detection_results.get("vscode_extensions"):
            ext_frame = ttk.LabelFrame(self.detection_results_frame, text="VS Code Extensions", padding=10)
            ext_frame.pack(fill=tk.X, pady=5)
            
            ext_count = len(self.detection_results.get("vscode_extensions", []))
            ttk.Label(ext_frame, text=f"{ext_count} extensions detected").pack(anchor=tk.W)
    
    def populate_selection_tab(self):
        """Populate the tool selection tab with detected and available tools."""
        # Clear previous content
        for widget in self.tools_frame.winfo_children():
            if widget != self.tools_frame.winfo_children()[0]:  # Keep the "Select All" frame
                widget.destroy()
        
        # Define all available tools
        all_tools = {
            "ides": {
                "vscode": "Visual Studio Code",
                "vscode_insiders": "Visual Studio Code Insiders",
                "trae": "Trae IDE",
                "void": "VOID IDE"
            },
            "ai_tools": {
                "cline": "Cline",
                "roo": "Roo Code",
                "aider": "Aider"
            }
        }
        
        # Create variables for checkboxes
        self.config_vars = {}
        self.install_vars = {}
        
        # Add IDE section
        ide_frame = ttk.LabelFrame(self.tools_frame, text="IDEs", padding=10)
        ide_frame.pack(fill=tk.X, pady=5)
        
        detected_ides = self.detection_results.get("ides", {})
        
        for ide_key, ide_name in all_tools["ides"].items():
            is_installed = ide_key in detected_ides
            version = detected_ides.get(ide_key, {}).get("version", "Not installed")
            
            self.add_tool_item(
                ide_frame, 
                ide_key, 
                ide_name, 
                version, 
                is_installed
            )
        
        # Add AI Tools section
        ai_frame = ttk.LabelFrame(self.tools_frame, text="AI Tools", padding=10)
        ai_frame.pack(fill=tk.X, pady=5)
        
        detected_ai_tools = self.detection_results.get("ai_tools", {})
        
        for tool_key, tool_name in all_tools["ai_tools"].items():
            is_installed = tool_key in detected_ai_tools
            version = detected_ai_tools.get(tool_key, {}).get("version", "Not installed")
            
            self.add_tool_item(
                ai_frame, 
                tool_key, 
                tool_name, 
                version, 
                is_installed
            )
    
    def add_tool_item(self, parent, tool_key, tool_name, version, is_installed):
        """Add a tool item to the selection tab."""
        tool_frame = ttk.Frame(parent, style="Tool.TFrame")
        tool_frame.pack(fill=tk.X, pady=5)
        
        # Tool info
        info_frame = ttk.Frame(tool_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        name_label = ttk.Label(
            info_frame, 
            text=tool_name,
            style="ToolName.TLabel"
        )
        name_label.pack(anchor=tk.W)
        
        version_text = f"Version: {version}"
        version_label = ttk.Label(
            info_frame, 
            text=version_text,
            style="ToolVersion.TLabel"
        )
        version_label.pack(anchor=tk.W)
        
        status_text = "Installed" if is_installed else "Not installed"
        status_color = "green" if is_installed else "red"
        
        status_label = ttk.Label(
            info_frame, 
            text=f"Status: {status_text}",
            foreground=status_color,
            style="ToolStatus.TLabel"
        )
        status_label.pack(anchor=tk.W)
        
        # Checkboxes
        checkbox_frame = ttk.Frame(tool_frame)
        checkbox_frame.pack(side=tk.RIGHT, padx=10)
        
        # Configure checkbox
        self.config_vars[tool_key] = tk.BooleanVar(value=is_installed)
        config_check = ttk.Checkbutton(
            checkbox_frame,
            text="Configure",
            variable=self.config_vars[tool_key]
        )
        config_check.pack(anchor=tk.E, pady=2)
        
        # Install checkbox (only for non-installed tools)
        self.install_vars[tool_key] = tk.BooleanVar(value=False)
        install_check = ttk.Checkbutton(
            checkbox_frame,
            text="Install",
            variable=self.install_vars[tool_key],
            state="normal" if not is_installed else "disabled"
        )
        install_check.pack(anchor=tk.E, pady=2)
    
    def select_all_tools(self, value, selection_type):
        """Select or deselect all tools."""
        if selection_type in ["config", "both"]:
            for var in self.config_vars.values():
                var.set(value)
        
        if selection_type in ["install", "both"]:
            for key, var in self.install_vars.items():
                # Only set if the tool is not installed
                is_installed = (
                    key in self.detection_results.get("ides", {}) or 
                    key in self.detection_results.get("ai_tools", {})
                )
                if not is_installed:
                    var.set(value)
    
    def update_config_from_selection(self):
        """Update configuration based on tool selection."""
        selected_tools = {}
        tools_to_install = {}
        
        for tool_key, var in self.config_vars.items():
            selected_tools[tool_key] = var.get()
        
        for tool_key, var in self.install_vars.items():
            tools_to_install[tool_key] = var.get()
        
        self.config_choices["selected_tools"] = selected_tools
        self.config_choices["tools_to_install"] = tools_to_install
    
    def update_config_from_settings(self):
        """Update configuration based on settings tab."""
        self.config_choices["security_level"] = self.security_var.get()
        self.config_choices["ai_personality"] = self.ai_var.get()
        self.config_choices["reference_structure"] = self.ref_var.get()
    
    def show_custom_personality_dialog(self):
        """Show dialog for customizing AI personality."""
        # This is a placeholder - would implement detailed customization
        messagebox.showinfo(
            "Custom Personality",
            "Custom personality configuration will be available in a future version. "
            "Using default personality profile for now."
        )
        self.ai_var.set("default")
    
    def start_installation(self):
        """Start the installation and configuration process."""
        # Update UI
        self.install_progress_label.config(text="Preparing installation...")
        self.install_progress_bar["value"] = 0
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
        # Log initial message
        self.log_message("Starting installation and configuration process...")
        
        # Get tools to install
        tools_to_install = [
            tool for tool, install in self.config_choices["tools_to_install"].items() 
            if install
        ]
        
        # Create installer
        installer = ToolInstaller(self.detection_results, self.config_choices)
        
        # Install missing tools
        if tools_to_install:
            self.install_progress_label.config(text="Installing missing tools...")
            self.install_progress_bar["value"] = 10
            self.root.update()
            
            self.log_message(f"Installing {len(tools_to_install)} missing tools...")
            
            for i, tool in enumerate(tools_to_install):
                self.log_message(f"Installing {tool}...")
                success = installer._install_tool(tool)
                
                if success:
                    self.log_message(f"✓ Successfully installed {tool}")
                else:
                    self.log_message(f"✗ Failed to install {tool}")
                
                # Update progress
                progress = 10 + (i + 1) * 30 / len(tools_to_install)
                self.install_progress_bar["value"] = progress
                self.root.update()
        else:
            self.install_progress_bar["value"] = 40
            self.log_message("No tools selected for installation.")
        
        # Apply configurations
        self.install_progress_label.config(text="Applying configurations...")
        self.root.update()
        
        self.log_message("\nApplying configurations...")
        
        selected_tools = [
            tool for tool, selected in self.config_choices["selected_tools"].items() 
            if selected
        ]
        
        if selected_tools:
            for i, tool in enumerate(selected_tools):
                self.log_message(f"Configuring {tool}...")
                success = installer._apply_tool_config(tool)
                
                if success:
                    self.log_message(f"✓ Successfully configured {tool}")
                else:
                    self.log_message(f"✗ Failed to configure {tool}")
                
                # Update progress
                progress = 40 + (i + 1) * 50 / len(selected_tools)
                self.install_progress_bar["value"] = progress
                self.root.update()
        else:
            self.install_progress_bar["value"] = 90
            self.log_message("No tools selected for configuration.")
        
        # Set up reference structure if selected
        if self.config_choices["reference_structure"]:
            self.install_progress_label.config(text="Setting up reference structure...")
            self.install_progress_bar["value"] = 90
            self.root.update()
            
            self.log_message("\nSetting up reference data structure...")
            success = installer._setup_reference_structure()
            
            if success:
                self.log_message("✓ Successfully set up reference structure")
            else:
                self.log_message("✗ Failed to set up reference structure")
        
        # Complete
        self.install_progress_label.config(text="Installation complete!")
        self.install_progress_bar["value"] = 100
        self.log_message("\nInstallation and configuration process completed!")
        
        # Prepare summary
        self.prepare_summary()
    
    def log_message(self, message):
        """Add a message to the installation log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def prepare_summary(self):
        """Prepare the summary tab content."""
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        # Add header
        self.summary_text.insert(tk.END, "INSTALLATION AND CONFIGURATION SUMMARY\n\n", "header")
        
        # Add installed tools
        installed_tools = [
            tool for tool, install in self.config_choices["tools_to_install"].items() 
            if install
        ]
        
        if installed_tools:
            self.summary_text.insert(tk.END, "Installed Tools:\n", "section")
            for tool in installed_tools:
                self.summary_text.insert(tk.END, f"✓ {tool}\n", "item")
        else:
            self.summary_text.insert(tk.END, "No tools were installed.\n", "section")
        
        # Add configured tools
        configured_tools = [
            tool for tool, selected in self.config_choices["selected_tools"].items() 
            if selected
        ]
        
        if configured_tools:
            self.summary_text.insert(tk.END, "\nConfigured Tools:\n", "section")
            for tool in configured_tools:
                self.summary_text.insert(tk.END, f"✓ {tool}\n", "item")
        else:
            self.summary_text.insert(tk.END, "\nNo tools were configured.\n", "section")
        
        # Add configuration details
        self.summary_text.insert(tk.END, "\nConfiguration Details:\n", "section")
        self.summary_text.insert(tk.END, f"Security Level: {self.config_choices['security_level'].upper()}\n", "item")
        self.summary_text.insert(tk.END, f"AI Personality: {self.config_choices['ai_personality'].upper()}\n", "item")
        
        if self.config_choices["reference_structure"]:
            self.summary_text.insert(tk.END, "Reference Structure: Created\n", "item")
        else:
            self.summary_text.insert(tk.END, "Reference Structure: Not created\n", "item")
        
        # Add next steps
        self.summary_text.insert(tk.END, "\nNext Steps:\n", "section")
        self.summary_text.insert(tk.END, "1. Restart any IDEs that were configured\n", "item")
        self.summary_text.insert(tk.END, "2. Test the installed extensions and configurations\n", "item")
        self.summary_text.insert(tk.END, "3. Review the reference structure if it was created\n", "item")
        
        # Add footer
        self.summary_text.insert(tk.END, "\nThank you for using the Development Environment Readyifier!\n", "footer")
        
        # Configure text tags
        self.summary_text.tag_configure("header", font=("Arial", 14, "bold"))
        self.summary_text.tag_configure("section", font=("Arial", 12, "bold"))
        self.summary_text.tag_configure("item", font=("Arial", 10))
        self.summary_text.tag_configure("footer", font=("Arial", 12, "italic"))
        
        self.summary_text.config(state=tk.DISABLED)
    
    def finish(self):
        """Finish the setup process and exit."""
        messagebox.showinfo(
            "Setup Complete",
            "The development environment setup is complete. "
            "Thank you for using the Development Environment Readyifier!"
        )
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReadyifierGUI(root)
    root.mainloop()
