import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class FolderScannerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show_hidden = False

    def initUI(self):
        self.setWindowTitle('Folder Structure Scanner')
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        self.centerWindow()

        # Layouts
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Folder selection
        self.folderInput = QtWidgets.QLineEdit(self)
        self.folderInput.setPlaceholderText('Select folder to scan...')
        self.folderInput.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        browseButton = QtWidgets.QPushButton('Browse', self)
        browseButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border: none; border-radius: 4px;")
        browseButton.clicked.connect(self.browseFolder)

        # Hidden files/folders checkbox
        self.hiddenCheckbox = QtWidgets.QCheckBox('Include hidden files/folders', self)
        self.hiddenCheckbox.setStyleSheet("padding: 5px;")
        self.hiddenCheckbox.stateChanged.connect(self.toggleHidden)

        # Results output
        self.resultsText = QtWidgets.QTextEdit(self)
        self.resultsText.setFont(QtGui.QFont('Courier', 10))
        self.resultsText.setReadOnly(True)
        self.resultsText.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 4px;")

        # Copy to clipboard button
        copyButton = QtWidgets.QPushButton('Copy Results to Clipboard', self)
        copyButton.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border: none; border-radius: 4px;")
        copyButton.clicked.connect(self.copyToClipboard)

        # Scan button
        scanButton = QtWidgets.QPushButton('Scan Folder', self)
        scanButton.setStyleSheet("background-color: #FF5722; color: white; padding: 8px; border: none; border-radius: 4px;")
        scanButton.clicked.connect(self.scanFolder)

        # Add widgets to layout
        folderLayout = QtWidgets.QHBoxLayout()
        folderLayout.addWidget(self.folderInput)
        folderLayout.addWidget(browseButton)
        layout.addLayout(folderLayout)
        layout.addWidget(self.hiddenCheckbox)
        layout.addWidget(self.resultsText)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(scanButton)
        buttonLayout.addWidget(copyButton)
        layout.addLayout(buttonLayout)

    def centerWindow(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def browseFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.folderInput.setText(folder)

    def toggleHidden(self, state):
        self.show_hidden = state == QtCore.Qt.Checked

    def scanFolder(self):
        folder = self.folderInput.text()
        if not folder or not os.path.isdir(folder):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please select a valid folder.')
            return

        folder_structure = self.scanDirectory(folder)
        self.resultsText.setPlainText(folder_structure)

    def scanDirectory(self, folder, indent=0):
        result = ''
        prefix = '├── ' if indent > 0 else ''
        items = sorted(os.listdir(folder))
        items = [item for item in items if self.show_hidden or not item.startswith('.')]

        for i, item in enumerate(items):
            path = os.path.join(folder, item)
            is_last_item = (i == len(items) - 1)
            branch = '└── ' if is_last_item else '├── '
            indent_prefix = '│   ' * indent
            if os.path.isdir(path):
                result += f'{indent_prefix}{branch}{item}/\n'
                result += self.scanDirectory(path, indent + 1)
            else:
                result += f'{indent_prefix}{branch}{item}\n'

        return result

    def copyToClipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.resultsText.toPlainText())
        QtWidgets.QMessageBox.information(self, 'Copied', 'Folder structure copied to clipboard.')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FolderScannerApp()
    window.show()
    sys.exit(app.exec_())
