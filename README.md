# Calorie Tracker

A FastAPI-based calorie tracking application with a modern, responsive UI. Track your daily calories, carbs, and protein intake with an easy-to-use interface.

## Features

- Track daily calories, carbohydrates, and protein intake
- Circular progress indicators for visual tracking
- Scan nutrition labels using your camera (requires OpenAI API key)
- Manual entry option for nutrition data
- 30-day history graph with target line
- MongoDB integration for data persistence
- Responsive design that works on all devices

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
MONGODB_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
```

4. Run the application:
```bash
uvicorn main:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

- Click the "Scan" button to use your camera to scan nutrition labels
- Click the "Add" button to manually enter nutrition data
- View your daily progress in the circular indicators
- Track your 30-day history in the graph below

## Requirements

- Python 3.8+
- MongoDB
- OpenAI API key (for nutrition label scanning)
- Modern web browser
- Camera (for scanning feature) 