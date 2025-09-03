#!/bin/bash

echo "🌍 Setting up TransCultura Demo..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv transcultura_env

# Activate virtual environment
echo "Activating virtual environment..."
source transcultura_env/bin/activate  # For Linux/Mac
# For Windows use: transcultura_env\Scripts\activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if Ollama is running
echo "Checking Ollama connection..."
curl -s http://localhost:11434/api/version > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    echo "   ollama run llama3.2:3b"
    exit 1
fi

# Create directories
mkdir -p transcultura_db

echo "🚀 Setup complete! Run the demo with:"
echo "streamlit run transcultura_demo.py"