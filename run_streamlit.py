#!/usr/bin/env python3
"""
Simple script to run the Streamlit Travel Itinerary Planner
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    print("🏖️ Starting AI Travel Itinerary Planner...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit==1.28.0"])
        print("✅ Streamlit installed successfully!")
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ main.py not found! Please make sure you're in the correct directory.")
        return
    
    # Check if streamlit_app.py exists
    if not os.path.exists('streamlit_app.py'):
        print("❌ streamlit_app.py not found!")
        return
    
    print("🌐 Starting Streamlit server...")
    print("📝 The app will open in your default browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()
