# Project Structure Overview

## 📁 File Structure

```
Call-twilio/
│
├── 📄 main.py                 # Application entry point
├── 📄 setup.py                # Setup and installation script
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md               # Project documentation
├── 📄 .env.template           # Environment variables template
├── 📄 run.bat                 # Windows batch script to run app
├── 📄 run.ps1                 # PowerShell script to run app
├── 📄 PROJECT_STRUCTURE.md    # This file
│
└── 📁 src/                    # Source code directory
    │
    ├── 📄 __init__.py
    │
    ├── 📁 gui/                # User Interface Components
    │   ├── 📄 __init__.py
    │   ├── 📄 main_window.py      # Main application window
    │   ├── 📄 popup_dialer.py     # Popup dialer window
    │   │
    │   └── 📁 components/     # UI Component Modules
    │       ├── 📄 __init__.py
    │       ├── 📄 dialer_widget.py      # Phone dialer interface
    │       ├── 📄 sidebar_navigation.py # Left navigation panel
    │       └── 📄 content_area.py       # Main content display area
    │
    ├── 📁 services/           # Business Logic Services
    │   ├── 📄 __init__.py
    │   ├── 📄 call_service.py     # Twilio API integration
    │   ├── 📄 database_service.py # Supabase database operations
    │   └── 📄 export_service.py   # Data export functionality
    │
    └── 📁 utils/              # Utility Modules
        ├── 📄 __init__.py
        └── 📄 config.py           # Configuration management
```

## 🎯 Component Overview

### Core Application Files

- **`main.py`**: Entry point that initializes PyQt5 application and shows main window
- **`setup.py`**: Interactive setup script for initial configuration
- **`requirements.txt`**: All Python dependencies including PyQt5, Twilio SDK, Supabase

### GUI Architecture

#### Main Window (`gui/main_window.py`)
- Primary application window
- Manages layout with splitter (sidebar + content area + dialer)
- Handles menu bar, toolbar, and status bar
- Coordinates between components
- Manages popup mode switching

#### Popup Dialer (`gui/popup_dialer.py`)
- Compact, always-on-top dialer window
- Frameless window with custom title bar
- Bottom navigation tabs (Recent, Favorites, Voicemail)
- Draggable interface

#### Components

1. **Dialer Widget** (`components/dialer_widget.py`)
   - Phone number input with validation
   - Caller ID selection dropdown
   - Numeric keypad
   - Call/hangup controls
   - Format validation and phone number cleaning

2. **Sidebar Navigation** (`components/sidebar_navigation.py`)
   - Navigation between sections (History, Voicemail, Contacts, Settings, Analytics)
   - Export button
   - Quick action buttons
   - Notification badges

3. **Content Area** (`components/content_area.py`)
   - Stacked widget for different sections
   - Call history table with search/filter
   - Placeholder sections for voicemail, contacts, settings, analytics
   - Export functionality

### Service Layer

#### Call Service (`services/call_service.py`)
- Twilio API integration for making calls
- Call status tracking and management
- Phone number validation
- Call history retrieval
- Recording URL management

#### Database Service (`services/database_service.py`)
- Supabase integration for data persistence
- CRUD operations for call history, contacts, voicemails
- User settings management
- Data export queries

#### Export Service (`services/export_service.py`)
- Export to Excel, CSV, JSON formats
- Data formatting and validation
- File path generation
- Analytics report generation

### Configuration

#### Config Module (`utils/config.py`)
- Environment variable management
- Application settings and defaults
- Twilio and Supabase configuration validation
- UI dimensions and preferences

## 🔧 Key Features Implemented

### ✅ Completed Features

1. **Professional GUI Framework**
   - Dark theme with modern styling
   - Responsive layout with resizable panels
   - Professional button styling and hover effects

2. **Dialer Interface**
   - Number input with paste support
   - Caller ID selection (Hidden, Company, Toll Free)
   - Visual keypad with click functionality
   - Call/hangup state management

3. **Navigation System**
   - Sidebar with section switching
   - Visual feedback for active sections
   - Quick action buttons

4. **Popup Mode**
   - Compact dialer window
   - Always-on-top functionality
   - Bottom tab navigation
   - Draggable interface

5. **Data Management Framework**
   - Service layer architecture
   - Database abstraction
   - Export system foundation

6. **Configuration System**
   - Environment variable management
   - Settings validation
   - Flexible configuration options

### 🔄 Backend Integration Points

All backend functionality is prepared with placeholder comments:

1. **Twilio Integration**: Uncomment Twilio client code in `call_service.py`
2. **Supabase Integration**: Uncomment database code in `database_service.py`
3. **Export Features**: Uncomment pandas/openpyxl code in `export_service.py`

### 📱 UI/UX Design Features

1. **Responsive Design**
   - Splitter layouts for resizable panels
   - Minimum and maximum size constraints
   - Proper stretch factors

2. **User-Friendly Interface**
   - Clear visual hierarchy
   - Intuitive navigation
   - Keyboard shortcuts
   - Tooltips and help text

3. **Professional Styling**
   - Consistent color scheme
   - Modern button designs
   - Proper spacing and alignment
   - Visual feedback for interactions

4. **Accessibility**
   - Keyboard navigation support
   - Clear contrast ratios
   - Readable fonts and sizing

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   python setup.py  # Interactive setup
   # OR
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your credentials
   ```

3. **Run Application**:
   ```bash
   python main.py
   # OR use the run scripts:
   # Windows: run.bat
   # PowerShell: run.ps1
   ```

## 📊 Development Workflow

### Adding New Features

1. **GUI Components**: Add to `src/gui/components/`
2. **Business Logic**: Add to `src/services/`
3. **Configuration**: Update `src/utils/config.py`
4. **Integration**: Connect in `main_window.py`

### Backend Integration

1. Uncomment service code
2. Install additional dependencies
3. Set up database schema
4. Configure API credentials

### Testing

1. GUI testing: Run without backend setup
2. Service testing: Mock external APIs
3. Integration testing: Use development credentials

This structure provides a solid foundation for a professional Twilio calling dashboard with room for future enhancements and backend integration.
