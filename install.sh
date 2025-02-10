#!/bin/bash
set -e

echo "Starting installation of Script Prompter..."

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

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "git is not installed. Please install git and try again."
    exit 1
fi

# Define repository URL and installation directory
REPO_URL="https://github.com/nicoaira/script-prompter.git"
INSTALL_DIR="$HOME/.local/share/script-prompter"

# Clone or update the repository
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository from $REPO_URL..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Install Python dependencies from the repository's requirements.txt
echo "Installing Python dependencies..."
pip3 install --user -r "$INSTALL_DIR/requirements.txt"

# Create a launcher script in ~/.local/bin
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/script_prompter"
cat > "$LAUNCHER" <<EOF
#!/bin/bash
# Ensure user site packages are in PYTHONPATH so PyQt5 can be found
export PYTHONPATH="\$PYTHONPATH:$(python3 -m site --user-site)"
python3 "$INSTALL_DIR/script_prompter.py"
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

echo "Installation complete!"
echo "You can launch Script Prompter from your applications menu or by running 'script_prompter' in a terminal."
