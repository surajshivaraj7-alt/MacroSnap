# MacroSnap 🥗

MacroSnap is an AI-powered nutrition tracking app built with Streamlit and Google Gemini.

## Features

- 📸 Analyze food photos using AI
- ✍️ Analyze meals using text descriptions
- 🔥 Estimate calories
- 🥩 Estimate protein
- 🍚 Estimate carbohydrates
- 🥑 Estimate fat
- 🎯 Set daily nutrition goals
- 📊 Track daily progress
- 📅 View meal history
- 📈 View 7-day nutrition charts
- 💾 Store meal data locally using SQLite

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- SQLite
- Google GenAI SDK

## Setup

1. Clone this repository.
2. Create a Python virtual environment.
3. Install the required packages.
4. Create `.streamlit/secrets.toml`.
5. Add your Gemini API key:

```toml
GEMINI_API_KEY = "your_api_key_here"