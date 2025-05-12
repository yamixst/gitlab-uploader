#!/usr/bin/env python3

import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if required packages are installed and install them if needed."""
    try:
        import gitlab
        import tkinter
        print("All required packages are installed.")
    except ImportError as e:
        missing_package = str(e).split("'")[1]
        print(f"Missing package: {missing_package}")
        
        response = input(f"Would you like to install the required packages? (y/n): ")
        if response.lower() == 'y':
            print("Installing required packages...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Packages installed successfully.")
        else:
            print("Please install the required packages manually by running:")
            print("pip install -r requirements.txt")
            sys.exit(1)

def main():
    # Check for required packages
    check_requirements()
    
    # Run the GitLab uploader
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gitlab_uploader.py")
    
    if platform.system() == "Windows":
        subprocess.call([sys.executable, script_path])
    else:
        subprocess.call(["python3", script_path])

if __name__ == "__main__":
    main()