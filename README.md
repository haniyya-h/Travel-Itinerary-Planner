# 🏖️ AI Travel Itinerary Planner

A beautiful AI-powered travel planning application with a modern Streamlit web interface. Create personalized itineraries using multiple Large Language Models (LLMs) with an intuitive, user-friendly design.

## ✨ Features

- **🌐 Beautiful Web Interface**: Modern Streamlit UI with tabs, forms, and responsive design
- **🤖 Multi-LLM Integration**: Uses ChatGroq for day-by-day outlines, Google Gemini for detailed itineraries, and ChatGroq for packing checklists
- **💾 Smart Memory System**: Remembers your preferences across sessions using ConversationBufferMemory
- **🎯 Personalized Planning**: Tailors recommendations based on your stored preferences
- **📋 Comprehensive Output**: Generates day-by-day outlines, detailed itineraries, and packing checklists
- **📚 Trip History**: View and manage your past travel plans
- **❤️ Preference Management**: Add, view, and delete your travel preferences
- **🔑 Built-in API Key Setup**: User-friendly API key input dialog - no manual .env file creation needed
- **⚙️ API Key Management**: Change API keys anytime through the web interface
- **🚀 Zero-Config Setup**: Just run the app and enter your API keys when prompted

## 🎨 Web Interface

The application features a beautiful, modern web interface with:

- **🔑 API Key Setup Dialog**: First-time setup with guided instructions and validation
- **🗺️ Plan Trip Tab**: Interactive form for destination and duration selection
- **❤️ Preferences Tab**: Manage your travel preferences and likes/dislikes
- **📚 History Tab**: View and manage your past travel plans
- **⚙️ Settings Sidebar**: API key management and status indicators
- **💡 Tips Sidebar**: Helpful travel planning advice
- **🎨 Custom Styling**: Professional gradient design and responsive layout

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - [Groq](https://console.groq.com/) (for ChatGroq models)
  - [Google AI Studio](https://makersuite.google.com/app/apikey) (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/haniyya-h/Travel-Itinerary-Planner.git
   cd Travel-Itinerary-Planner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Set up API keys** 🔑
   - The app will open in your browser
   - You'll see a beautiful API key setup dialog
   - Follow the guided instructions to get your API keys
   - Enter your keys and click "Save Keys & Continue"

6. **Start planning!** ✈️
   - The app will automatically save your API keys
   - You can now plan trips, manage preferences, and view history
   - Change API keys anytime using the sidebar settings

## 🎯 Usage

### Web Interface

1. **Start the application**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **First-time setup**:
   - Enter your Groq and Google Gemini API keys when prompted
   - The app will automatically save them for future use

3. **Use the web interface**:
   - **Plan Trip**: Enter destination and duration, click "Generate Travel Plan"
   - **Preferences**: Add your travel preferences to personalize future plans
   - **History**: View and manage your past travel plans
   - **Settings**: Change API keys or view their status in the sidebar

### Command Line Interface (Alternative)

You can also run the original command-line version:

```bash
python main.py
```

### Adding Preferences

Use the **Preferences** tab to add travel preferences that will be remembered:

- **Nature vs. Culture**: "I prefer nature over museums"
- **Activities**: "I love hiking and swimming"
- **Avoidances**: "I don't like tourist attractions"
- **Food**: "I prefer local cuisine over international chains"

### API Key Management

- **First-time setup**: The app will prompt you to enter API keys when you first run it
- **Change keys**: Use the "Change API Keys" button in the sidebar to update your keys
- **Status indicators**: Check the sidebar to see if your API keys are properly loaded
- **Automatic saving**: Keys are automatically saved to a `.env` file for future use

## 🏗️ Architecture

### Core Components

- **`streamlit_app.py`**: Beautiful web interface using Streamlit with built-in API key management
- **`main.py`**: Core application logic and LLM integrations
- **`run_streamlit.py`**: Simple script to start the Streamlit app
- **`OutlineGenerator`**: Uses ChatGroq to create day-by-day travel outlines
- **`DetailedItineraryGenerator`**: Uses Google Gemini to generate detailed itineraries
- **`PackingChecklistGenerator`**: Uses ChatGroq to create personalized packing lists
- **`TravelPlanner`**: Main controller that orchestrates the planning process

### LLM Models Used

- **ChatGroq**: `llama-3.1-8b-instant` for fast outline generation
- **Google Gemini**: `gemini-1.5-flash` for detailed itinerary creation
- **ChatGroq**: `llama-3.1-8b-instant` for packing checklist generation

## 📁 Project Structure

```
travel-itinerary-planner/
├── streamlit_app.py       # Beautiful Streamlit web interface
├── main.py                # Core application logic
├── run_streamlit.py       # Simple startup script
├── requirements.txt       # Python dependencies
├── env_template.txt      # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # This file
└── .venv/                # Virtual environment (created during setup)
```

## 🔧 Configuration

### Environment Variables

The app automatically manages these environment variables for you:

| Variable | Description | Required | Auto-Managed |
|----------|-------------|----------|--------------|
| `GROQ_API_KEY` | Your Groq API key | Yes | ✅ |
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes | ✅ |
| `LANGCHAIN_TRACING_V2` | Enable/disable LangSmith tracing | No | ✅ |

### API Key Setup

**🎉 No manual setup required!** The app handles everything for you:

1. **Groq API Key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up/Login and create an API key
   - Enter it in the app's API key dialog

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Enter it in the app's API key dialog

The app will automatically:
- ✅ Validate your API keys
- ✅ Save them to a `.env` file
- ✅ Load them for future sessions
- ✅ Show their status in the sidebar

## 🎨 Example Output

### Day-by-Day Outline
```
Day 1: Arrival and City Exploration
- Morning: Arrive in Barcelona, check into hotel
- Afternoon: Explore Las Ramblas and Gothic Quarter
- Evening: Traditional Catalan dinner

Day 2: Architecture and Culture
- Morning: Visit Sagrada Familia
- Afternoon: Park Güell exploration
- Evening: Flamenco show
```

### Detailed Itinerary
```
Day 1: Arrival and City Exploration
Morning (9:00 AM - 12:00 PM):
- Arrive at Barcelona-El Prat Airport
- Take Aerobus to city center (€5.90)
- Check into Hotel Casa Fuster (5-star, €200/night)
- Light breakfast at Café de l'Opera

Afternoon (1:00 PM - 6:00 PM):
- Walk along Las Ramblas (free)
- Visit La Boqueria Market (free entry)
- Explore Gothic Quarter (free)
- Visit Barcelona Cathedral (€7)

Evening (7:00 PM - 10:00 PM):
- Dinner at Can Culleretes (€25-35)
- Traditional Catalan cuisine
- Walk through Plaça Reial
```

### Packing Checklist
```
Essential Items:
- Passport and travel documents
- Travel insurance documents
- Credit cards and cash (Euros)
- Phone and charger
- Universal adapter

Clothing:
- 5-7 lightweight shirts
- 2-3 pairs of pants/shorts
- 1 light jacket
- Comfortable walking shoes
- Swimsuit (for beach visits)

Electronics:
- Camera or smartphone
- Power bank
- Headphones
- Laptop (if needed for work)
```

## 🛠️ Development

### Running Tests

```bash
python APITesting.py
```

## 🔧 Troubleshooting

### Installation Issues

**Problem:** `pip install -r requirements.txt` fails with dependency conflicts
**Solution:** Install packages individually:
```bash
pip install langchain langchain-groq langchain-google-genai langchain-community streamlit python-dotenv
```

**Problem:** Port 8501 is already in use
**Solution:** Stop any existing Streamlit processes or use a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### API Key Issues

**Problem:** "Invalid API Key" error
**Solution:** 
1. Use the "Change API Keys" button in the sidebar to re-enter your keys
2. Verify your API keys are valid and have sufficient credits
3. Check the sidebar for API key status indicators

**Problem:** API key dialog not appearing
**Solution:**
1. Delete the `.env` file if it exists
2. Restart the Streamlit app
3. The API key dialog should appear on first launch

**Problem:** API keys not saving
**Solution:**
1. Make sure you have write permissions in the project directory
2. Check that the `.env` file is not read-only
3. Try using the "Change API Keys" button to re-save them

### Adding New Features

1. **New LLM Provider**: Add a new generator class following the existing pattern
2. **New Output Format**: Extend the `TravelPlanner.plan_trip()` method
3. **Enhanced Memory**: Modify the `ConversationBufferMemory` configuration
4. **UI Improvements**: Modify `streamlit_app.py` for new interface features
5. **API Key Providers**: Add support for additional AI services in the API key dialog

### Dependencies

- `streamlit`: Beautiful web interface framework
- `langchain`: Core LangChain framework
- `langchain-groq`: Groq integration
- `langchain-google-genai`: Google Gemini integration
- `langchain-community`: Community integrations
- `python-dotenv`: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆕 Recent Updates

### Version 2.0 - Enhanced User Experience
- ✅ **Built-in API Key Management**: No more manual `.env` file creation
- ✅ **User-Friendly Setup**: Beautiful API key input dialog with validation
- ✅ **Real-time Status Indicators**: See API key status in the sidebar
- ✅ **One-Click Key Updates**: Change API keys anytime through the interface
- ✅ **Model Updates**: Updated to use supported Groq models
- ✅ **Zero-Config Setup**: Just run the app and enter your keys when prompted

### What's New
- 🔑 **API Key Dialog**: First-time users see a guided setup process
- ⚙️ **Settings Sidebar**: Manage API keys and view their status
- 🎨 **Enhanced UI**: Improved styling and user experience
- 🚀 **Simplified Installation**: Reduced setup steps from 7 to 4

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing framework
- [Groq](https://groq.com/) for fast LLM inference
- [Google AI](https://ai.google.dev/) for Gemini models
- [Streamlit](https://streamlit.io/) for the beautiful web interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/haniyya-h/travel-itinerary-planner/issues) page
2. Create a new issue with detailed information
3. Include your Python version, OS, and error messages

---

**Happy Travel Planning! ✈️🌍**
