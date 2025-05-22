# Script Prompter

Script Prompter is a user-friendly GUI application designed to help you easily construct enriched prompts for large language models (LLMs). With its intuitive drag-and-drop interface, you can attach script files, add custom context and instructions, and generate a well-formatted prompt.

![image](https://github.com/user-attachments/assets/50e21940-9516-4067-b21b-c04053fb2fe8)

## Features

- **Drag and Drop / Click to Add:** Attach script files by dragging and dropping them onto the app or by clicking to open a file dialog. You can even drag the files from the VS Code explorer!
- **File Management:** View attached files with the option to remove any file via an "X" button.
- **Custom Inputs:** Optional text boxes for user-provided context and specific instructions.
- **Line Numbering:** Optionally prepend line numbers to each line of the attached scripts for easy reference in your prompts.
- **File Structure Tree:** Optionally include a textual representation of the directory structure of the attached files. This helps the LLM understand the relationship between files.
- **Enriched Prompt Generation:** Generate a structured prompt using a customizable template. The template dynamically adjusts to include the file tree and line numbering notes when those options are selected.
- **Template Editing:** Customize the base enriched prompt template to fit your needs.
- **Easy Installation:** Install with a single command, which downloads the package, installs dependencies, creates a command-line launcher, and sets up a desktop entry.

## Requirements

- **Operating System:** Ubuntu (or any Linux distribution that supports desktop entries)
- **Python 3**
- **pip3**
- **git** (for downloading the package)

## Installation

You can install Script Prompter with one command. Open your terminal and run:

```bash
curl -sSL https://raw.githubusercontent.com/nicoaira/script-prompter/main/install.sh | bash
```

This installation script will:
1. **Check for dependencies:** Verifies that `python3`, `pip3`, and `git` are installed.
2. **Clone or Update:** Clones the Script Prompter repository from GitHub or pulls the latest changes if already installed.
3. **Install Python dependencies:** Uses pip3 to install PyQt5 (and any other dependencies listed in `requirements.txt`).
4. **Copy the Application:** Places the main Python script and assets in `~/.local/share/script-prompter/`.
5. **Create a Launcher:** Generates a launcher script in `~/.local/bin/script_prompter` so you can run the app with the command `script_prompter`.
6. **Desktop Entry:** Creates a `.desktop` file in `~/.local/share/applications/` so that the application appears in your system's applications menu. You can then add it to your taskbar.

> **Note:** Ensure that `~/.local/bin` is included in your system’s PATH. Recent Ubuntu installations include this by default.

For local development or testing without pushing changes to the remote repository, you can use the `local_install.sh` script:
```bash
bash local_install.sh
```
This script copies local files instead of cloning/pulling from GitHub.

## Usage

Once installed, you can launch the application in two ways:
- **From the Terminal:**  
  Run the command:
  ```bash
  script_prompter
  ```
- **From the Applications Menu:**  
  Look for **Script Prompter** in your system’s applications. You can then pin it to your taskbar or favorites.

### How to Use the App

1.  **Attach Files:**
    Drag and drop your script files onto the drop area or click to open a file dialog. Each attached file will be displayed with an "X" button for easy deletion.

2.  **Select Options (Optional):**
    -   **Include line numbers in scripts:** Check this box if you want each line of your script(s) to be numbered in the output. A note will be added to the prompt indicating this.
    -   **Add file structure tree:** Check this box to include a tree diagram showing the relative paths of the attached files. A note explaining the tree will be added to the prompt.

3.  **Add Context & Instructions:**
    Enter any additional context or instructions in the respective text boxes. Both fields are optional.

4.  **Generate Your Prompt:**
    Click **Copy Enriched Prompt** to generate a well-formatted prompt using the current template and selected options. The generated prompt is copied to your clipboard.
    (The "Copy Raw Context" button provides a simpler, unformatted output but is less central to the new workflow).

5.  **Customize the Template (Optional):**
    Click **Edit Template** to modify the base enriched prompt template. The template supports the following placeholders:
    -   `{context}`: Replaced with user-provided context.
    -   `{scripts}`: Replaced with attached scripts (filename and content).
    -   `{instructions}`: Replaced with provided instructions.
    The sections for the file tree and line number notes are added dynamically based on the checkbox selections and are not part of the editable base template.

### Example Enriched Prompt Output

Below is an example of what an enriched prompt might look like when both "Include line numbers" and "Add file structure tree" are selected:

```text
### Context
This is some user-provided context about the project.
The main goal is to analyze the interaction between script_prompter.py and install.sh.

### File Structure:
script-prompter
├── install.sh
└── script_prompter.py
Note: This tree shows the organization of the attached files.

### These are the scripts:
install.sh:
1:#!/bin/bash
2:set -e
3:
4:echo "Starting installation of Script Prompter..."
5:# ... (rest of install.sh content with line numbers)

script_prompter.py:
1:#!/usr/bin/env python3
2:import sys
3:import os
4:from PyQt5.QtWidgets import (
5:# ... (rest of script_prompter.py content with line numbers)

Note: Line numbers have been prepended to each line of the script(s) above for easy reference.

### Instructions
1. Review the Python script for UI improvements.
2. Explain the role of 'git pull' in install.sh.
3. Summarize the application's purpose.
```

## Contributing

Contributions are welcome! Feel free to fork the repository, submit pull requests, or open issues to suggest improvements. For any major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
