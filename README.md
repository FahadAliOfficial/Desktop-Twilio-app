# Twilio Calling Dashboard

A professional, user-friendly GUI application for managing Twilio calls with advanced features including call history, voicemail management, and data export capabilities.

## Features

- **Professional Dialer Interface**: Intuitive keypad with caller ID options
- **Call History Management**: Complete call tracking with search and filtering
- **Voicemail Integration**: Access and manage voicemail messages
- **Contact Management**: Store and organize contacts
- **Popup Mode**: Compact, always-on-top dialer for quick access
- **Data Export**: Export call history to Excel, CSV, or JSON formats
- **Analytics Dashboard**: Call statistics and reporting
- **Supabase Integration**: Cloud database for data persistence

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.template` to `.env`
   - Fill in your Twilio and Supabase credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_key
   ```

4. **Run the application**:
   ```powershell
   python main.py
   ```

## Project Structure

```
Call-twilio/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.template              # Environment variables template
├── README.md                  # This file
└── src/
    ├── gui/                   # User interface components
    │   ├── main_window.py     # Main application window
    │   ├── popup_dialer.py    # Popup dialer window
    │   └── components/        # UI components
    │       ├── dialer_widget.py      # Dialer interface
    │       ├── sidebar_navigation.py # Navigation sidebar
    │       └── content_area.py       # Main content area
    ├── services/              # Business logic services
    │   ├── call_service.py    # Twilio API integration
    │   ├── database_service.py # Supabase integration
    │   └── export_service.py  # Data export functionality
    └── utils/                 # Utility modules
        └── config.py          # Configuration management
```

## Usage

### Main Window Mode

1. **Making Calls**:
   - Enter phone number in the dialer
   - Select caller ID option (Hidden, Company, Toll Free)
   - Click "CALL" to initiate

2. **Navigation**:
   - Use the left sidebar to navigate between sections
   - Call History: View and search past calls
   - Voicemail: Access voicemail messages
   - Contacts: Manage contact list
   - Settings: Configure application
   - Analytics: View call statistics

3. **Export Data**:
   - Click "Export Call History" button
   - Choose format (Excel, CSV, JSON)
   - Data will be saved to exports/ folder

### Popup Mode

1. **Activate Popup Mode**:
   - Click "Popup Mode" button in main window
   - Or use Ctrl+P keyboard shortcut

2. **Popup Features**:
   - Compact dialer interface
   - Bottom navigation tabs (Recent, Favorites, Voicemail)
   - Always stays on top
   - Draggable window

3. **Return to Main Window**:
   - Click the minimize button (🔽)
   - Popup closes and main window appears

## Configuration

### Caller ID Options

- **Hide Caller ID**: Calls appear as anonymous
- **Company Number**: Uses your Twilio phone number
- **Toll Free Number**: Uses your toll-free number (if configured)

### Data Storage

The application uses Supabase for cloud data storage:
- Call history and metadata
- Contact information
- Voicemail records
- User settings and preferences

### Customization

You can customize the application by modifying:
- `src/utils/config.py`: Application settings
- GUI styles in the component files
- Export formats in `src/services/export_service.py`

## Development

### Adding Backend Functionality

The GUI is complete with placeholder comments for backend integration:

1. **Twilio Integration**: Uncomment Twilio client code in `call_service.py`
2. **Supabase Integration**: Uncomment Supabase code in `database_service.py`
3. **Data Export**: Uncomment pandas/openpyxl code in `export_service.py`

### Database Schema

When setting up Supabase, create these tables:

- `call_history`: Call records and metadata
- `contacts`: Contact information
- `voicemails`: Voicemail records
- `user_settings`: User preferences

### Custom Features

To add new features:
1. Create new components in `src/gui/components/`
2. Add business logic in `src/services/`
3. Update navigation in `sidebar_navigation.py`
4. Add content sections in `content_area.py`

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Configuration Errors**: Check that `.env` file has correct Twilio/Supabase credentials
3. **Permission Issues**: Ensure the application has permission to create files in the exports/ directory

### Logs

The application logs important events. Check the console output for debugging information.

## Licence

MIT License

Copyright (c) 2026 Fahad Ali


## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments for implementation guidance
3. Ensure all environment variables are properly configured
