"""
Sidebar Navigation - Left panel with navigation sections
Contains navigation for History, Voicemail, Settings, and Export functionality
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QScrollArea, QListWidget, 
                             QListWidgetItem, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon


class SidebarNavigation(QWidget):
    """
    Sidebar navigation widget with different sections
    """
    
    # Signals
    section_changed = pyqtSignal(str)  # section_name
    export_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Current selected section
        self.current_section = "history"
        
        # Set up the widget
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """
        Set up the sidebar navigation interface
        """
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title section
        self.setup_title_section(layout)
        
        # Export button
        self.setup_export_section(layout)
        
        # Navigation sections
        self.setup_navigation_sections(layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def setup_title_section(self, parent_layout):
        """
        Set up the title section
        """
        # Title label
        title_label = QLabel("📊 Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        parent_layout.addWidget(title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
    
    def setup_export_section(self, parent_layout):
        """
        Set up the export section
        """
        # Export button
        self.export_button = QPushButton("📊 Export Call History")
        self.export_button.setMinimumHeight(45)
        self.export_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: 2px solid #0056b3;
                border-radius: 8px;
                text-align: left;
                padding-left: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.export_button.clicked.connect(self.request_export)
        parent_layout.addWidget(self.export_button)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(separator)
    
    def setup_navigation_sections(self, parent_layout):
        """
        Set up the navigation sections
        """
        # Navigation group
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout(nav_group)
        nav_layout.setSpacing(5)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        # History section
        self.nav_buttons['history'] = self.create_nav_button(
            "📞 Call History", 
            "View and manage your call history",
            "history",
            True  # Selected by default
        )
        nav_layout.addWidget(self.nav_buttons['history'])
        
        # Voicemail section
        self.nav_buttons['voicemail'] = self.create_nav_button(
            "🔊 Voicemail", 
            "Access your voicemail messages",
            "voicemail"
        )
        nav_layout.addWidget(self.nav_buttons['voicemail'])
        
        # Contacts section
        self.nav_buttons['contacts'] = self.create_nav_button(
            "👥 Contacts", 
            "Manage your contact list",
            "contacts"
        )
        nav_layout.addWidget(self.nav_buttons['contacts'])
        
        # Settings section
        self.nav_buttons['settings'] = self.create_nav_button(
            "⚙️ Settings", 
            "Configure application settings",
            "settings"
        )
        nav_layout.addWidget(self.nav_buttons['settings'])
        
        # Analytics section
        self.nav_buttons['analytics'] = self.create_nav_button(
            "📈 Analytics", 
            "View call statistics and reports",
            "analytics"
        )
        nav_layout.addWidget(self.nav_buttons['analytics'])
        
        parent_layout.addWidget(nav_group)
        
        # Quick actions group
        self.setup_quick_actions(parent_layout)
    
    def setup_quick_actions(self, parent_layout):
        """
        Set up quick action buttons
        """
        # Quick actions group
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(5)
        
        # Recent calls quick access
        recent_calls_button = QPushButton("🕒 Recent Calls")
        recent_calls_button.setMinimumHeight(35)
        recent_calls_button.clicked.connect(lambda: self.select_section("history"))
        actions_layout.addWidget(recent_calls_button)
        
        # Favorites quick access
        favorites_button = QPushButton("⭐ Favorites")
        favorites_button.setMinimumHeight(35)
        favorites_button.clicked.connect(lambda: self.select_section("contacts"))
        actions_layout.addWidget(favorites_button)
        
        # Missed calls quick access
        missed_calls_button = QPushButton("❌ Missed Calls")
        missed_calls_button.setMinimumHeight(35)
        missed_calls_button.clicked.connect(lambda: self.show_missed_calls())
        actions_layout.addWidget(missed_calls_button)
        
        parent_layout.addWidget(actions_group)
    
    def create_nav_button(self, text: str, tooltip: str, section: str, selected: bool = False) -> QPushButton:
        """
        Create a navigation button
        
        Args:
            text (str): Button text
            tooltip (str): Button tooltip
            section (str): Section identifier
            selected (bool): Whether button is initially selected
            
        Returns:
            QPushButton: The created button
        """
        button = QPushButton(text)
        button.setMinimumHeight(45)
        button.setToolTip(tooltip)
        button.setCheckable(True)
        button.setChecked(selected)
        button.setFont(QFont("Arial", 10))
        
        # Set button style
        button.setStyleSheet(self.get_nav_button_style(selected))
        
        # Connect click event
        button.clicked.connect(lambda: self.select_section(section))
        
        return button
    
    def get_nav_button_style(self, selected: bool = False) -> str:
        """
        Get the stylesheet for navigation buttons
        
        Args:
            selected (bool): Whether the button is selected
            
        Returns:
            str: CSS stylesheet
        """
        if selected:
            return """
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: 2px solid #1e7e34;
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #404040;
                    color: white;
                    border: 2px solid #555555;
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: #505050;
                    border-color: #777777;
                }
                QPushButton:checked {
                    background-color: #28a745;
                    border-color: #1e7e34;
                    font-weight: bold;
                }
            """
    
    def setup_connections(self):
        """
        Set up signal-slot connections
        """
        # TODO: Connect to data refresh signals
        pass
    
    def select_section(self, section: str):
        """
        Select a navigation section
        
        Args:
            section (str): The section to select
        """
        # Update current section
        self.current_section = section
        
        # Update button states
        for section_name, button in self.nav_buttons.items():
            is_selected = section_name == section
            button.setChecked(is_selected)
            button.setStyleSheet(self.get_nav_button_style(is_selected))
        
        # Emit section changed signal
        self.section_changed.emit(section)
    
    def request_export(self):
        """
        Request export of call history
        """
        self.export_requested.emit()
    
    def show_missed_calls(self):
        """
        Show missed calls in the history section
        """
        # Select history section and filter for missed calls
        self.select_section("history")
        
        # TODO: Emit signal to filter for missed calls
        # self.filter_requested.emit("missed")
    
    def update_notification_counts(self, voicemail_count: int = 0, missed_calls_count: int = 0):
        """
        Update notification counts on navigation buttons
        
        Args:
            voicemail_count (int): Number of unread voicemails
            missed_calls_count (int): Number of missed calls
        """
        # Update voicemail button text
        voicemail_text = "🔊 Voicemail"
        if voicemail_count > 0:
            voicemail_text += f" ({voicemail_count})"
        self.nav_buttons['voicemail'].setText(voicemail_text)
        
        # Update history button for missed calls indication
        history_text = "📞 Call History"
        if missed_calls_count > 0:
            history_text += f" ({missed_calls_count} missed)"
        self.nav_buttons['history'].setText(history_text)
    
    def get_current_section(self) -> str:
        """
        Get the currently selected section
        
        Returns:
            str: Current section name
        """
        return self.current_section
    
    def highlight_section(self, section: str):
        """
        Temporarily highlight a section (e.g., for notifications)
        
        Args:
            section (str): Section to highlight
        """
        if section in self.nav_buttons:
            button = self.nav_buttons[section]
            
            # TODO: Add temporary highlight animation
            # For now, just briefly change the style
            original_style = button.styleSheet()
            highlight_style = """
                QPushButton {
                    background-color: #ffc107;
                    color: #212529;
                    border: 2px solid #e0a800;
                    border-radius: 8px;
                    text-align: left;
                    padding-left: 15px;
                    font-weight: bold;
                }
            """
            
            button.setStyleSheet(highlight_style)
            
            # TODO: Use QTimer to restore original style after delay
            # QTimer.singleShot(1000, lambda: button.setStyleSheet(original_style))
