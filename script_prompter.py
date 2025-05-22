#!/usr/bin/env python3
import sys
import os  # Added import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QPushButton, QFileDialog, QHBoxLayout,
    QDialog, QDialogButtonBox, QCheckBox  # Added QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class DropArea(QLabel):
    """
    A QLabel subclass that acts as a drop zone.
    Users can drag & drop or click to attach files.
    When a file is added, it calls the provided callback with (filename, content).
    """
    def __init__(self, parent=None):
        super(DropArea, self).__init__(parent)
        self.setText("Drag and drop files here or click to attach files")
        self.setStyleSheet("QLabel { border: 2px dashed #aaa; padding: 10px; }")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.file_added_callback = None  # Will be set by the main window

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()  # file_path is the full path
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                # Pass full file_path to callback
                if self.file_added_callback:
                    self.file_added_callback(file_path, content)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if file_paths:
            for file_path in file_paths:  # file_path is the full path
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    # Pass full file_path to callback
                    if self.file_added_callback:
                        self.file_added_callback(file_path, content)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

class FileItemWidget(QWidget):
    """
    A custom widget representing an attached file.
    Displays the filename with an "X" button on the right to delete it.
    """
    def __init__(self, display_name, full_path, delete_callback, parent=None):  # Added full_path
        super(FileItemWidget, self).__init__(parent)
        self.full_path = full_path  # Store full_path
        self.delete_callback = delete_callback

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        self.label = QLabel(display_name)  # display_name is basename
        layout.addWidget(self.label)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedWidth(30)
        self.delete_button.clicked.connect(self.on_delete)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def on_delete(self):
        self.delete_callback(self.full_path)  # Pass full_path on delete

class TemplateDialog(QDialog):
    """
    A dialog window to let the user edit the enriched prompt template.
    The template uses these placeholders:
      - {scripts} for the file scripts (filename and content)
      - {context} for the user-provided context
      - {instructions} for the instructions
    """
    def __init__(self, current_template, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Prompt Template")
        self.template_edit = QTextEdit()
        self.template_edit.setPlainText(current_template)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Modify your enriched prompt template."))
        layout.addWidget(QLabel("Placeholders available:"))
        layout.addWidget(QLabel("  {scripts} - Inserted scripts (filename: content)"))
        layout.addWidget(QLabel("  {context} - User context"))
        layout.addWidget(QLabel("  {instructions} - Instructions"))
        layout.addWidget(self.template_edit)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def getTemplate(self):
        return self.template_edit.toPlainText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Script Prompter")
        self.resize(600, 800)  # Increased height for new checkbox

        # Dictionary to store attached files: full_path -> content.
        self.files = {}
        # Dictionary to store file item widgets (for deletion): full_path -> widget.
        self.file_items = {}

        # Default enriched prompt template.
        self.template = (
            "### Context\n{context}\n\n"
            "### These are the scripts:\n{scripts}\n\n"
            "### Instructions\n{instructions}"
        )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Drop area for files.
        self.drop_area = DropArea()
        self.drop_area.file_added_callback = self.add_file
        main_layout.addWidget(self.drop_area)

        # Container for attached files.
        main_layout.addWidget(QLabel("Attached Files:"))
        self.file_list_container = QWidget()
        self.file_list_layout = QVBoxLayout(self.file_list_container)
        self.file_list_layout.setContentsMargins(0, 0, 0, 0)
        self.file_list_layout.setSpacing(5)
        main_layout.addWidget(self.file_list_container)

        # Checkbox for line numbers
        self.include_line_numbers_checkbox = QCheckBox("Include line numbers in scripts")
        main_layout.addWidget(self.include_line_numbers_checkbox)

        # Checkbox for file tree
        self.add_tree_checkbox = QCheckBox("Add file structure tree")
        main_layout.addWidget(self.add_tree_checkbox)

        # Text edit for user context.
        self.context_text = QTextEdit()
        self.context_text.setPlaceholderText("Enter user context here (optional)...")
        main_layout.addWidget(QLabel("User Context:"))
        main_layout.addWidget(self.context_text)

        # Text edit for instructions.
        self.instructions_text = QTextEdit()
        self.instructions_text.setPlaceholderText("Enter instructions here (optional)...")
        main_layout.addWidget(QLabel("Instructions:"))
        main_layout.addWidget(self.instructions_text)

        # Buttons.
        button_layout = QHBoxLayout()
        self.copy_raw_button = QPushButton("Copy Raw Context")
        self.copy_raw_button.clicked.connect(self.copy_raw_context)
        button_layout.addWidget(self.copy_raw_button)

        self.copy_enriched_button = QPushButton("Copy Enriched Prompt")
        self.copy_enriched_button.clicked.connect(self.copy_enriched_prompt)
        button_layout.addWidget(self.copy_enriched_button)

        self.edit_template_button = QPushButton("Edit Template")
        self.edit_template_button.clicked.connect(self.edit_template)
        button_layout.addWidget(self.edit_template_button)

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

    def add_file(self, file_path, content):  # Changed first param to file_path
        if file_path in self.files:
            return  # Optionally warn or update.
        
        self.files[file_path] = content
        display_name = os.path.basename(file_path)  # Get basename for display
        file_item = FileItemWidget(display_name, file_path, self.delete_file)
        self.file_list_layout.addWidget(file_item)
        self.file_items[file_path] = file_item

    def delete_file(self, file_path):  # Changed param to file_path
        if file_path in self.files:
            del self.files[file_path]
        if file_path in self.file_items:
            widget = self.file_items[file_path]
            self.file_list_layout.removeWidget(widget)
            widget.deleteLater()
            del self.file_items[file_path]

    def _generate_tree_lines_recursive(self, tree_dict, prefix=""):
        lines = []
        items = sorted(tree_dict.items())
        for i, (name, content) in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if isinstance(content, dict):  # It's a directory
                extension = "    " if i == len(items) - 1 else "│   "
                lines.extend(self._generate_tree_lines_recursive(content, prefix + extension))
        return lines

    def build_file_tree_text(self):
        paths = list(self.files.keys())
        if not paths:
            return "(No files attached to display in tree)"

        normalized_paths = [os.path.normpath(p) for p in paths]

        if len(normalized_paths) == 1:
            return os.path.basename(normalized_paths[0])

        # Build the hierarchical dictionary for the tree
        # common_dir logic helps make the tree relative if there's a sensible common root.
        common_dir = os.path.commonpath(normalized_paths)
        
        # Check if common_dir is a file itself or not a directory (e.g. common part of filenames)
        # or if it's the filesystem root (which we might not want as an explicit single root in the tree).
        is_fs_root = (common_dir == os.path.dirname(common_dir) and os.path.isdir(common_dir))

        tree_dict_to_generate = {}
        processed_for_tree_dict = False

        if os.path.isdir(common_dir) and not is_fs_root and common_dir != ".":
            # Common directory found, make tree relative to it, with common_dir's basename as root.
            root_name = os.path.basename(common_dir)
            relative_structure = {}
            for p in sorted(normalized_paths):
                if p == common_dir:  # Skip if a path is the common_dir itself for now
                    continue 
                try:
                    rel_path = os.path.relpath(p, common_dir)
                except ValueError:  # Should not happen if common_dir is truly common and p is under it
                    rel_path = p  # Fallback
                
                parts = rel_path.split(os.sep)
                curr = relative_structure
                for part in parts[:-1]:
                    curr = curr.setdefault(part, {})
                if parts:  # Ensure parts is not empty
                    curr[parts[-1]] = True  # Mark as file/endpoint
            
            tree_dict_to_generate = {root_name: relative_structure}
            processed_for_tree_dict = True

        if not processed_for_tree_dict:  # Fallback: Diverse paths or common_dir is root/'.'
            # Build tree with potentially multiple roots from the paths themselves.
            multi_root_structure = {}
            for p in sorted(normalized_paths):
                parts = p.split(os.sep)
                # Handle leading '/' for absolute paths correctly
                if parts[0] == '' and len(parts) > 1:  # e.g. /home/user -> ['', 'home', 'user']
                    parts = parts[1:]
                
                curr = multi_root_structure
                for part in parts[:-1]:
                    curr = curr.setdefault(part, {})
                if parts:
                    curr[parts[-1]] = True
            tree_dict_to_generate = multi_root_structure
        
        # Generate lines from the prepared dictionary
        # The _generate_tree_lines_recursive expects a dict where keys are items at current level.
        # If tree_dict_to_generate has one key (e.g. {root_name: content}), we want root_name printed first.
        
        final_tree_lines = []
        sorted_top_level_items = sorted(tree_dict_to_generate.items())

        for i, (top_name, top_content) in enumerate(sorted_top_level_items):
            final_tree_lines.append(top_name)  # Print the top-level item name
            if isinstance(top_content, dict):
                 # Pass an initial prefix for children of this top-level item
                 # If it's the last top-level item, its children's vertical bars shouldn't extend beyond it.
                 # This detail is complex with current recursive helper. Simpler: always indent children.
                final_tree_lines.extend(self._generate_tree_lines_recursive(top_content, ""))  # Children start with fresh connectors

        return "\n".join(final_tree_lines)

    def build_scripts_text(self):
        scripts = ""
        add_line_numbers = self.include_line_numbers_checkbox.isChecked()
        for filename, content in self.files.items():
            processed_content = content
            if add_line_numbers:
                lines = content.splitlines()
                numbered_lines = [f"{i+1}:{line}" for i, line in enumerate(lines)]
                processed_content = "\n".join(numbered_lines)
            
            scripts += f"{filename}:\n{processed_content}\n\n"
        return scripts.strip()

    def copy_raw_context(self):
        scripts_text = self.build_scripts_text()
        user_context = self.context_text.toPlainText()
        instructions = self.instructions_text.toPlainText()
        raw_context = ""
        if scripts_text:
            raw_context += scripts_text + "\n\n"
        if user_context:
            raw_context += user_context + "\n\n"
        if instructions:
            raw_context += instructions
        QApplication.clipboard().setText(raw_context)
        print("Raw context copied to clipboard.")

    def copy_enriched_prompt(self):
        scripts_text_built = self.build_scripts_text()
        user_context = self.context_text.toPlainText()
        instructions = self.instructions_text.toPlainText()

        # Prepare arguments for formatting
        format_args = {
            "context": user_context if user_context else "(No user context provided)",
            "instructions": instructions if instructions else "(No instructions provided)",
            "scripts": scripts_text_built if scripts_text_built else "(No scripts attached)"
        }

        # Build the prompt string part by part
        prompt_parts = []
        prompt_parts.append("### Context\n{context}\n")

        if self.add_tree_checkbox.isChecked() and self.files:
            file_tree_text = self.build_file_tree_text()
            format_args["file_tree"] = file_tree_text
            prompt_parts.append("### File Structure:\n{file_tree}\nNote: This tree shows the organization of the attached files.\n")

        script_section = "### These are the scripts:\n{scripts}\n"
        if self.include_line_numbers_checkbox.isChecked() and self.files:
            script_section += "Note: Line numbers have been prepended to each line of the script(s) above for easy reference.\n"
        prompt_parts.append(script_section)
        
        prompt_parts.append("### Instructions\n{instructions}")

        final_template_str = "\n".join(prompt_parts)
        enriched_prompt = final_template_str.format(**format_args)
        
        QApplication.clipboard().setText(enriched_prompt)
        print("Enriched prompt copied to clipboard.")

    def edit_template(self):
        dialog = TemplateDialog(self.template, self)
        if dialog.exec_() == QDialog.Accepted:
            self.template = dialog.getTemplate()
            print("Template updated.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
