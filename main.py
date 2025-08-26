"""
Twilio Calling Dashboard - Main Application Entry Point
Author: GitHub Copilot
Date: August 26, 2025

This is the main entry point for the Twilio calling dashboard application.
It initializes the application and shows the main window.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Add the src directory to the path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Set the project root for imports
os.environ['PYTHONPATH'] = src_path

from gui.main_window import TwilioMainWindow
from utils.config import AppConfig


def setup_application_style(app):
    """
    Set up the application style and theme
    """
    # Set application style
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Set application properties
    app.setApplicationName("Twilio Calling Dashboard")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Company")
    
    # Apply dark theme stylesheet
    dark_stylesheet = """
    QMainWindow {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 10pt;
    }
    
    QPushButton {
        background-color: #404040;
        border: 1px solid #555555;
        border-radius: 6px;
        padding: 8px 16px;
        color: #ffffff;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #505050;
        border-color: #777777;
    }
    
    QPushButton:pressed {
        background-color: #353535;
    }
    
    QLineEdit {
        background-color: #404040;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 8px;
        font-size: 12pt;
    }
    
    QLineEdit:focus {
        border-color: #0078d4;
    }
    
    QComboBox {
        background-color: #404040;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 8px;
        min-width: 150px;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    
    QComboBox::down-arrow {
        image: url(none);
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #ffffff;
    }
    
    QTreeWidget, QListWidget {
        background-color: #353535;
        border: 1px solid #555555;
        border-radius: 6px;
        padding: 5px;
    }
    
    QTreeWidget::item, QListWidget::item {
        padding: 8px;
        border-bottom: 1px solid #555555;
    }
    
    QTreeWidget::item:selected, QListWidget::item:selected {
        background-color: #0078d4;
    }
    
    QTabWidget::pane {
        border: 1px solid #555555;
        background-color: #353535;
    }
    
    QTabBar::tab {
        background-color: #404040;
        border: 1px solid #555555;
        padding: 8px 16px;
        margin: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #0078d4;
    }
    """
    
    app.setStyleSheet(dark_stylesheet)


def main():
    """
    Main function to start the application
    """
    # Create the application
    app = QApplication(sys.argv)
    
    # Set up application style
    setup_application_style(app)
    
    # TODO: Initialize configuration and database connections
    config = AppConfig()
    
    # TODO: Initialize Supabase connection
    # supabase_client = initialize_supabase()
    
    # Create and show the main window
    main_window = TwilioMainWindow()
    
    # Show size constraints information in status bar
    min_size = main_window.minimumSize()
    max_size = main_window.maximumSize()
    main_window.statusBar().showMessage(
        f"Window size constraints: Min {min_size.width()}x{min_size.height()} - Max {max_size.width()}x{max_size.height()}", 
        5000
    )
    
    main_window.showMaximized()  # Always start maximized
    
    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
