#!/bin/bash
set -e

echo "Starting LOCAL installation of Script Prompter..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Determine the current python3 binary (works with conda or system python)
PYTHON_BIN=$(which python3)

# Define installation directory
INSTALL_DIR="$HOME/.local/share/script-prompter"
# Define the source directory (current directory where this script is located)
# SCRIPT_DIR will be the directory where the script itself is.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

echo "Preparing installation directory: $INSTALL_DIR"
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "Copying local project files from $SCRIPT_DIR to $INSTALL_DIR..."
# Use rsync to copy files, excluding .git, .gitignore, and this script itself.
rsync -av "$SCRIPT_DIR/" "$INSTALL_DIR/" --exclude ".git" --exclude ".gitignore" --exclude "local_install.sh" --exclude "*.pyc" --exclude "__pycache__" --exclude ".vscode"
# Add other dev-specific exclusions if any

# Install Python dependencies from the local requirements.txt
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    echo "Installing Python dependencies from $INSTALL_DIR/requirements.txt..."
    pip3 install --user -r "$INSTALL_DIR/requirements.txt"
else
    echo "Warning: requirements.txt not found in $INSTALL_DIR. Skipping dependency installation."
fi

# Create a launcher script in ~/.local/bin
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/script_prompter"
cat > "$LAUNCHER" <<EOF
#!/bin/bash
# Add the user site-packages directory to PYTHONPATH so PyQt5 can be found
export PYTHONPATH="\$PYTHONPATH:$($PYTHON_BIN -m site --user-site)"
# Launch the application using the determined python3 interpreter
"$PYTHON_BIN" "$INSTALL_DIR/script_prompter.py"
EOF
chmod +x "$LAUNCHER"
echo "Launcher created at $LAUNCHER"

# Create .desktop file in ~/.local/share/applications
DESKTOP_FILE="$HOME/.local/share/applications/script_prompter.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Script Prompter
Exec=$LAUNCHER
Icon=$INSTALL_DIR/icon.png
Type=Application
Terminal=false
Categories=Utility;
EOF
echo ".desktop file created at $DESKTOP_FILE"

echo "Local installation complete!"
echo "You can launch Script Prompter from your applications menu or by running 'script_prompter' in a terminal."
echo "NOTE: This is a local installation. To uninstall, you may need to manually remove:"
echo "  - Directory: $INSTALL_DIR"
echo "  - Launcher: $LAUNCHER"
echo "  - Desktop file: $DESKTOP_FILE"
