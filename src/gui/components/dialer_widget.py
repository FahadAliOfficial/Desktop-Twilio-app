"""
Dialer Widget - The main calling interface component
Contains the number input, caller ID selection, and call controls
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QComboBox, QLabel, QGridLayout,
                             QGroupBox, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
import re


class DialerWidget(QWidget):
    """
    Widget for dialing phone numbers with caller ID options
    """
    
    # Signals
    call_requested = pyqtSignal(str, str)  # phone_number, caller_id_type
    popup_mode_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Initialize UI state
        self.current_number = ""
        
        # Set up the widget
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """
        Set up the dialer user interface
        """
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("📞 Dialer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Phone number input section
        self.setup_number_input(layout)
        
        # Caller ID selection section
        self.setup_caller_id_selection(layout)
        
        # Keypad section
        self.setup_keypad(layout)
        
        # Call controls section
        self.setup_call_controls(layout)
        
        # Popup mode button
        self.setup_popup_controls(layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def setup_number_input(self, parent_layout):
        """
        Set up the phone number input section
        """
        # Group box for number input
        number_group = QGroupBox("Phone Number")
        number_layout = QVBoxLayout(number_group)
        
        # Phone number input field
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter phone number or paste...")
        self.number_input.setFont(QFont("Arial", 14))
        self.number_input.setMinimumHeight(45)
        
        # Set input validator for phone numbers
        phone_regex = QRegExp(r"[\d\+\-\(\)\s]*")
        phone_validator = QRegExpValidator(phone_regex)
        self.number_input.setValidator(phone_validator)
        
        number_layout.addWidget(self.number_input)
        
        # Format info label
        format_label = QLabel("Format: +1 (555) 123-4567 or 5551234567")
        format_label.setStyleSheet("color: #888888; font-size: 9pt;")
        number_layout.addWidget(format_label)
        
        parent_layout.addWidget(number_group)
    
    def setup_caller_id_selection(self, parent_layout):
        """
        Set up the caller ID selection dropdown
        """
        # Group box for caller ID
        caller_id_group = QGroupBox("Caller ID Options")
        caller_id_layout = QVBoxLayout(caller_id_group)
        
        # Caller ID dropdown
        self.caller_id_combo = QComboBox()
        self.caller_id_combo.setMinimumHeight(40)
        
        # Add caller ID options
        # TODO: Populate from config
        self.caller_id_combo.addItem("🔒 Hide Caller ID", "hidden")
        self.caller_id_combo.addItem("🏢 Company Number", "company")
        self.caller_id_combo.addItem("📞 Toll Free Number", "toll_free")
        
        caller_id_layout.addWidget(self.caller_id_combo)
        
        parent_layout.addWidget(caller_id_group)
    
    def setup_keypad(self, parent_layout):
        """
        Set up the numeric keypad
        """
        # Group box for keypad
        keypad_group = QGroupBox("Keypad")
        keypad_layout = QGridLayout(keypad_group)
        keypad_layout.setSpacing(5)
        
        # Keypad buttons
        keypad_buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('*', 3, 0), ('0', 3, 1), ('#', 3, 2)
        ]
        
        self.keypad_buttons = {}
        
        for text, row, col in keypad_buttons:
            button = QPushButton(text)
            button.setMinimumSize(60, 50)
            button.setFont(QFont("Arial", 12, QFont.Bold))
            button.clicked.connect(lambda checked, t=text: self.append_number(t))
            
            self.keypad_buttons[text] = button
            keypad_layout.addWidget(button, row, col)
        
        parent_layout.addWidget(keypad_group)
    
    def setup_call_controls(self, parent_layout):
        """
        Set up call control buttons
        """
        # Control buttons layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Clear button
        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.setMinimumHeight(45)
        self.clear_button.clicked.connect(self.clear_number)
        controls_layout.addWidget(self.clear_button)
        
        # Backspace button
        self.backspace_button = QPushButton("⌫ Back")
        self.backspace_button.setMinimumHeight(45)
        self.backspace_button.clicked.connect(self.backspace_number)
        controls_layout.addWidget(self.backspace_button)
        
        parent_layout.addLayout(controls_layout)
        
        # Call button
        self.call_button = QPushButton("📞 CALL")
        self.call_button.setMinimumHeight(60)
        self.call_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.call_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: 2px solid #1e7e34;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                border-color: #545b62;
            }
        """)
        self.call_button.clicked.connect(self.initiate_call)
        parent_layout.addWidget(self.call_button)
        
        # Hang up button (initially hidden)
        self.hangup_button = QPushButton("📵 HANG UP")
        self.hangup_button.setMinimumHeight(60)
        self.hangup_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.hangup_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: 2px solid #c82333;
                border-radius: 8px;
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
    
    def setup_popup_controls(self, parent_layout):
        """
        Set up popup mode controls
        """
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
        
        # Popup mode button
        self.popup_button = QPushButton("📱 Popup Mode")
        self.popup_button.setMinimumHeight(40)
        self.popup_button.setToolTip("Switch to compact popup dialer")
        self.popup_button.clicked.connect(self.request_popup_mode)
        parent_layout.addWidget(self.popup_button)
    
    def setup_connections(self):
        """
        Set up signal-slot connections
        """
        # Connect number input changes
        self.number_input.textChanged.connect(self.on_number_changed)
        self.number_input.returnPressed.connect(self.initiate_call)
    
    def append_number(self, digit: str):
        """
        Append a digit to the phone number
        
        Args:
            digit (str): The digit to append
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
        
        Args:
            text (str): The current text in the input field
        """
        # Update current number
        self.current_number = text
        
        # Enable/disable call button based on input
        self.call_button.setEnabled(bool(self.is_valid_phone_number(text)))
    
    def is_valid_phone_number(self, phone_number: str) -> bool:
        """
        Validate if the phone number is in a valid format
        
        Args:
            phone_number (str): The phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not phone_number:
            return False
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d\+]', '', phone_number)
        
        # Check if it's a valid length (10-15 digits, optionally starting with +)
        if cleaned.startswith('+'):
            return len(cleaned) >= 11 and len(cleaned) <= 16
        else:
            return len(cleaned) >= 10 and len(cleaned) <= 15
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Format the phone number for display and calling
        
        Args:
            phone_number (str): The raw phone number
            
        Returns:
            str: Formatted phone number
        """
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d\+]', '', phone_number)
        
        # TODO: Add more sophisticated formatting logic
        # For now, just return the cleaned number
        return cleaned
    
    def initiate_call(self):
        """
        Initiate a phone call with the current number and selected caller ID
        """
        phone_number = self.number_input.text().strip()
        
        if not phone_number:
            QMessageBox.warning(self, "Invalid Number", "Please enter a phone number.")
            return
        
        if not self.is_valid_phone_number(phone_number):
            QMessageBox.warning(self, "Invalid Number", 
                              "Please enter a valid phone number.\n"
                              "Format: +1 (555) 123-4567 or 5551234567")
            return
        
        # Get selected caller ID type
        caller_id_data = self.caller_id_combo.currentData()
        caller_id_text = self.caller_id_combo.currentText()
        
        # Format the phone number
        formatted_number = self.format_phone_number(phone_number)
        
        # TODO: Show calling state
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
        
        Args:
            is_calling (bool): Whether a call is in progress
        """
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
    
    def request_popup_mode(self):
        """
        Request to switch to popup mode
        """
        self.popup_mode_requested.emit()
    
    def get_current_number(self) -> str:
        """
        Get the current phone number
        
        Returns:
            str: Current phone number
        """
        return self.number_input.text()
    
    def set_number(self, phone_number: str):
        """
        Set the phone number in the input field
        
        Args:
            phone_number (str): The phone number to set
        """
        self.number_input.setText(phone_number)
    
    def get_selected_caller_id(self) -> tuple:
        """
        Get the selected caller ID option
        
        Returns:
            tuple: (caller_id_type, caller_id_text)
        """
        return (self.caller_id_combo.currentData(), self.caller_id_combo.currentText())
