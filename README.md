# JARVIS 3.0 - Advanced AI Assistant

A modern, feature-rich web interface for JARVIS, powered by Google's Gemini AI.

## Features

✨ **Modern UI/UX**
- Beautiful, responsive design with dark/light theme toggle
- Smooth animations and transitions
- Mobile-friendly interface

💬 **Advanced Chat Features**
- Real-time messaging with typing indicators
- Message history persistence
- Quick suggestion chips
- Export conversations

🎨 **Customization**
- Theme switching (Dark/Light mode)
- Settings panel
- Customizable response settings

🚀 **Performance**
- Fast and responsive
- Optimized for all screen sizes
- Clean, maintainable code

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd JARVIS3.0
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Option 1: Environment variable (Recommended)
   ```bash
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   ```
   
   Option 2: Create a `.env` file
   ```bash
   cp .env.example .env
   # Then edit .env and add your API key
   ```

4. **Run the application (web)**
   ```bash
   set PYTHONPATH=%cd%\src
   python run_web.py
   ```

5. **(Optional) Run the desktop app**
   ```bash
   set PYTHONPATH=%cd%\src
   python run_desktop.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as described above

## Project Structure

```
JARVIS3.0/
├── app.py                 # Web entry wrapper -> jarvis.web
├── run_web.py             # Web runner (adds ./src to PYTHONPATH)
├── run_desktop.py         # Desktop runner (adds ./src)
├── requirements.txt
├── src/
│   └── jarvis/
│       ├── api/           # Gemini + Flask API
│       ├── config/        # Settings/env
│       ├── desktop/       # Tkinter desktop app
│       ├── utils/         # Shared helpers
│       └── web/           # Flask app + assets
│           ├── app.py
│           ├── templates/
│           └── static/
└── README.md
```

## Usage

1. Start the server using `python run_web.py` (after setting `PYTHONPATH` to `./src`)
2. Open the web interface in your browser
3. Type your message and press Enter or click Send
4. Use suggestion chips for quick prompts
5. Access settings via the sidebar
6. Export conversations using the download button

## Features in Detail

### Chat Interface
- **Real-time messaging**: Instant responses from Gemini AI
- **Message history**: Automatically saved and restored
- **Typing indicators**: Visual feedback when AI is processing
- **Quick suggestions**: Pre-defined prompt chips for common tasks

### Customization
- **Theme toggle**: Switch between dark and light modes
- **Settings panel**: Configure API key and preferences
- **Export chat**: Download conversations as text files

### Responsive Design
- Works seamlessly on desktop, tablet, and mobile devices
- Collapsible sidebar for mobile
- Touch-friendly interface

## Troubleshooting

**API Key Issues**
- Make sure your API key is correctly set
- Check that the key has proper permissions
- Verify the key is active in Google AI Studio

**Port Already in Use**
- Change the port in `app.py`: `app.run(port=5001)`

**Module Not Found**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Future Enhancements

- [ ] Voice input/output
- [ ] File upload and analysis
- [ ] Multi-language support
- [ ] Conversation search
- [ ] Custom AI model selection
- [ ] Plugin system

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

Made with ❤️ for AI enthusiasts


