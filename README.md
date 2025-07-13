# 🛒 AI-Powered Grocery List Generator

An intelligent shopping list application that generates personalized grocery lists based on user-inputted dishes, enhanced with AI and YouTube recipe integration.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Groq's LLM to generate comprehensive shopping lists
- 📺 **YouTube Recipe Integration**: Extracts ingredients from YouTube cooking videos
- 🎯 **Smart Categorization**: Automatically categorizes ingredients (Produce, Meat, Dairy, etc.)
- 📋 **Downloadable Lists**: Export shopping lists as text files
- 🍳 **Cooking Tutorials**: Provides relevant YouTube video tutorials
- 👨‍🍳 **Cooking Instructions**: Extracts step-by-step cooking instructions
- 🔄 **Personalization**: Adapts to dietary restrictions and preferences
- 📱 **Modern UI**: Clean, responsive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key (free at [console.groq.com](https://console.groq.com/keys))
- YouTube API key (optional, for enhanced features)

### Installation

1. **Clone or download the project**
   ```bash
   cd AI_shopping_list
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv ai_shopping_env
   source ai_shopping_env/bin/activate  # On Windows: ai_shopping_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script**
   ```bash
   python setup.py
   ```

5. **Configure API keys**
   - Copy `.env.example` to `.env`
   - Add your Groq API key (required)
   - Add your YouTube API key (optional)

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required: Get from https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Optional: Get from https://console.cloud.google.com/
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### API Keys Setup

#### Groq API Key (Required)
1. Visit [console.groq.com](https://console.groq.com/keys)
2. Create a free account
3. Generate an API key
4. Add it to your `.env` file

#### YouTube API Key (Optional)
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add it to your `.env` file

## 📁 Project Structure

```
AI_shopping_list/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── youtube_collector.py   # YouTube API integration
├── recipe_processor.py    # Recipe data processing
├── setup.py              # Setup script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore file
├── README.md            # This file
├── data/                # Recipe data storage
└── models/              # AI model storage
```

## 🎯 Usage

1. **Launch the app**: `streamlit run app.py`
2. **Enter dishes**: Type the dishes you want to cook (one per line)
3. **Generate list**: Click "Generate Shopping List"
4. **Review results**: Check your categorized shopping list
5. **Watch tutorials**: View related YouTube cooking videos
6. **Download**: Export your list as a text file

### Example Input:
```
Spaghetti Carbonara
Caesar Salad
Chocolate Chip Cookies
```

### Example Output:
- **Categorized shopping list** with specific quantities
- **YouTube video tutorials** for each dish
- **Cooking instructions** extracted from videos
- **Downloadable text file** for mobile use

## 🔮 Advanced Features

### YouTube Recipe Integration
- Searches for relevant cooking videos
- Extracts ingredients from video transcripts
- Provides cooking instructions
- Embeds video tutorials in the app

### AI Enhancement
- Uses Groq's LLM for intelligent ingredient prediction
- Considers serving sizes and dietary restrictions
- Merges AI-generated lists with YouTube data
- Provides quantity estimates

### Data Processing
- Cleans and categorizes ingredients
- Removes duplicates and normalizes quantities
- Handles various measurement units
- Extracts cooking steps from transcripts

## 🛠️ Development

### Adding New Features

1. **New ingredient categories**: Edit `recipe_processor.py`
2. **Different AI models**: Update `config.py`
3. **Custom UI components**: Modify `app.py`
4. **Additional data sources**: Create new collector modules

### Testing

```bash
# Run with debug mode
streamlit run app.py --logger.level=debug

# Check API connections
python -c "from config import Config; Config.validate()"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: For providing the AI language model
- **YouTube**: For recipe video data
- **Streamlit**: For the web framework
- **spaCy & NLTK**: For natural language processing

## 🐛 Troubleshooting

### Common Issues

1. **"Import errors"**: Run `python setup.py` to install all dependencies
2. **"API key not found"**: Check your `.env` file configuration
3. **"YouTube features not working"**: Ensure YouTube API key is set
4. **"spaCy model not found"**: Run `python -m spacy download en_core_web_sm`

### Getting Help

- Check the debug information in the app
- Review the console logs
- Ensure all dependencies are installed
- Verify API keys are correctly set

## 🚀 Future Enhancements

- [ ] PDF export functionality
- [ ] Mobile app integration
- [ ] Recipe scaling based on serving size
- [ ] Nutritional information
- [ ] Price estimation
- [ ] Store location integration
- [ ] Recipe recommendations
- [ ] Meal planning features

---

Made with ❤️ using Python, Streamlit, and AI
