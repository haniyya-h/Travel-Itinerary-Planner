#!/usr/bin/env python3
"""
Streamlit Travel Itinerary Planner
A beautiful web interface for the AI Travel Planner using Streamlit
"""

import streamlit as st
import os
import sys
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path to import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import TravelPlanner
except ImportError as e:
    st.error(f"Error importing TravelPlanner: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🏖️ AI Travel Itinerary Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        color: #262730;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'travel_planner' not in st.session_state:
    st.session_state.travel_planner = None
if 'trip_history' not in st.session_state:
    st.session_state.trip_history = []
if 'preferences' not in st.session_state:
    st.session_state.preferences = []
if 'api_keys_configured' not in st.session_state:
    st.session_state.api_keys_configured = False
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ""
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = ""

def save_api_keys_to_env(groq_key, google_key):
    """Save API keys to .env file"""
    try:
        env_content = f"""# Travel Itinerary Planner API Keys
GROQ_API_KEY={groq_key}
GOOGLE_API_KEY={google_key}

# Optional: LangChain Configuration
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=travel_planner

# Application Configuration
APP_NAME=Travel Itinerary Planner
DEBUG=true
LOG_LEVEL=INFO
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        return True
    except Exception as e:
        st.error(f"Error saving API keys: {e}")
        return False

def show_api_key_dialog():
    """Show API key input dialog"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1>🏖️ AI Travel Itinerary Planner</h1>
        <p>Welcome! Let's get you started by setting up your API keys.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Keys Setup")
    st.markdown("""
    This app uses two AI services to create your travel plans:
    - **Groq**: For fast day-by-day planning and packing lists
    - **Google Gemini**: For detailed itineraries with specific recommendations
    
    You'll need to get API keys from both services (they're free to use):
    """)
    
    with st.expander("📋 How to get API keys", expanded=False):
        st.markdown("""
        **Groq API Key:**
        1. Visit [Groq Console](https://console.groq.com/)
        2. Sign up/Login to your account
        3. Go to API Keys section
        4. Create a new API key
        5. Copy the key (starts with `gsk_...`)
        
        **Google Gemini API Key:**
        1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API key"
        4. Copy the generated key
        """)
    
    with st.form("api_keys_form"):
        st.subheader("Enter Your API Keys")
        
        groq_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Your Groq API key (starts with 'gsk_')"
        )
        
        google_key = st.text_input(
            "🔑 Google Gemini API Key",
            type="password",
            placeholder="AI...",
            help="Your Google Gemini API key"
        )
        
        submitted = st.form_submit_button("🚀 Save Keys & Continue", use_container_width=True)
        
        if submitted:
            if not groq_key or not google_key:
                st.error("❌ Please enter both API keys")
            elif not groq_key.startswith("gsk_"):
                st.error("❌ Groq API key should start with 'gsk_'")
            else:
                # Save keys to session state
                st.session_state.groq_api_key = groq_key
                st.session_state.google_api_key = google_key
                
                # Save to .env file
                if save_api_keys_to_env(groq_key, google_key):
                    # Reload environment variables from .env file
                    load_dotenv(override=True)
                    
                    # Set environment variables for current session
                    os.environ["GROQ_API_KEY"] = groq_key
                    os.environ["GOOGLE_API_KEY"] = google_key
                    os.environ["LANGCHAIN_TRACING_V2"] = "false"
                    
                    st.session_state.api_keys_configured = True
                    st.success("✅ API keys saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save API keys")

def initialize_travel_planner():
    """Initialize the TravelPlanner instance"""
    # Always reload environment variables to ensure we have the latest keys
    load_dotenv(override=True)
    
    if st.session_state.travel_planner is None:
        try:
            # Check for required environment variables
            groq_key = os.getenv("GROQ_API_KEY")
            google_key = os.getenv("GOOGLE_API_KEY")
            
            if not groq_key:
                st.error("❌ GROQ_API_KEY environment variable is required")
                st.info("Please set your Groq API key in the environment variables")
                return False
            if not google_key:
                st.error("❌ GOOGLE_API_KEY environment variable is required")
                st.info("Please set your Google Gemini API key in the environment variables")
                return False
            
            # Set LangChain tracing to false if not already set
            if not os.getenv("LANGCHAIN_TRACING_V2"):
                os.environ["LANGCHAIN_TRACING_V2"] = "false"
            
            st.session_state.travel_planner = TravelPlanner()
            st.success("✅ TravelPlanner initialized successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Error initializing TravelPlanner: {e}")
            return False
    return True

def main():
    """Main Streamlit application"""
    
    # Check if API keys are configured
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    # If no API keys are found, show the API key dialog
    if not groq_key or not google_key:
        show_api_key_dialog()
        return
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏖️ AI Travel Itinerary Planner</h1>
        <p>Powered by ChatGroq & Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize TravelPlanner
    if not initialize_travel_planner():
        st.stop()
    
    # Sidebar for API key management
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Show API key status
        groq_status = "✅" if os.getenv("GROQ_API_KEY") else "❌"
        google_status = "✅" if os.getenv("GOOGLE_API_KEY") else "❌"
        st.markdown(f"**API Keys Status:**")
        st.markdown(f"- Groq: {groq_status}")
        st.markdown(f"- Google: {google_status}")
        
        if st.button("🔑 Change API Keys"):
            # Clear the .env file and session state to force re-entry
            if os.path.exists('.env'):
                os.remove('.env')
            # Clear environment variables
            if 'GROQ_API_KEY' in os.environ:
                del os.environ['GROQ_API_KEY']
            if 'GOOGLE_API_KEY' in os.environ:
                del os.environ['GOOGLE_API_KEY']
            # Reset TravelPlanner instance
            st.session_state.travel_planner = None
            st.session_state.api_keys_configured = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - **Be specific** about your destination
        - **Add preferences** to personalize your plans
        - **Check the weather** for your travel dates
        - **Book accommodations** in advance
        """)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Plan Trip", "❤️ Preferences", "📚 History"])
    
    with tab1:
        st.header("🗺️ Plan Your Dream Trip")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Trip planning form
            with st.form("trip_form"):
                st.subheader("Trip Details")
                
                destination = st.text_input(
                    "📍 Destination",
                    placeholder="e.g., Spain, Japan, Costa Rica",
                    help="Enter the country or city you want to visit"
                )
                
                duration = st.selectbox(
                    "📅 Trip Duration",
                    options=[3, 5, 7, 10, 14, 21, 30],
                    format_func=lambda x: f"{x} days",
                    help="Select the duration of your trip"
                )
                
                submitted = st.form_submit_button("🚀 Generate Travel Plan", use_container_width=True)
                
                if submitted:
                    if not destination:
                        st.error("Please enter a destination")
                    else:
                        with st.spinner("🌍 Creating your personalized travel plan..."):
                            try:
                                result = st.session_state.travel_planner.plan_trip(destination, duration)
                                
                                # Store in history
                                trip_data = {
                                    "destination": destination,
                                    "duration": duration,
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "result": result
                                }
                                st.session_state.trip_history.insert(0, trip_data)
                                
                                st.success("🎉 Travel plan generated successfully!")
                                
                                # Display results
                                st.markdown("---")
                                
                                # Day-by-day outline
                                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                                st.subheader("📋 Day-by-Day Outline")
                                st.markdown(result["outline"])
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Detailed itinerary
                                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                                st.subheader("📅 Detailed Itinerary")
                                st.markdown(result["detailed_itinerary"])
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Packing checklist
                                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                                st.subheader("🎒 Packing Checklist")
                                st.markdown(result["packing_checklist"])
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.error(f"❌ Error generating travel plan: {e}")
        
        with col2:
            # Current preferences display
            if st.session_state.preferences:
                st.markdown("### ❤️ Your Preferences")
                for i, pref in enumerate(st.session_state.preferences):
                    st.markdown(f"• {pref}")
            else:
                st.info("💡 Add preferences in the Preferences tab to personalize your travel plans!")
    
    with tab2:
        st.header("❤️ Your Travel Preferences")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Add new preference
            with st.form("preference_form"):
                st.subheader("Add New Preference")
                
                preference = st.text_area(
                    "What do you prefer?",
                    placeholder="e.g., I prefer nature over museums, I love hiking and swimming, I don't like tourist attractions",
                    height=100,
                    help="Describe your travel preferences, likes, and dislikes"
                )
                
                submitted = st.form_submit_button("💾 Save Preference", use_container_width=True)
                
                if submitted:
                    if not preference.strip():
                        st.error("Please enter a preference")
                    else:
                        try:
                            st.session_state.travel_planner.add_preference(preference.strip())
                            st.session_state.preferences.append(preference.strip())
                            st.success("✅ Preference saved successfully!")
                        except Exception as e:
                            st.error(f"❌ Error saving preference: {e}")
        
        with col2:
            # Display stored preferences
            st.subheader("📝 Stored Preferences")
            
            if st.session_state.preferences:
                for i, pref in enumerate(st.session_state.preferences):
                    col_pref, col_del = st.columns([4, 1])
                    with col_pref:
                        st.markdown(f"• {pref}")
                    with col_del:
                        if st.button("🗑️", key=f"del_{i}", help="Delete preference"):
                            try:
                                st.session_state.preferences.pop(i)
                                st.rerun()
                            except:
                                pass
            else:
                st.info("No preferences stored yet. Add some to personalize your travel plans!")
    
    with tab3:
        st.header("📚 Trip History")
        
        if st.session_state.trip_history:
            for i, trip in enumerate(st.session_state.trip_history):
                with st.expander(f"🗺️ {trip['destination']} - {trip['duration']} days ({trip['date']})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("**Day-by-Day Outline:**")
                        st.markdown(trip['result']['outline'][:500] + "..." if len(trip['result']['outline']) > 500 else trip['result']['outline'])
                        
                        if st.button("📖 View Full Plan", key=f"view_{i}"):
                            st.markdown("### 📋 Full Day-by-Day Outline")
                            st.markdown(trip['result']['outline'])
                            
                            st.markdown("### 📅 Full Detailed Itinerary")
                            st.markdown(trip['result']['detailed_itinerary'])
                            
                            st.markdown("### 🎒 Full Packing Checklist")
                            st.markdown(trip['result']['packing_checklist'])
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{i}"):
                            st.session_state.trip_history.pop(i)
                            st.rerun()
        else:
            st.info("No trips planned yet. Start planning your first adventure!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏖️ AI Travel Itinerary Planner | Built with ❤️ using LangChain, ChatGroq & Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
