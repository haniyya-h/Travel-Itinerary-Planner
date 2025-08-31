# 🏖️ AI Travel Itinerary Planner

A beautiful AI-powered travel planning application with a modern Streamlit web interface. Create personalized itineraries using multiple Large Language Models (LLMs) with an intuitive, user-friendly design.

## ✨ Features

- **🌐 Beautiful Web Interface**: Modern Streamlit UI with tabs, forms, and responsive design
- **🤖 Multi-LLM Integration**: Uses ChatGroq for day-by-day outlines, Google Gemini for detailed itineraries, and Groq for packing checklists
- **💾 Smart Memory System**: Remembers your preferences across sessions using ConversationBufferMemory
- **🎯 Personalized Planning**: Tailors recommendations based on your stored preferences
- **📋 Comprehensive Output**: Generates day-by-day outlines, detailed itineraries, and packing checklists
- **📚 Trip History**: View and manage your past travel plans
- **❤️ Preference Management**: Add, view, and delete your travel preferences
- **🚀 Easy Setup**: Simple configuration with environment variables

## 🎨 Web Interface

The application features a beautiful, modern web interface with:

- **🗺️ Plan Trip Tab**: Interactive form for destination and duration selection
- **❤️ Preferences Tab**: Manage your travel preferences and likes/dislikes
- **📚 History Tab**: View and manage your past travel plans
- **💡 Tips Sidebar**: Helpful travel planning advice
- **🎨 Custom Styling**: Professional gradient design and responsive layout

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - [Groq](https://console.groq.com/) (for ChatGroq and Groq models)
  - [Google AI Studio](https://makersuite.google.com/app/apikey) (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/haniyya-h/Travel-Itinerary-Planner.git
   cd travel-itinerary-planner
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
   
   **Note:** The requirements.txt now contains only essential packages with compatible versions. If you encounter any issues, you can also install packages individually:
   ```bash
   pip install langchain langchain-groq langchain-google-genai langchain-community streamlit python-dotenv
   ```

4. Set up environment variables using one of these methods:

### Option A: Using .env file (Recommended for development)
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_actual_groq_key_here
GOOGLE_API_KEY=your_actual_google_key_here
LANGCHAIN_TRACING_V2=false
```

### Option B: Setting environment variables in terminal
```bash
export GROQ_API_KEY=your_actual_groq_key_here
export GOOGLE_API_KEY=your_actual_google_key_here
export LANGCHAIN_TRACING_V2=false
```

5. **Run the Streamlit application**
   ```bash
   python run_streamlit.py
   ```
   
   Or directly:
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL

## 🎯 Usage

### Web Interface

1. **Start the application**
   ```bash
   python run_streamlit.py
   ```

2. **Use the web interface**:
   - **Plan Trip**: Enter destination and duration, click "Generate Travel Plan"
   - **Preferences**: Add your travel preferences to personalize future plans
   - **History**: View and manage your past travel plans

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

## 🏗️ Architecture

### Core Components

- **`streamlit_app.py`**: Beautiful web interface using Streamlit
- **`main.py`**: Core application logic and LLM integrations
- **`run_streamlit.py`**: Simple script to start the Streamlit app
- **`OutlineGenerator`**: Uses ChatGroq to create day-by-day travel outlines
- **`DetailedItineraryGenerator`**: Uses Google Gemini to generate detailed itineraries
- **`PackingChecklistGenerator`**: Uses Groq to create personalized packing lists
- **`TravelPlanner`**: Main controller that orchestrates the planning process

### LLM Models Used

- **ChatGroq**: `llama-3.1-8b-instant` for fast outline generation
- **Google Gemini**: `gemini-1.5-flash` for detailed itinerary creation
- **Groq**: `llama-3.1-8b-instant` for packing checklist generation

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

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |
| `LANGCHAIN_TRACING_V2` | Enable/disable LangSmith tracing | No (default: false) |

### API Key Setup

1. **Groq API Key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up/Login and create an API key
   - Copy the key to your `.env` file

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

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

**Problem:** Environment variables not loading
**Solution:** Ensure your `.env` file is in the project root and contains:
```
GROQ_API_KEY=your_actual_groq_key
GOOGLE_API_KEY=your_actual_google_key
LANGCHAIN_TRACING_V2=false
```

### API Key Issues

**Problem:** "GROQ_API_KEY environment variable is required"
**Solution:** 
1. Check your `.env` file exists and has the correct API key
2. Restart the Streamlit app after creating/updating `.env`
3. Verify your API keys are valid and have sufficient credits

### Adding New Features

1. **New LLM Provider**: Add a new generator class following the existing pattern
2. **New Output Format**: Extend the `TravelPlanner.plan_trip()` method
3. **Enhanced Memory**: Modify the `ConversationBufferMemory` configuration
4. **UI Improvements**: Modify `streamlit_app.py` for new interface features

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

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing framework
- [Groq](https://groq.com/) for fast LLM inference
- [Google AI](https://ai.google.dev/) for Gemini models
- [Streamlit](https://streamlit.io/) for the beautiful web interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/travel-itinerary-planner/issues) page
2. Create a new issue with detailed information
3. Include your Python version, OS, and error messages

---

**Happy Travel Planning! ✈️🌍**
