"""
Setup script for Twilio Calling Dashboard
Helps with initial configuration and dependency installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🚀 Twilio Calling Dashboard Setup")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\nTry installing manually:")
        print("pip install -r requirements.txt")
        return False


def setup_environment_file():
    """Set up the .env file from template"""
    print("\nSetting up environment configuration...")
    
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    if template_file.exists():
        shutil.copy(template_file, env_file)
        print("✅ Created .env file from template")
        print("\n📝 Next steps:")
        print("1. Edit the .env file with your actual credentials")
        print("2. Add your Twilio Account SID and Auth Token")
        print("3. Add your Supabase URL and API Key")
        return True
    else:
        print("❌ .env.template file not found")
        return False


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        "exports",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_twilio_credentials():
    """Check if Twilio credentials are configured"""
    print("\nChecking Twilio configuration...")
    
    # Try to load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if account_sid and auth_token and phone_number:
            print("✅ Twilio credentials found in .env file")
            return True
        else:
            print("⚠️  Twilio credentials not configured")
            print("Please edit the .env file with your Twilio credentials")
            return False
            
    except ImportError:
        print("⚠️  python-dotenv not installed - skipping credential check")
        return False


def check_supabase_credentials():
    """Check if Supabase credentials are configured"""
    print("\nChecking Supabase configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if supabase_url and supabase_key:
            print("✅ Supabase credentials found in .env file")
            return True
        else:
            print("⚠️  Supabase credentials not configured")
            print("Please edit the .env file with your Supabase credentials")
            return False
            
    except ImportError:
        print("⚠️  python-dotenv not installed - skipping credential check")
        return False


def test_application():
    """Test if the application can start"""
    print("\nTesting application startup...")
    
    try:
        # Try importing the main modules
        sys.path.append('src')
        from utils.config import AppConfig
        from services.call_service import CallService
        
        config = AppConfig()
        print("✅ Application modules loaded successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Edit the .env file with your actual credentials:")
    print("   - Twilio Account SID and Auth Token")
    print("   - Twilio phone numbers")
    print("   - Supabase URL and API Key")
    print("\n2. Run the application:")
    print("   python main.py")
    print("\n3. Switch to popup mode with Ctrl+P")
    print("\n4. Export call history using the Export button")
    print("\n📚 For more information, see README.md")
    print("\n💡 Tip: The application works without backend integration")
    print("   for GUI testing and development.")


def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Continuing with partial setup...")
    
    # Set up environment file
    setup_environment_file()
    
    # Create directories
    create_directories()
    
    # Check credentials (optional)
    check_twilio_credentials()
    check_supabase_credentials()
    
    # Test application
    test_application()
    
    # Print next steps
    print_next_steps()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
