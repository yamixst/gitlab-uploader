import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import gitlab
import threading
import base64
from configparser import ConfigParser
import json

class GitLabUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("GitLab File Uploader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configuration variables
        self.gitlab_url = tk.StringVar()
        self.private_token = tk.StringVar()
        self.project_id = tk.StringVar()
        self.branch = tk.StringVar(value="main")
        self.selected_file_path = tk.StringVar()
        self.target_path = tk.StringVar()
        self.commit_message = tk.StringVar(value="Upload file via GitLab Uploader")
        
        self.config_file = "config.ini"
        self.load_config()
        
        self.create_ui()
    
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # GitLab Connection Settings Frame
        connection_frame = ttk.LabelFrame(main_frame, text="GitLab Connection Settings", padding="10")
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # GitLab URL
        ttk.Label(connection_frame, text="GitLab URL:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(connection_frame, textvariable=self.gitlab_url, width=40).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Private Token
        ttk.Label(connection_frame, text="Private Token:").grid(row=1, column=0, sticky=tk.W, pady=2)
        token_entry = ttk.Entry(connection_frame, textvariable=self.private_token, width=40, show="*")
        token_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Project ID
        ttk.Label(connection_frame, text="Project ID:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(connection_frame, textvariable=self.project_id, width=40).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Branch
        ttk.Label(connection_frame, text="Branch:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(connection_frame, textvariable=self.branch, width=40).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Test Connection Button
        ttk.Button(connection_frame, text="Test Connection", command=self.test_connection).grid(row=4, column=0, pady=10)
        
        # Save Config Button
        ttk.Button(connection_frame, text="Save Configuration", command=self.save_config).grid(row=4, column=1, pady=10)
        
        # File Selection Frame
        file_frame = ttk.LabelFrame(main_frame, text="File Upload", padding="10")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Source File
        ttk.Label(file_frame, text="Source File:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.selected_file_path, width=40).grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=0, column=2, padx=5, pady=2)
        
        # Target Path
        ttk.Label(file_frame, text="Target Path:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.target_path, width=40).grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Label(file_frame, text="(e.g., folder/filename.ext)").grid(row=1, column=2, sticky=tk.W, pady=2)
        
        # Commit Message
        ttk.Label(file_frame, text="Commit Message:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.commit_message, width=40).grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=2)
        
        # Upload Button
        upload_button = ttk.Button(file_frame, text="Upload File", command=self.upload_file)
        upload_button.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Progress Frame
        progress_frame = ttk.Frame(main_frame, padding="10")
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", length=580, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=5)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, wraplength=580)
        self.status_label.pack(fill=tk.X, pady=5)
    
    def load_config(self):
        if os.path.exists(self.config_file):
            config = ConfigParser()
            config.read(self.config_file)
            
            if 'GitLab' in config:
                self.gitlab_url.set(config.get('GitLab', 'url', fallback=''))
                self.private_token.set(config.get('GitLab', 'token', fallback=''))
                self.project_id.set(config.get('GitLab', 'project_id', fallback=''))
                self.branch.set(config.get('GitLab', 'branch', fallback='main'))
    
    def save_config(self):
        config = ConfigParser()
        config['GitLab'] = {
            'url': self.gitlab_url.get(),
            'token': self.private_token.get(),
            'project_id': self.project_id.get(),
            'branch': self.branch.get()
        }
        
        with open(self.config_file, 'w') as f:
            config.write(f)
        
        messagebox.showinfo("Configuration Saved", "Your GitLab configuration has been saved.")
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_path.set(file_path)
            # Auto-set the target path to just the filename
            filename = os.path.basename(file_path)
            self.target_path.set(filename)
    
    def test_connection(self):
        self.status_var.set("Testing connection...")
        self.progress.start()
        
        def do_test():
            try:
                gl = gitlab.Gitlab(self.gitlab_url.get(), private_token=self.private_token.get())
                gl.auth()
                project = gl.projects.get(self.project_id.get())
                
                self.root.after(0, lambda: self.status_var.set(f"Connected successfully! Project: {project.name}"))
                self.root.after(0, self.progress.stop)
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Connection error: {str(e)}"))
                self.root.after(0, self.progress.stop)
        
        threading.Thread(target=do_test).start()
    
    def upload_file(self):
        if not self.selected_file_path.get():
            messagebox.showerror("Error", "Please select a file to upload")
            return
        
        if not self.target_path.get():
            messagebox.showerror("Error", "Please specify a target path")
            return
        
        self.status_var.set("Uploading file...")
        self.progress.start()
        
        def do_upload():
            try:
                gl = gitlab.Gitlab(self.gitlab_url.get(), private_token=self.private_token.get())
                gl.auth()
                project = gl.projects.get(self.project_id.get())
                
                # Read file content
                with open(self.selected_file_path.get(), 'rb') as file:
                    file_content = file.read()
                
                # Encode file content to base64
                file_content_base64 = base64.b64encode(file_content).decode('utf-8')
                
                # Prepare commit data
                commit_data = {
                    'branch': self.branch.get(),
                    'commit_message': self.commit_message.get(),
                    'actions': [
                        {
                            'action': 'create',
                            'file_path': self.target_path.get(),
                            'content': file_content_base64,
                            'encoding': 'base64'
                        }
                    ]
                }
                
                # Create commit
                result = project.commits.create(commit_data)
                
                self.root.after(0, lambda: self.status_var.set(f"File uploaded successfully to {self.target_path.get()}"))
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"File uploaded successfully to {self.target_path.get()}"))
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Upload error: {str(e)}"))
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to upload file: {str(e)}"))
        
        threading.Thread(target=do_upload).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GitLabUploader(root)
    root.mainloop()