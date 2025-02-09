# Script Prompter

Script Prompter is a user-friendly GUI application designed to help you easily construct enriched prompts for large language models (LLMs). With its intuitive drag-and-drop interface, you can attach script files, add custom context and instructions, and generate two versions of your prompt:

- **Raw Context:** A simple concatenation of your attached scripts, context, and instructions.
- **Enriched Prompt:** A well-formatted prompt that uses a customizable template to structure your inputs.

The application is built with Python and PyQt5 and is easily installable on Ubuntu. It even creates a desktop launcher so you can add it to your taskbar with just a single command.

## Features

- **Drag and Drop:** Easily attach script files by dragging and dropping or by clicking to select files.
- **File Management:** View attached files with the ability to remove any file via an "X" button.
- **Custom Inputs:** Optional text boxes for user context and instructions.
- **Prompt Generation:** 
  - **Copy Raw Context:** Quickly copy a plain text version of your input.
  - **Copy Enriched Prompt:** Generate a structured prompt using a default (or custom) template.
- **Template Editing:** Customize the enriched prompt template to fit your needs.
- **Easy Installation:** One-line installation command installs dependencies, sets up a launcher, and creates a desktop entry.

## Requirements

- **Operating System:** Ubuntu (or any Linux distribution that supports desktop entries)
- **Python 3**  
- **pip3** (for installing Python dependencies)

## Installation

You can install Script Prompter with a single command. Open your terminal and run:

```bash
curl -sSL https://raw.githubusercontent.com/nicoaira/script-prompter/main/install.sh | bash
```

This installation script will:
1. **Install Python dependencies:** Uses pip3 to install PyQt5 (and any other dependencies listed in `requirements.txt`).
2. **Copy the Application:** Places the main Python script in `~/.local/script_prompter/`.
3. **Create a Launcher:** Generates a launcher script in `~/.local/bin/` so you can run the app with the command `script_prompter`.
4. **Desktop Entry:** Creates a `.desktop` file in `~/.local/share/applications/` so that the application appears in your system's applications menu. You can then add it to your taskbar by right-clicking the icon and selecting “Add to Favorites” or “Lock to Launcher.”

> **Note:** Ensure that `~/.local/bin` is included in your system’s PATH. Recent Ubuntu installations include this by default.

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

1. **Attach Files:**  
   Drag and drop your script files onto the drop area or click to open a file dialog. Each attached file will be displayed with an "X" button for easy deletion.
   
2. **Add Context & Instructions:**  
   Enter any additional context or instructions in the respective text boxes. Both fields are optional.
   
3. **Generate Your Prompt:**  
   - Click **Copy Raw Context** to copy a straightforward concatenation of your scripts, context, and instructions.
   - Click **Copy Enriched Prompt** to generate a well-formatted prompt using the current template.
   
4. **Customize the Template:**  
   Click **Edit Template** to modify the enriched prompt template. The template supports the following placeholders:
   - `{scripts}`: Replaced with attached scripts (filename and content).
   - `{context}`: Replaced with user-provided context.
   - `{instructions}`: Replaced with provided instructions.

## Contributing

Contributions are welcome! Feel free to fork the repository, submit pull requests, or open issues to suggest improvements. For any major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


---

Enjoy using Script Prompter to streamline your prompt-building process for LLM applications!
```

---
