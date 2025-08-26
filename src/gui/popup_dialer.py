"""
Popup Dialer - Compact popup window for dialing
A minimal, always-on-top dialer window with bottom navigation
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QComboBox, QLabel, QGridLayout,
                             QFrame, QTabWidget, QListWidget, QMessageBox,
                             QStackedWidget, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator, QIcon, QPalette
import re


class PopupDialer(QWidget):
    """
    Compact popup dialer window
    """
    
    # Signals
    call_requested = pyqtSignal(str, str)  # phone_number, caller_id_type
    main_window_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set window properties
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        # Remove translucent background as it might cause issues
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize UI state
        self.current_number = ""
        self.is_calling = False
        self.current_view = "dialer"  # Default view
        
        # Set up the widget
        self.setup_ui()
        self.setup_connections()
        
        # Set window size and position (make it larger for better usability)
        self.resize(420, 600)
        self.center_on_screen()
    
    def setup_ui(self):
        """
        Set up the popup dialer interface with navigation
        """
        # Main layout with frame for styling
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 20px;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_frame)
        
        # Frame layout with proper margins to match border radius
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setSpacing(18)
        frame_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title bar with close button
        self.setup_title_bar(frame_layout)
        
        # Main content area (stacked widget for different views)
        self.content_stack = QStackedWidget()
        frame_layout.addWidget(self.content_stack)
        
        # Create different views
        self.setup_dialer_view()
        self.setup_recent_view()
        self.setup_voicemail_view()
        
        # Bottom navigation bar
        self.setup_navigation_bar(frame_layout)
    
    def setup_dialer_view(self):
        """
        Set up the main dialer view with keypad
        """
        dialer_widget = QWidget()
        dialer_layout = QVBoxLayout(dialer_widget)
        dialer_layout.setSpacing(15)
        dialer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Phone number input
        self.setup_phone_input(dialer_layout)
        
        # Caller ID selection
        self.setup_caller_id_selection(dialer_layout)
        
        # Keypad
        self.setup_compact_keypad(dialer_layout)
        
        # Call controls
        self.setup_call_controls(dialer_layout)
        
        # Add to stack
        self.content_stack.addWidget(dialer_widget)
        
    def setup_recent_view(self):
        """
        Set up the recent calls view
        """
        recent_widget = QWidget()
        recent_layout = QVBoxLayout(recent_widget)
        recent_layout.setSpacing(15)
        recent_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("📞 Recent Calls")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4a90e2; margin-bottom: 10px;")
        recent_layout.addWidget(title_label)
        
        # Recent calls list
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet("""
            QListWidget {
                background-color: #353535;
                border: 2px solid #4a90e2;
                border-radius: 10px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #555555;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        
        # Add sample recent calls
        recent_calls = [
            "📞 +1 (555) 123-4567\n   Today 2:30 PM",
            "📞 +1 (555) 987-6543\n   Today 1:15 PM", 
            "📞 +1 (555) 555-0123\n   Yesterday 4:45 PM",
            "📞 +1 (555) 777-8888\n   Yesterday 10:20 AM",
            "📞 +1 (555) 999-0000\n   Monday 3:00 PM"
        ]
        for call in recent_calls:
            self.recent_list.addItem(call)
        
        self.recent_list.itemDoubleClicked.connect(self.dial_from_recent)
        recent_layout.addWidget(self.recent_list)
        
        # Quick dial button
        quick_dial_btn = QPushButton("📞 Quick Dial Selected")
        quick_dial_btn.setMinimumHeight(50)
        quick_dial_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        quick_dial_btn.clicked.connect(self.quick_dial_selected)
        recent_layout.addWidget(quick_dial_btn)
        
        # Add to stack
        self.content_stack.addWidget(recent_widget)
        
    def setup_voicemail_view(self):
        """
        Set up the voicemail view
        """
        voicemail_widget = QWidget()
        voicemail_layout = QVBoxLayout(voicemail_widget)
        voicemail_layout.setSpacing(15)
        voicemail_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("🔊 Voicemail")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4a90e2; margin-bottom: 10px;")
        voicemail_layout.addWidget(title_label)
        
        # Voicemail list
        self.voicemail_list = QListWidget()
        self.voicemail_list.setStyleSheet("""
            QListWidget {
                background-color: #353535;
                border: 2px solid #4a90e2;
                border-radius: 10px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #555555;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        
        # Add sample voicemails
        voicemails = [
            "🔴 NEW: +1 (555) 123-4567\n   Duration: 1:23 - Today 3:45 PM",
            "🔴 NEW: +1 (555) 987-6543\n   Duration: 0:45 - Today 11:20 AM",
            "⚫ +1 (555) 555-0123\n   Duration: 2:10 - Yesterday 6:30 PM",
            "⚫ +1 (555) 777-8888\n   Duration: 0:30 - Monday 2:15 PM"
        ]
        for voicemail in voicemails:
            self.voicemail_list.addItem(voicemail)
        
        voicemail_layout.addWidget(self.voicemail_list)
        
        # Voicemail controls
        controls_layout = QHBoxLayout()
        
        play_btn = QPushButton("▶️ Play")
        play_btn.setMinimumHeight(45)
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        callback_btn = QPushButton("📞 Call Back")
        callback_btn.setMinimumHeight(45)
        callback_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        callback_btn.clicked.connect(self.callback_from_voicemail)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setMinimumHeight(45)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        controls_layout.addWidget(play_btn)
        controls_layout.addWidget(callback_btn)
        controls_layout.addWidget(delete_btn)
        voicemail_layout.addLayout(controls_layout)
        
        # Add to stack
        self.content_stack.addWidget(voicemail_widget)
        
    def setup_navigation_bar(self, parent_layout):
        """
        Set up bottom navigation bar with view switching buttons
        """
        # Add spacing
        parent_layout.addSpacing(10)
        
        # Navigation container with improved styling
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #353535;
                border: 2px solid #4a90e2;
                border-radius: 18px;
                padding: 8px;
                margin-top: 5px;
            }
        """)
        
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(12, 12, 12, 12)
        nav_layout.setSpacing(8)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        # Recent button
        recent_btn = QPushButton("📞\nRecent")
        recent_btn.setMinimumHeight(65)
        recent_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        recent_btn.clicked.connect(lambda: self.switch_view("recent"))
        self.nav_buttons["recent"] = recent_btn
        nav_layout.addWidget(recent_btn)
        
        # Dialer button (default active)
        dialer_btn = QPushButton("⌨\nDialer")
        dialer_btn.setMinimumHeight(65)
        dialer_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        dialer_btn.clicked.connect(lambda: self.switch_view("dialer"))
        self.nav_buttons["dialer"] = dialer_btn
        nav_layout.addWidget(dialer_btn)
        
        # Voicemail button
        voicemail_btn = QPushButton("🔊\nVoicemail")
        voicemail_btn.setMinimumHeight(65)
        voicemail_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        voicemail_btn.clicked.connect(lambda: self.switch_view("voicemail"))
        self.nav_buttons["voicemail"] = voicemail_btn
        nav_layout.addWidget(voicemail_btn)
        
        # Style all navigation buttons
        nav_button_style = """
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 12px 8px;
            }
            QPushButton:hover {
                background-color: #505050;
                border-color: #4a90e2;
            }
        """
        
        active_button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: 2px solid #357abd;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 12px 8px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """
        
        for btn in self.nav_buttons.values():
            btn.setStyleSheet(nav_button_style)
        
        # Set dialer as active by default
        self.nav_buttons["dialer"].setStyleSheet(active_button_style)
        
        parent_layout.addWidget(nav_frame)
        
    def switch_view(self, view_name):
        """
        Switch between different views in the popup
        """
        self.current_view = view_name
        
        # Update button styles
        nav_button_style = """
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 12px 8px;
            }
            QPushButton:hover {
                background-color: #505050;
                border-color: #4a90e2;
            }
        """
        
        active_button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: 2px solid #357abd;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 12px 8px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """
        
        # Reset all buttons
        for btn in self.nav_buttons.values():
            btn.setStyleSheet(nav_button_style)
        
        # Set active button
        if view_name in self.nav_buttons:
            self.nav_buttons[view_name].setStyleSheet(active_button_style)
        
        # Switch content view
        view_index = {"recent": 1, "dialer": 0, "voicemail": 2}
        if view_name in view_index:
            self.content_stack.setCurrentIndex(view_index[view_name])
    def setup_title_bar(self, parent_layout):
        """
        Set up the title bar with minimize and close buttons
        """
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("📱 Quick Dialer")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #4a90e2; 
                padding: 8px 12px;
                background-color: rgba(74, 144, 226, 0.1);
                border-radius: 12px;
                margin-bottom: 5px;
            }
        """)
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Minimize button (restore to main window)
        minimize_button = QPushButton("⬇")
        minimize_button.setMinimumSize(45, 40)
        minimize_button.setMaximumSize(45, 40)
        minimize_button.setToolTip("Return to main window")
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e5f99;
            }
        """)
        minimize_button.clicked.connect(self.return_to_main_window)
        title_layout.addWidget(minimize_button)
        
        # Close button
        close_button = QPushButton("✕")
        close_button.setMinimumSize(45, 40)
        close_button.setMaximumSize(45, 40)
        close_button.setToolTip("Close application")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #a71e2a;
            }
        """)
        close_button.clicked.connect(self.close_application)
        title_layout.addWidget(close_button)
        
        parent_layout.addLayout(title_layout)
        
        # Separator with better styling
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("""
            QFrame {
                color: #4a90e2;
                background-color: #4a90e2;
                border: none;
                max-height: 2px;
                margin: 15px 5px;
            }
        """)
        parent_layout.addWidget(separator)
    
    def setup_phone_input(self, parent_layout):
        """
        Set up the phone number input field
        """
        # Phone number input with better styling (larger size)
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter phone number...")
        self.number_input.setMinimumHeight(70)  # Increased from 55
        self.number_input.setFont(QFont("Segoe UI", 18))  # Larger font
        self.number_input.setStyleSheet("""
            QLineEdit {
                background-color: #353535;
                border: 3px solid #555555;
                border-radius: 22px;
                color: #ffffff;
                padding: 20px 25px;
                font-size: 18px;
                font-weight: 500;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background-color: #404040;
            }
            QLineEdit::placeholder {
                color: #888888;
                font-style: italic;
            }
        """)
        
        # Set up phone number validation
        phone_regex = QRegExp(r'^[\+]?[0-9\s\-\(\)]{0,20}$')
        phone_validator = QRegExpValidator(phone_regex)
        self.number_input.setValidator(phone_validator)
        
        parent_layout.addWidget(self.number_input)
    
    def setup_caller_id_selection(self, parent_layout):
        """
        Set up the compact caller ID selection
        """
        # Caller ID dropdown with improved styling
        self.caller_id_combo = QComboBox()
        self.caller_id_combo.setMinimumHeight(60)  # Larger height
        self.caller_id_combo.setFont(QFont("Segoe UI", 16))  # Larger font
        
        # Force dark palette for dropdown
        palette = QPalette()
        palette.setColor(QPalette.Base, palette.color(QPalette.Window))
        palette.setColor(QPalette.Window, palette.color(QPalette.Base))
        self.caller_id_combo.setPalette(palette)
        
        # Apply styles
        self.caller_id_combo.setStyleSheet("""
            QComboBox {
                background-color: #353535;
                border: 3px solid #555555;
                border-radius: 20px;
                padding: 15px 25px;
                color: #ffffff;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Segoe UI';
                min-width: 250px;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 40px;
                background-color: transparent;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 8px solid #ffffff;
                margin: 10px;
            }
            QComboBox:hover::down-arrow {
                border-top-color: #4a90e2;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b !important;
                color: #ffffff !important;
                border: 3px solid #4a90e2;
                border-radius: 15px;
                selection-background-color: #4a90e2;
                selection-color: #ffffff;
                outline: none;
                font-size: 16px;
                padding: 8px;
                show-decoration-selected: 1;
            }
            QComboBox QAbstractItemView::item {
                background-color: #2b2b2b !important;
                color: #ffffff !important;
                padding: 15px 20px;
                border: none;
                margin: 2px;
                border-radius: 8px;
                min-height: 25px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #4a90e2 !important;
                color: #ffffff !important;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #357abd !important;
                color: #ffffff !important;
            }
        """)
        
        # Add caller ID options with better icons and descriptions
        self.caller_id_combo.addItem("🔒 Hide Caller ID (Private)", "hidden")
        self.caller_id_combo.addItem("🏢 Company Number (Business)", "company")
        self.caller_id_combo.addItem("📞 Toll Free Number (Support)", "toll_free")
        
        parent_layout.addWidget(self.caller_id_combo)
    
    def setup_compact_keypad(self, parent_layout):
        """
        Set up the compact numeric keypad
        """
        # Reduced spacing before keypad (was 10)
        parent_layout.addSpacing(5)
        
        # Keypad grid with better spacing
        keypad_layout = QGridLayout()
        keypad_layout.setSpacing(12)  # More space between buttons
        keypad_layout.setContentsMargins(5, 5, 5, 5)
        
        # Keypad buttons (larger for better usability)
        keypad_buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('*', 3, 0), ('0', 3, 1), ('#', 3, 2)
        ]
        
        self.keypad_buttons = {}
        
        for text, row, col in keypad_buttons:
            button = QPushButton(text)
            button.setMinimumSize(75, 60)  # Larger buttons
            button.setMaximumSize(75, 60)
            button.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Better font
            button.setStyleSheet("""
                QPushButton {
                    background-color: #353535;
                    color: #ffffff;
                    border: 2px solid #555555;
                    border-radius: 18px;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Segoe UI';
                }
                QPushButton:hover {
                    background-color: #4a90e2;
                    border-color: #357abd;
                }
                QPushButton:pressed {
                    background-color: #357abd;
                    border-color: #2e5f99;
                }
            """)
            button.clicked.connect(lambda checked, t=text: self.append_number(t))
            
            self.keypad_buttons[text] = button
            keypad_layout.addWidget(button, row, col)
        
        parent_layout.addLayout(keypad_layout)
    
    def setup_call_controls(self, parent_layout):
        """
        Set up compact call control buttons
        """
        # Reduced spacing before controls (was 8, now 3)
        parent_layout.addSpacing(3)
        
        # Control buttons layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Clear and backspace buttons (larger and more visible)
        self.clear_button = QPushButton("🗑 Clear")
        self.clear_button.setMinimumSize(85, 50)
        self.clear_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        self.clear_button.clicked.connect(self.clear_number)
        controls_layout.addWidget(self.clear_button)
        
        self.backspace_button = QPushButton("⌫ Back")
        self.backspace_button.setMinimumSize(85, 50)
        self.backspace_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.backspace_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        self.backspace_button.clicked.connect(self.backspace_number)
        controls_layout.addWidget(self.backspace_button)
        
        parent_layout.addLayout(controls_layout)
        
        # Further reduced spacing before call button (was 5, now 2)
        parent_layout.addSpacing(2)
        
        # Call button (much larger and more prominent, moved up)
        self.call_button = QPushButton("📞 CALL")
        self.call_button.setMinimumHeight(75)  # Even taller for better visibility
        self.call_button.setFont(QFont("Segoe UI", 16, QFont.Bold))  # Larger font
        self.call_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: 4px solid #1e7e34;
                border-radius: 25px;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 18px;
                margin: 2px 0px;
            }
            QPushButton:hover {
                background-color: #218838;
                border-color: #1c7430;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
                border-color: #5a6268;
            }
        """)
        self.call_button.clicked.connect(self.initiate_call)
        parent_layout.addWidget(self.call_button)
        
        # Hang up button (initially hidden)
        self.hangup_button = QPushButton("📵 HANG UP")
        self.hangup_button.setMinimumHeight(65)
        self.hangup_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.hangup_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 18px;
                margin: 10px 0px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.hangup_button.clicked.connect(self.hang_up_call)
        self.hangup_button.hide()
        parent_layout.addWidget(self.hangup_button)
    
    def setup_connections(self):
        """
        Set up signal-slot connections
        """
        # Connect number input changes
        self.number_input.textChanged.connect(self.on_number_changed)
        self.number_input.returnPressed.connect(self.initiate_call)
    
    def center_on_screen(self):
        """
        Center the popup window on the screen
        """
        from PyQt5.QtWidgets import QApplication
        
        # Get the primary screen geometry
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        
        # Calculate center position
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        
        # Move to center
        self.move(x, y)
    
    def showEvent(self, event):
        """
        Override showEvent to always center the popup when shown
        """
        super().showEvent(event)
        # Center the popup every time it's shown
        self.center_on_screen()
    
    def append_number(self, digit: str):
        """
        Append a digit to the phone number
        """
        current_text = self.number_input.text()
        self.number_input.setText(current_text + digit)
    
    def clear_number(self):
        """
        Clear the phone number input
        """
        self.number_input.clear()
    
    def backspace_number(self):
        """
        Remove the last character from the phone number
        """
        current_text = self.number_input.text()
        if current_text:
            self.number_input.setText(current_text[:-1])
    
    def on_number_changed(self, text: str):
        """
        Handle phone number input changes
        """
        self.current_number = text
        self.call_button.setEnabled(bool(self.is_valid_phone_number(text)))
    
    def is_valid_phone_number(self, phone_number: str) -> bool:
        """
        Validate if the phone number is in a valid format
        """
        if not phone_number:
            return False
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d\+]', '', phone_number)
        
        # Check if it's a valid length
        if cleaned.startswith('+'):
            return len(cleaned) >= 11 and len(cleaned) <= 16
        else:
            return len(cleaned) >= 10 and len(cleaned) <= 15
    
    def initiate_call(self):
        """
        Initiate a phone call
        """
        phone_number = self.number_input.text().strip()
        
        if not phone_number:
            QMessageBox.warning(self, "Invalid Number", "Please enter a phone number.")
            return
        
        if not self.is_valid_phone_number(phone_number):
            QMessageBox.warning(self, "Invalid Number", 
                              "Please enter a valid phone number.")
            return
        
        # Get selected caller ID type
        caller_id_data = self.caller_id_combo.currentData()
        
        # Format the phone number
        formatted_number = self.format_phone_number(phone_number)
        
        # Update UI state
        self.set_calling_state(True)
        
        # Emit signal to initiate call
        self.call_requested.emit(formatted_number, caller_id_data)
    
    def hang_up_call(self):
        """
        Hang up the current call
        """
        # TODO: Implement hang up logic
        self.set_calling_state(False)
    
    def set_calling_state(self, is_calling: bool):
        """
        Update UI to reflect calling state
        """
        self.is_calling = is_calling
        
        if is_calling:
            self.call_button.hide()
            self.hangup_button.show()
            self.number_input.setEnabled(False)
            self.caller_id_combo.setEnabled(False)
            
            # Disable keypad buttons
            for button in self.keypad_buttons.values():
                button.setEnabled(False)
        else:
            self.hangup_button.hide()
            self.call_button.show()
            self.number_input.setEnabled(True)
            self.caller_id_combo.setEnabled(True)
            
            # Enable keypad buttons
            for button in self.keypad_buttons.values():
                button.setEnabled(True)
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Format the phone number for calling
        """
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d\+]', '', phone_number)
        return cleaned
    
    def dial_from_recent(self, item):
        """
        Dial a number from recent calls list
        """
        # Extract phone number from recent call item
        text = item.text()
        lines = text.split('\n')
        if lines:
            # Extract phone number (remove emoji and extra text)
            phone_line = lines[0].replace('📞 ', '').strip()
            self.number_input.setText(phone_line)
            # Switch to dialer view
            self.switch_view("dialer")
    
    def quick_dial_selected(self):
        """
        Quick dial the selected recent call
        """
        current_item = self.recent_list.currentItem()
        if current_item:
            # Extract phone number
            text = current_item.text()
            lines = text.split('\n')
            if lines:
                phone_line = lines[0].replace('📞 ', '').strip()
                self.number_input.setText(phone_line)
                # Switch to dialer and initiate call
                self.switch_view("dialer")
                self.initiate_call()
    
    def callback_from_voicemail(self):
        """
        Call back from selected voicemail
        """
        current_item = self.voicemail_list.currentItem()
        if current_item:
            # Extract phone number from voicemail item
            text = current_item.text()
            lines = text.split('\n')
            if lines:
                # Extract phone number (remove status indicators)
                phone_line = lines[0].replace('🔴 NEW: ', '').replace('⚫ ', '').strip()
                self.number_input.setText(phone_line)
                # Switch to dialer and initiate call
                self.switch_view("dialer")
                self.initiate_call()
    
    def dial_from_favorites(self, item):
        """
        Dial a number from favorites list (keeping for compatibility)
        """
        # Extract phone number from "Name: Number" format
        text = item.text()
        if ":" in text:
            phone_number = text.split(":")[-1].strip()
            self.number_input.setText(phone_number)
    
    def return_to_main_window(self):
        """
        Return to the main window
        """
        self.main_window_requested.emit()
        self.hide()
    
    def close_application(self):
        """
        Close the entire application
        """
        # TODO: Add confirmation dialog
        if self.parent():
            self.parent().close()
        else:
            self.close()
    
    def mousePressEvent(self, event):
        """
        Handle mouse press for dragging
        """
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """
        Handle mouse move for dragging
        """
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()
