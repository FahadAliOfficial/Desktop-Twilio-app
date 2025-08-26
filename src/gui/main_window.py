"""
Main Window class for the Twilio Calling Dashboard
This is the primary window that contains all the main functionality
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QSplitter, QMenuBar, QStatusBar, QAction, QMessageBox,
                             QToolBar, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QKeySequence

from gui.components.dialer_widget import DialerWidget
from gui.components.sidebar_navigation import SidebarNavigation
from gui.components.content_area import ContentArea
from gui.popup_dialer import PopupDialer
from services.call_service import CallService
from utils.config import AppConfig


class TwilioMainWindow(QMainWindow):
    """
    Main window for the Twilio calling dashboard application
    """
    
    # Signals
    call_initiated = pyqtSignal(str, str)  # phone_number, caller_id_type
    popup_mode_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config = AppConfig()
        
        # Initialize services
        # TODO: Initialize call service with Twilio credentials
        self.call_service = None  # CallService(self.config)
        
        # Initialize UI state
        self.is_popup_mode = False
        self.popup_window = None
        
        # Set up the main window
        self.setup_ui()
        self.setup_connections()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        
        # TODO: Load user preferences and window state
        # self.load_preferences()
    
    def setup_ui(self):
        """
        Set up the main user interface
        """
        # Set window properties
        self.setWindowTitle(f"{self.config.APP_NAME} v{self.config.APP_VERSION}")
        self.setGeometry(100, 100, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self.setMinimumSize(800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create splitter for resizable layout
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create sidebar navigation
        self.sidebar = SidebarNavigation()
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(350)
        splitter.addWidget(self.sidebar)
        
        # Create content area container
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        # Create content area for main content
        self.content_area = ContentArea()
        content_layout.addWidget(self.content_area, stretch=2)
        
        # Create dialer widget
        self.dialer = DialerWidget()
        self.dialer.setMinimumWidth(300)
        self.dialer.setMaximumWidth(400)
        content_layout.addWidget(self.dialer, stretch=1)
        
        splitter.addWidget(content_container)
        
        # Set splitter proportions
        splitter.setSizes([300, 900])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
    
    def setup_connections(self):
        """
        Set up signal-slot connections
        """
        # Connect sidebar navigation signals
        self.sidebar.section_changed.connect(self.content_area.show_section)
        self.sidebar.export_requested.connect(self.export_call_history)
        
        # Connect dialer signals
        self.dialer.call_requested.connect(self.initiate_call)
        self.dialer.popup_mode_requested.connect(self.toggle_popup_mode)
        
        # Connect content area signals
        self.content_area.call_history_refresh_requested.connect(self.refresh_call_history)
        
        # TODO: Connect call service signals
        # if self.call_service:
        #     self.call_service.call_status_changed.connect(self.update_call_status)
        #     self.call_service.call_completed.connect(self.on_call_completed)
    
    def setup_menu_bar(self):
        """
        Set up the application menu bar
        """
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        # Export action
        export_action = QAction('&Export Call History', self)
        export_action.setShortcut(QKeySequence.Print)
        export_action.triggered.connect(self.export_call_history)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        # Popup mode action
        popup_action = QAction('&Popup Mode', self)
        popup_action.setShortcut('Ctrl+P')
        popup_action.triggered.connect(self.toggle_popup_mode)
        view_menu.addAction(popup_action)
        
        # Refresh action
        refresh_action = QAction('&Refresh', self)
        refresh_action.setShortcut(QKeySequence.Refresh)
        refresh_action.triggered.connect(self.refresh_call_history)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        # About action
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """
        Set up the application toolbar
        """
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # TODO: Add toolbar buttons with icons
        # Call button
        call_button = QPushButton("📞 Call")
        call_button.clicked.connect(lambda: self.dialer.initiate_call())
        toolbar.addWidget(call_button)
        
        toolbar.addSeparator()
        
        # Popup mode button
        popup_button = QPushButton("📱 Popup Mode")
        popup_button.clicked.connect(self.toggle_popup_mode)
        toolbar.addWidget(popup_button)
        
        toolbar.addSeparator()
        
        # Refresh button
        refresh_button = QPushButton("🔄 Refresh")
        refresh_button.clicked.connect(self.refresh_call_history)
        toolbar.addWidget(refresh_button)
    
    def setup_status_bar(self):
        """
        Set up the application status bar
        """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Show ready status
        self.status_bar.showMessage("Ready", 2000)
        
        # TODO: Add permanent widgets for connection status
        # self.connection_status = QLabel("Disconnected")
        # self.status_bar.addPermanentWidget(self.connection_status)
    
    def initiate_call(self, phone_number: str, caller_id_type: str):
        """
        Initiate a phone call
        
        Args:
            phone_number (str): The phone number to call
            caller_id_type (str): Type of caller ID to use
        """
        try:
            # TODO: Implement actual call initiation logic
            self.status_bar.showMessage(f"Calling {phone_number} with {caller_id_type} caller ID...", 5000)
            
            # Placeholder for call service integration
            # if self.call_service:
            #     self.call_service.initiate_call(phone_number, caller_id_type)
            # else:
            #     QMessageBox.warning(self, "Service Error", 
            #                        "Call service not initialized. Please check your Twilio configuration.")
            
            # Emit signal for other components
            self.call_initiated.emit(phone_number, caller_id_type)
            
        except Exception as e:
            QMessageBox.critical(self, "Call Error", f"Failed to initiate call: {str(e)}")
    
    def toggle_popup_mode(self):
        """
        Toggle between main window and popup mode
        """
        if not self.is_popup_mode:
            # Switch to popup mode
            self.hide()
            
            if not self.popup_window:
                self.popup_window = PopupDialer(self)
                # Connect popup window signals
                self.popup_window.main_window_requested.connect(self.return_from_popup_mode)
                self.popup_window.call_requested.connect(self.initiate_call)
            
            self.popup_window.show()
            self.is_popup_mode = True
            
        else:
            # Switch back to main window
            if self.popup_window:
                self.popup_window.hide()
            
            self.show()
            self.is_popup_mode = False
    
    def return_from_popup_mode(self):
        """
        Handle return from popup mode to main window
        """
        if self.popup_window:
            self.popup_window.hide()
        
        self.show()
        self.is_popup_mode = False
    
    def export_call_history(self):
        """
        Export call history to Excel file
        """
        try:
            # TODO: Implement export functionality
            self.status_bar.showMessage("Exporting call history...", 3000)
            
            # Placeholder for export logic
            # from ..services.export_service import ExportService
            # export_service = ExportService()
            # export_service.export_call_history()
            
            QMessageBox.information(self, "Export Complete", 
                                  "Call history exported successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export call history: {str(e)}")
    
    def refresh_call_history(self):
        """
        Refresh call history data
        """
        try:
            self.status_bar.showMessage("Refreshing call history...", 2000)
            
            # TODO: Implement refresh logic
            # Refresh data in content area
            self.content_area.refresh_current_section()
            
        except Exception as e:
            QMessageBox.critical(self, "Refresh Error", f"Failed to refresh data: {str(e)}")
    
    def show_about_dialog(self):
        """
        Show about dialog
        """
        QMessageBox.about(self, "About", 
                         f"{self.config.APP_NAME} v{self.config.APP_VERSION}\n\n"
                         "A professional Twilio calling dashboard application.\n\n"
                         "Features:\n"
                         "• Make calls with different caller ID options\n"
                         "• Call history management\n"
                         "• Voicemail integration\n"
                         "• Export capabilities\n"
                         "• Popup dialer mode")
    
    def closeEvent(self, event):
        """
        Handle application close event
        """
        # TODO: Save preferences and cleanup
        if self.popup_window:
            self.popup_window.close()
        
        # TODO: Cleanup call service and database connections
        # if self.call_service:
        #     self.call_service.cleanup()
        
        event.accept()
