#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QPushButton, QFileDialog, QHBoxLayout,
    QDialog, QDialogButtonBox
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
            file_path = url.toLocalFile()
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                filename = file_path.split('/')[-1]
                if self.file_added_callback:
                    self.file_added_callback(filename, content)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if file_paths:
            for file_path in file_paths:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    filename = file_path.split('/')[-1]
                    if self.file_added_callback:
                        self.file_added_callback(filename, content)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

class FileItemWidget(QWidget):
    """
    A custom widget representing an attached file.
    Displays the filename with an "X" button on the right to delete it.
    """
    def __init__(self, filename, delete_callback, parent=None):
        super(FileItemWidget, self).__init__(parent)
        self.filename = filename
        self.delete_callback = delete_callback

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        self.label = QLabel(filename)
        layout.addWidget(self.label)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedWidth(30)
        self.delete_button.clicked.connect(self.on_delete)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def on_delete(self):
        self.delete_callback(self.filename)

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
        self.resize(600, 700)

        # Dictionary to store attached files: filename -> content.
        self.files = {}
        # Dictionary to store file item widgets (for deletion).
        self.file_items = {}

        # Default enriched prompt template.
        self.template = (
            "## Enriched Prompt\n\n"
            "### Scripts\n{scripts}\n\n"
            "### User Context\n{context}\n\n"
            "### Instructions\n{instructions}\n"
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

    def add_file(self, filename, content):
        if filename in self.files:
            return  # Optionally warn or update.
        self.files[filename] = content
        file_item = FileItemWidget(filename, self.delete_file)
        self.file_list_layout.addWidget(file_item)
        self.file_items[filename] = file_item

    def delete_file(self, filename):
        if filename in self.files:
            del self.files[filename]
        if filename in self.file_items:
            widget = self.file_items[filename]
            self.file_list_layout.removeWidget(widget)
            widget.deleteLater()
            del self.file_items[filename]

    def build_scripts_text(self):
        scripts = ""
        for filename, content in self.files.items():
            scripts += f"{filename}:\n{content}\n\n"
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
        scripts_text = self.build_scripts_text()
        user_context = self.context_text.toPlainText()
        instructions = self.instructions_text.toPlainText()
        enriched_prompt = self.template.format(
            scripts=scripts_text if scripts_text else "(No scripts attached)",
            context=user_context if user_context else "(No user context provided)",
            instructions=instructions if instructions else "(No instructions provided)"
        )
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
