#!/usr/bin/env python3
"""
gui_manager.py - GUI interface for Dev Environment Readyifier

This script provides a graphical user interface for the Dev Environment Readyifier,
making it easy to select which tools to install and configure.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class GUIManager:
    """Manages the graphical user interface for the Dev Environment Readyifier."""
    
    def __init__(self, environments, missing_extensions, large_files, extension_manager, repo_context_manager, file_structure_manager):
        """Initialize the GUI manager with detected environments and missing extensions."""
        self.environments = environments
        self.missing_extensions = missing_extensions
        self.large_files = large_files
        self.extension_manager = extension_manager
        self.repo_context_manager = repo_context_manager
        self.file_structure_manager = file_structure_manager
        
        self.root = None
        self.notebook = None
        self.env_frames = {}
        self.extension_vars = {}
        self.file_vars = {}
        self.md_vars = {}
        
        # Track selected options
        self.selected_extensions = {}
        self.selected_files = []
        self.selected_md_files = []
    
    def run(self):
        """Run the GUI application."""
        self.root = tk.Tk()
        self.root.title("Dev Environment Readyifier")
        self.root.geometry("900x700")
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame, 
            text="Dev Environment Readyifier", 
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self._create_welcome_tab()
        self._create_environments_tab()
        self._create_extensions_tab()
        self._create_file_structure_tab()
        self._create_repo_context_tab()
        self._create_summary_tab()
        
        # Create footer with buttons
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            footer_frame, 
            text="Previous", 
            command=self._previous_tab
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            footer_frame, 
            text="Next", 
            command=self._next_tab
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(
            footer_frame, 
            text="Apply Selected Changes", 
            command=self._apply_changes
        ).pack(side=tk.RIGHT)
        
        # Start the main loop
        self.root.mainloop()
    
    def _create_welcome_tab(self):
        """Create the welcome tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Welcome")
        
        # Welcome message
        ttk.Label(
            tab, 
            text="Welcome to Dev Environment Readyifier!", 
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 10))
        
        ttk.Label(
            tab, 
            text="This tool will help you set up your development environment with best practices.",
            wraplength=600
        ).pack()
        
        # Environment summary
        env_frame = ttk.LabelFrame(tab, text="Detected Environments", padding=10)
        env_frame.pack(fill=tk.X, pady=(20, 10))
        
        if self.environments:
            for i, (env_name, env_info) in enumerate(self.environments.items()):
                ttk.Label(
                    env_frame, 
                    text=f"{env_name}: {env_info.get('path', 'Unknown path')}"
                ).pack(anchor=tk.W)
        else:
            ttk.Label(
                env_frame, 
                text="No development environments detected."
            ).pack(anchor=tk.W)
        
        # Extension summary
        ext_frame = ttk.LabelFrame(tab, text="Extension Status", padding=10)
        ext_frame.pack(fill=tk.X, pady=(10, 10))
        
        if self.missing_extensions:
            total_missing = sum(
                sum(len(exts) for exts in categories.values())
                for categories in self.missing_extensions.values()
            )
            ttk.Label(
                ext_frame, 
                text=f"Found {total_missing} missing extensions across {len(self.missing_extensions)} environments."
            ).pack(anchor=tk.W)
        else:
            ttk.Label(
                ext_frame, 
                text="No missing extensions found."
            ).pack(anchor=tk.W)
        
        # File structure summary
        file_frame = ttk.LabelFrame(tab, text="File Structure Status", padding=10)
        file_frame.pack(fill=tk.X, pady=(10, 10))
        
        if self.large_files:
            ttk.Label(
                file_frame, 
                text=f"Found {len(self.large_files)} files exceeding the recommended 200-line limit."
            ).pack(anchor=tk.W)
        else:
            ttk.Label(
                file_frame, 
                text="No files exceed the 200-line limit."
            ).pack(anchor=tk.W)
        
        # Instructions
        ttk.Label(
            tab, 
            text="Click 'Next' to start configuring your environment.",
            font=("Arial", 10, "italic")
        ).pack(pady=(20, 0))
    
    def _create_environments_tab(self):
        """Create the environments tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Environments")
        
        ttk.Label(
            tab, 
            text="Detected Development Environments", 
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display environments
        if self.environments:
            for env_name, env_info in self.environments.items():
                env_frame = ttk.LabelFrame(scrollable_frame, text=env_name, padding=10)
                env_frame.pack(fill=tk.X, pady=(0, 10))
                
                ttk.Label(
                    env_frame, 
                    text=f"Path: {env_info.get('path', 'Unknown')}"
                ).pack(anchor=tk.W)
                
                ttk.Label(
                    env_frame, 
                    text=f"Version: {env_info.get('version', 'Unknown')}"
                ).pack(anchor=tk.W)
                
                if env_name in self.missing_extensions:
                    total_missing = sum(len(exts) for exts in self.missing_extensions[env_name].values())
                    ttk.Label(
                        env_frame, 
                        text=f"Missing Extensions: {total_missing}"
                    ).pack(anchor=tk.W)
                else:
                    ttk.Label(
                        env_frame, 
                        text="Missing Extensions: 0"
                    ).pack(anchor=tk.W)
        else:
            ttk.Label(
                scrollable_frame, 
                text="No development environments detected."
            ).pack(anchor=tk.W)
    
    def _create_extensions_tab(self):
        """Create the extensions tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Extensions")
        
        ttk.Label(
            tab, 
            text="Missing Extensions", 
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display missing extensions
        if self.missing_extensions:
            for env_name, categories in self.missing_extensions.items():
                env_frame = ttk.LabelFrame(scrollable_frame, text=env_name, padding=10)
                env_frame.pack(fill=tk.X, pady=(0, 10))
                
                self.extension_vars[env_name] = {}
                
                for category, extensions in categories.items():
                    category_frame = ttk.LabelFrame(env_frame, text=category, padding=5)
                    category_frame.pack(fill=tk.X, pady=(0, 5))
                    
                    self.extension_vars[env_name][category] = {}
                    
                    for ext in extensions:
                        var = tk.BooleanVar(value=True)
                        self.extension_vars[env_name][category][ext.get("id", ext.get("name", "Unknown"))] = var
                        
                        ttk.Checkbutton(
                            category_frame, 
                            text=f"{ext.get('name', 'Unknown')} - {ext.get('description', 'No description')}",
                            variable=var
                        ).pack(anchor=tk.W)
        else:
            ttk.Label(
                scrollable_frame, 
                text="No missing extensions found."
            ).pack(anchor=tk.W)
    
    def _create_file_structure_tab(self):
        """Create the file structure tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="File Structure")
        
        ttk.Label(
            tab, 
            text="File Structure Management", 
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # File annotation option
        annotation_frame = ttk.LabelFrame(scrollable_frame, text="File Annotation", padding=10)
        annotation_frame.pack(fill=tk.X, pady=(0, 10))
        
        annotation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            annotation_frame, 
            text="Add filepath and filename as first entry in files",
            variable=annotation_var
        ).pack(anchor=tk.W)
        
        ttk.Label(
            annotation_frame, 
            text="This will add a comment with the filepath and filename to the beginning of each file.",
            wraplength=600
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Large files
        large_files_frame = ttk.LabelFrame(scrollable_frame, text="Large Files", padding=10)
        large_files_frame.pack(fill=tk.X, pady=(0, 10))
        
        if self.large_files:
            ttk.Label(
                large_files_frame, 
                text=f"The following files exceed the recommended 200-line limit:",
                wraplength=600
            ).pack(anchor=tk.W)
            
            for file_path, line_count in self.large_files:
                var = tk.BooleanVar(value=False)
                self.file_vars[file_path] = var
                
                ttk.Checkbutton(
                    large_files_frame, 
                    text=f"{file_path} ({line_count} lines)",
                    variable=var
                ).pack(anchor=tk.W)
            
            ttk.Label(
                large_files_frame, 
                text="Selected files will be analyzed for potential splitting.",
                wraplength=600
            ).pack(anchor=tk.W, pady=(5, 0))
        else:
            ttk.Label(
                large_files_frame, 
                text="No files exceed the 200-line limit."
            ).pack(anchor=tk.W)
    
    def _create_repo_context_tab(self):
        """Create the repository context tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Repo Context")
        
        ttk.Label(
            tab, 
            text="Repository Context Management", 
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Specialized markdown files
        md_frame = ttk.LabelFrame(scrollable_frame, text="Specialized Markdown Files", padding=10)
        md_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            md_frame, 
            text="Create the following specialized markdown files for project documentation:",
            wraplength=600
        ).pack(anchor=tk.W)
        
        for filename, description in self.repo_context_manager.md_files.items():
            var = tk.BooleanVar(value=True)
            self.md_vars[filename] = var
            
            ttk.Checkbutton(
                md_frame, 
                text=f"{filename} - {description}",
                variable=var
            ).pack(anchor=tk.W)
        
        # Repository context prompt
        prompt_frame = ttk.LabelFrame(scrollable_frame, text="Repository Context Prompt", padding=10)
        prompt_frame.pack(fill=tk.X, pady=(0, 10))
        
        prompt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            prompt_frame, 
            text="Generate repository context prompt",
            variable=prompt_var
        ).pack(anchor=tk.W)
        
        ttk.Label(
            prompt_frame, 
            text="This will generate a comprehensive prompt that provides context about your repository for AI assistants.",
            wraplength=600
        ).pack(anchor=tk.W, pady=(5, 0))
    
    def _create_summary_tab(self):
        """Create the summary tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Summary")
        
        ttk.Label(
            tab, 
            text="Summary of Selected Changes", 
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 20))
        
        # Create scrollable frame for summary
        self.summary_canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.summary_canvas.yview)
        self.summary_frame = ttk.Frame(self.summary_canvas)
        
        self.summary_frame.bind(
            "<Configure>",
            lambda e: self.summary_canvas.configure(scrollregion=self.summary_canvas.bbox("all"))
        )
        
        self.summary_canvas.create_window((0, 0), window=self.summary_frame, anchor="nw")
        self.summary_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.summary_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(
            self.summary_frame, 
            text="Click 'Next' to view the summary of selected changes.",
            wraplength=600
        ).pack(anchor=tk.W)
    
    def _update_summary_tab(self):
        """Update the summary tab with selected changes."""
        # Clear existing widgets
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.summary_frame, 
            text="The following changes will be applied:",
            wraplength=600
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Extensions
        extensions_frame = ttk.LabelFrame(self.summary_frame, text="Extensions to Install", padding=10)
        extensions_frame.pack(fill=tk.X, pady=(0, 10))
        
        extension_count = 0
        for env_name, categories in self.extension_vars.items():
            env_extensions = []
            for category, extensions in categories.items():
                for ext_id, var in extensions.items():
                    if var.get():
                        env_extensions.append(ext_id)
                        extension_count += 1
            
            if env_extensions:
                ttk.Label(
                    extensions_frame, 
                    text=f"{env_name}: {len(env_extensions)} extensions",
                    wraplength=600
                ).pack(anchor=tk.W)
        
        if extension_count == 0:
            ttk.Label(
                extensions_frame, 
                text="No extensions selected for installation.",
                wraplength=600
            ).pack(anchor=tk.W)
        
        # File structure
        file_frame = ttk.LabelFrame(self.summary_frame, text="File Structure Changes", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        annotation_count = 0
        for file_path, var in self.file_vars.items():
            if var.get():
                annotation_count += 1
        
        if annotation_count > 0:
            ttk.Label(
                file_frame, 
                text=f"Analyze {annotation_count} large files for potential splitting",
                wraplength=600
            ).pack(anchor=tk.W)
        
        ttk.Label(
            file_frame, 
            text="Add filepath and filename annotations to all files",
            wraplength=600
        ).pack(anchor=tk.W)
        
        # Repository context
        repo_frame = ttk.LabelFrame(self.summary_frame, text="Repository Context", padding=10)
        repo_frame.pack(fill=tk.X, pady=(0, 10))
        
        md_count = 0
        for filename, var in self.md_vars.items():
            if var.get():
                md_count += 1
        
        ttk.Label(
            repo_frame, 
            text=f"Create {md_count} specialized markdown files",
            wraplength=600
        ).pack(anchor=tk.W)
        
        ttk.Label(
            repo_frame, 
            text="Generate repository context prompt",
            wraplength=600
        ).pack(anchor=tk.W)
        
        # Total changes
        ttk.Label(
            self.summary_frame, 
            text=f"Total changes: {extension_count + annotation_count + md_count + 2}",
            font=("Arial", 12, "bold"),
            wraplength=600
        ).pack(anchor=tk.W, pady=(10, 0))
    
    def _next_tab(self):
        """Switch to the next tab."""
        current_tab = self.notebook.index(self.notebook.select())
        
        # If on the last tab before summary, update summary
        if current_tab == self.notebook.index(self.notebook.tabs()[-2]):
            self._update_summary_tab()
        
        # Switch to next tab if not on the last tab
        if current_tab < self.notebook.index(self.notebook.tabs()[-1]):
            self.notebook.select(current_tab + 1)
    
    def _previous_tab(self):
        """Switch to the previous tab."""
        current_tab = self.notebook.index(self.notebook.select())
        
        # Switch to previous tab if not on the first tab
        if current_tab > 0:
            self.notebook.select(current_tab - 1)
    
    def _apply_changes(self):
        """Apply the selected changes."""
        # Collect selected extensions
        self.selected_extensions = {}
        for env_name, categories in self.extension_vars.items():
            self.selected_extensions[env_name] = {}
            for category, extensions in categories.items():
                self.selected_extensions[env_name][category] = []
                for ext_id, var in extensions.items():
                    if var.get():
                        self.selected_extensions[env_name][category].append(ext_id)
        
        # Collect selected files
        self.selected_files = []
        for file_path, var in self.file_vars.items():
            if var.get():
                self.selected_files.append(file_path)
        
        # Collect selected MD files
        self.selected_md_files = []
        for filename, var in self.md_vars.items():
            if var.get():
                self.selected_md_files.append(filename)
        
        # Show progress dialog
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Applying Changes")
        progress_window.geometry("500x300")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(
            progress_window, 
            text="Applying selected changes...", 
            font=("Arial", 12, "bold")
        ).pack(pady=(20, 10))
        
        progress = ttk.Progressbar(progress_window, mode="indeterminate")
        progress.pack(fill=tk.X, padx=20, pady=10)
        progress.start()
        
        log_frame = ttk.Frame(progress_window)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        log_text = tk.Text(log_frame, height=10, width=60)
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_frame, command=log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Function to update log
        def update_log(message):
            log_text.insert(tk.END, message + "\n")
            log_text.see(tk.END)
            self.root.update_idletasks()
        
        # Apply changes in a separate thread
        import threading
        
        def apply_changes_thread():
            try:
                # Install extensions
                if self.selected_extensions:
                    update_log("Installing extensions...")
                    for env_name, categories in self.selected_extensions.items():
                        for category, ext_ids in categories.items():
                            if ext_ids:
                                update_log(f"  Installing {len(ext_ids)} extensions for {env_name}...")
                                # Convert extension IDs to proper format for installer
                                selections = {env_name: {category: ext_ids}}
                                results = self.extension_manager.install_selected_extensions(selections)
                                update_log(f"    Successfully installed: {len(results['success'])}")
                                update_log(f"    Failed installations: {len(results['failed'])}")
                
                # Create specialized markdown files
                if self.selected_md_files:
                    update_log("Creating specialized markdown files...")
                    for filename in self.selected_md_files:
                        update_log(f"  Creating {filename}...")
                        # Filter md_files to only include selected ones
                        filtered_md_files = {k: v for k, v in self.repo_context_manager.md_files.items() if k in self.selected_md_files}
                        self.repo_context_manager.md_files = filtered_md_files
                        results = self.repo_context_manager.create_specialized_md_files()
                        for filename, status in results.items():
                            update_log(f"    {status}")
                
                # Add file annotations
                update_log("Adding file annotations...")
                modified_files = self.file_structure_manager.add_file_annotations()
                update_log(f"  Added annotations to {len(modified_files)} files")
                
                # Analyze large files
                if self.selected_files:
                    update_log("Analyzing large files...")
                    suggestions = self.file_structure_manager.suggest_file_splits()
                    for suggestion in suggestions:
                        update_log(f"  {suggestion['file']}: {suggestion['split_suggestion']}")
                
                # Generate repository context prompt
                update_log("Generating repository context prompt...")
                prompt = self.repo_context_manager.generate_repo_prompt()
                prompt_file = os.path.join(self.repo_context_manager.repo_path, "repo_prompt.md")
                with open(prompt_file, 'w') as f:
                    f.write(prompt)
                update_log(f"  Saved prompt to {prompt_file}")
                
                # Complete
                update_log("\nAll changes applied successfully!")
                progress.stop()
                
                # Add close button
                ttk.Button(
                    progress_window, 
                    text="Close", 
                    command=progress_window.destroy
                ).pack(pady=(0, 20))
            
            except Exception as e:
                update_log(f"Error: {e}")
                progress.stop()
                
                # Add close button
                ttk.Button(
                    progress_window, 
                    text="Close", 
                    command=progress_window.destroy
                ).pack(pady=(0, 20))
        
        # Start thread
        threading.Thread(target=apply_changes_thread).start()

# Example usage
if __name__ == "__main__":
    import sys
    
    print("This module should be imported and used by setup.py.")
    print("Run setup.py to start the Dev Environment Readyifier.")
    sys.exit(1)
