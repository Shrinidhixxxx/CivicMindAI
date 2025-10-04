#!/bin/bash
# CivicMindAI Quick Start Script

echo "🤖 Starting CivicMindAI - Chennai Civic Assistant"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# Start the application
echo "🚀 Starting CivicMindAI..."
echo "📱 Open http://localhost:8501 in your browser"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run main.py
