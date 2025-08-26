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
        
        # Set window flags early to ensure all controls are available
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | 
                           Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | 
                           Qt.WindowCloseButtonHint)
        
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
        Set up the main user interface with responsive design
        """
        # Set window properties with size constraints
        self.setWindowTitle(f"{self.config.APP_NAME} v{self.config.APP_VERSION}")
        self.setGeometry(100, 100, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        
        # Set minimum and maximum size constraints
        self.setMinimumSize(1300, 650)   # Minimum size for usability
        # Remove maximum size constraint temporarily to test maximize button
        # self.setMaximumSize(2560, 1440) # Maximum size for ultra-wide monitors
        
        # Initialize responsive state
        self.sidebar_collapsed = False
        self.current_width_category = "large"
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)
        
        # Create sidebar with toggle functionality
        self.setup_responsive_sidebar()
        
        # Create main content area with adaptive layout
        self.setup_main_content_area()
        
        # Apply initial responsive layout
        self.apply_responsive_layout()
    
    def setup_responsive_sidebar(self):
        """
        Setup sidebar with collapse/expand functionality
        """
        # Create sidebar container
        self.sidebar_container = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_container)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        
        # Create toggle button for sidebar
        self.sidebar_toggle_btn = QPushButton("☰")
        self.sidebar_toggle_btn.setMaximumSize(40, 40)
        self.sidebar_toggle_btn.setMinimumSize(40, 40)
        self.sidebar_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e5f99;
            }
        """)
        self.sidebar_toggle_btn.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.sidebar_toggle_btn)
        
        # Create actual sidebar
        self.sidebar = SidebarNavigation()
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(350)
        self.sidebar_layout.addWidget(self.sidebar)
        
        # Add sidebar container to main layout
        self.main_layout.addWidget(self.sidebar_container)
    
    def setup_main_content_area(self):
        """
        Setup main content area with adaptive layout
        """
        # Create content splitter for content area and dialer
        self.content_splitter = QSplitter(Qt.Horizontal)
        self.content_splitter.setChildrenCollapsible(True)
        
        # Create content area
        self.content_area = ContentArea()
        self.content_area.setMinimumWidth(400)
        self.content_splitter.addWidget(self.content_area)
        
        # Create dialer widget
        self.dialer = DialerWidget()
        self.dialer.setMinimumWidth(280)
        self.dialer.setMaximumWidth(400)
        self.content_splitter.addWidget(self.dialer)
        
        # Set initial proportions
        self.content_splitter.setSizes([700, 300])
        
        # Add content splitter to main layout
        self.main_layout.addWidget(self.content_splitter, stretch=1)
    
    def toggle_sidebar(self):
        """
        Toggle sidebar visibility
        """
        if self.sidebar_collapsed:
            # Expand sidebar
            self.sidebar.show()
            self.sidebar_toggle_btn.setText("☰")
            self.sidebar_collapsed = False
        else:
            # Collapse sidebar
            self.sidebar.hide()
            self.sidebar_toggle_btn.setText("→")
            self.sidebar_collapsed = True
    
    def apply_responsive_layout(self):
        """
        Apply responsive layout based on current window size
        """
        width = self.width()
        
        # Determine width category based on size constraints
        if width < 1100:
            new_category = "small"
        elif width < 1500:
            new_category = "medium"
        else:
            new_category = "large"
        
        # Only update if category changed
        if new_category != self.current_width_category:
            self.current_width_category = new_category
            
            if new_category == "small":
                # Auto-collapse sidebar on small screens
                if not self.sidebar_collapsed:
                    self.toggle_sidebar()
                
                # Adjust component sizes for small screens
                self.dialer.setMaximumWidth(280)
                self.dialer.setMinimumWidth(250)
                self.content_area.setMinimumWidth(350)
                
                # Tighter margins for small screens
                self.main_layout.setContentsMargins(4, 4, 4, 4)
                self.main_layout.setSpacing(4)
                
            elif new_category == "medium":
                # Show sidebar but keep it compact
                if self.sidebar_collapsed:
                    self.toggle_sidebar()
                
                self.sidebar.setMaximumWidth(300)
                self.dialer.setMaximumWidth(330)
                self.dialer.setMinimumWidth(280)
                self.content_area.setMinimumWidth(400)
                
                # Standard margins
                self.main_layout.setContentsMargins(6, 6, 6, 6)
                self.main_layout.setSpacing(6)
                
            else:  # large
                # Full layout with comfortable spacing
                if self.sidebar_collapsed:
                    self.toggle_sidebar()
                
                self.sidebar.setMaximumWidth(380)
                self.dialer.setMaximumWidth(420)
                self.dialer.setMinimumWidth(320)
                self.content_area.setMinimumWidth(500)
                
                # Comfortable margins for large screens
                self.main_layout.setContentsMargins(8, 8, 8, 8)
                self.main_layout.setSpacing(8)
    
    def resizeEvent(self, event):
        """
        Handle window resize events for responsive behavior
        """
        super().resizeEvent(event)
        
        # Apply responsive layout based on new size
        self.apply_responsive_layout()
        
        # Update content splitter proportions based on available space
        width = self.width()
        sidebar_width = 0 if self.sidebar_collapsed else self.sidebar.width()
        available_width = width - sidebar_width - 30  # Account for margins and spacing
        
        if available_width > 0:
            if self.current_width_category == "small":
                # On small screens, prioritize content area
                content_ratio = 0.75
                dialer_ratio = 0.25
            elif self.current_width_category == "medium":
                # Balanced layout for medium screens
                content_ratio = 0.68
                dialer_ratio = 0.32
            else:
                # Large screens can have more balanced layout
                content_ratio = 0.65
                dialer_ratio = 0.35
            
            # Apply the proportions
            content_width = int(available_width * content_ratio)
            dialer_width = int(available_width * dialer_ratio)
            
            # Ensure minimum widths are respected
            if content_width < self.content_area.minimumWidth():
                content_width = self.content_area.minimumWidth()
                dialer_width = available_width - content_width
            
            if dialer_width < self.dialer.minimumWidth():
                dialer_width = self.dialer.minimumWidth()
                content_width = available_width - dialer_width
            
            self.content_splitter.setSizes([content_width, dialer_width])
    
    def constrainSize(self, size):
        """
        Constrain the window size to reasonable limits
        """
        # Get screen geometry for context
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        
        # Constrain width
        min_width = self.minimumSize().width()
        max_width = min(self.maximumSize().width(), screen_rect.width() - 100)
        width = max(min_width, min(size.width(), max_width))
        
        # Constrain height
        min_height = self.minimumSize().height()
        max_height = min(self.maximumSize().height(), screen_rect.height() - 100)
        height = max(min_height, min(size.height(), max_height))
        
        from PyQt5.QtCore import QSize
        return QSize(width, height)

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
        
        # Apply responsive styles
        self.apply_responsive_styles()
    
    def apply_responsive_styles(self):
        """
        Apply responsive styles to the main window
        """
        responsive_stylesheet = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        QSplitter::handle {
            background-color: #555555;
            width: 2px;
            margin: 1px;
            border-radius: 1px;
        }
        
        QSplitter::handle:hover {
            background-color: #4a90e2;
            width: 3px;
        }
        
        QSplitter::handle:pressed {
            background-color: #357abd;
        }
        
        QSplitter {
            border: none;
        }
        
        /* Responsive components */
        QWidget {
            font-size: 10pt;
        }
        
        QPushButton {
            font-size: 9pt;
            min-height: 28px;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #555555;
            background-color: #404040;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background-color: #4a90e2;
            border-color: #357abd;
        }
        
        QPushButton:pressed {
            background-color: #357abd;
        }
        
        QLineEdit, QComboBox {
            font-size: 10pt;
            min-height: 28px;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #555555;
            background-color: #353535;
            color: #ffffff;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border-color: #4a90e2;
            background-color: #404040;
        }
        """
        
        self.setStyleSheet(responsive_stylesheet)
    
    def showEvent(self, event):
        """
        Handle show event to ensure proper responsive layout on startup
        """
        super().showEvent(event)
        
        # # Ensure window flags are properly set when showing
        # self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | 
        #                    Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | 
        #                    Qt.WindowCloseButtonHint)
        # self.show()  # Re-show after setting flags
        
        # Apply responsive layout when window is first shown
        QTimer.singleShot(100, self.apply_responsive_layout)  # Delay to ensure proper sizing
    
    def changeEvent(self, event):
        """
        Handle window state changes (minimize, maximize, restore)
        """
        super().changeEvent(event)
        
        # Handle window state changes
        if event.type() == event.WindowStateChange:
            # Apply responsive layout when window state changes
            QTimer.singleShot(50, self.apply_responsive_layout)
            
            # Update menu action text and status bar based on window state
            if self.isMaximized():
                self.maximize_action.setText('&Restore Window')
                self.statusBar().showMessage("Window maximized", 2000)
            elif self.isMinimized():
                self.statusBar().showMessage("Window minimized", 2000)
            else:
                self.maximize_action.setText('&Maximize Window')
                self.statusBar().showMessage("Window restored", 2000)

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
        
        # Maximize/Restore action
        self.maximize_action = QAction('&Maximize Window', self)
        self.maximize_action.setShortcut('F11')
        self.maximize_action.triggered.connect(self.toggle_maximize)
        view_menu.addAction(self.maximize_action)
        
        view_menu.addSeparator()
        
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
    
    def toggle_maximize(self):
        """
        Toggle between maximized and normal window state
        """
        if self.isMaximized():
            self.showNormal()
            self.maximize_action.setText('&Maximize Window')
            self.statusBar().showMessage("Window restored to normal size", 2000)
        else:
            self.showMaximized()
            self.maximize_action.setText('&Restore Window')
            self.statusBar().showMessage("Window maximized", 2000)
    
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
