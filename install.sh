#!/bin/bash
set -e

echo "Starting installation of LLM Context Builder..."

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

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Create installation directory in the user's local folder
INSTALL_DIR="$HOME/.local/llm_context_builder"
mkdir -p "$INSTALL_DIR"
cp llm_context_builder.py "$INSTALL_DIR/"

# Create a launcher script in ~/.local/bin
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/llm_context_builder"
cat > "$LAUNCHER" <<EOF
#!/bin/bash
python3 "$INSTALL_DIR/llm_context_builder.py"
EOF
chmod +x "$LAUNCHER"
echo "Launcher created at $LAUNCHER"

# Create .desktop file in ~/.local/share/applications
DESKTOP_FILE="$HOME/.local/share/applications/llm_context_builder.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=LLM Context Builder
Exec=$LAUNCHER
Icon=utilities-terminal
Type=Application
Terminal=false
Categories=Utility;
EOF
echo ".desktop file created at $DESKTOP_FILE"

echo "Installation complete!"
echo "You can launch LLM Context Builder from your applications menu or by running 'llm_context_builder' in a terminal."
