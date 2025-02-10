#!/bin/bash
set -e

echo "Starting installation of Script Prompter..."

# Check if python3, pip3, and git are installed (omitted here for brevity)
# ...

# Define repository URL and installation directory
REPO_URL="https://github.com/nicoaira/script_prompter.git"
INSTALL_DIR="$HOME/.local/script_prompter"

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
python3 "$INSTALL_DIR/script_prompter.py"
EOF
chmod +x "$LAUNCHER"
echo "Launcher created at $LAUNCHER"

# Create .desktop file in ~/.local/share/applications with the correct icon path
DESKTOP_FILE="$HOME/.local/share/applications/script_prompter.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Script Prompter
Exec=$LAUNCHER
Icon=$INSTALL_DIR/logo.png
Type=Application
Terminal=false
Categories=Utility;
EOF
echo ".desktop file created at $DESKTOP_FILE"

echo "Installation complete!"
echo "You can launch Script Prompter from your applications menu or by running 'script_prompter' in a terminal."
