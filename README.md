# GitLab File Uploader

A simple GUI application to upload files to a GitLab repository.

## Features

- Upload files to a GitLab repository with a user-friendly interface
- Save connection settings for future use
- Test connection to GitLab before uploading
- Custom commit messages
- Progress indication

## Requirements

- Python 3.6+
- Required Python packages:
  - tkinter (usually comes with Python)
  - python-gitlab

## Installation

1. Clone this repository or download the files
2. Make the script executable (Linux/macOS only):
   ```
   chmod +x run.sh
   ```
3. Run the appropriate script for your operating system (see Usage section)

For manual installation:
```
pip install -r requirements.txt
```

## Usage

1. Run the application using one of the provided scripts:

### On Linux/macOS:
```
./run.sh
```

### On Windows:
```
run.bat
```

These scripts will:
- Create a virtual environment if it doesn't exist
- Install all required dependencies
- Launch the application

### Manual launch:
```
python gitlab_uploader.py
```

2. Configure GitLab connection settings:
   - GitLab URL: Your GitLab instance URL (e.g., https://gitlab.com)
   - Private Token: Your GitLab personal access token (can be generated in GitLab under User Settings > Access Tokens)
   - Project ID: The ID of the target project (found on the project's main page)
   - Branch: The branch to upload to (default is "main")

3. Select a file to upload using the "Browse..." button

4. Specify the target path (where the file should be placed in the repository)
   - This can be just a filename or include directories (e.g., "docs/images/logo.png")

5. Enter a commit message

6. Click "Upload File" to upload the file to GitLab

## Configuration

Your GitLab connection settings are saved to a `config.ini` file for convenience. You can manually edit this file or use the "Save Configuration" button in the application.

## Troubleshooting

If you encounter issues:

1. Ensure your GitLab token has sufficient permissions (needs at least "write_repository" scope)
2. Check that the project ID is correct and you have access to the project
3. Verify your network connection to the GitLab server
4. Look at the status message at the bottom of the application for error details

## License

This project is licensed under the MIT License - see the LICENSE file for details.