# src/main.py
import sys
import os

# Add the config directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config"))

from gui import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()