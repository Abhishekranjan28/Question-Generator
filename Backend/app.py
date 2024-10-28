from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

# Hugging Face API settings
HF_API_URL = "https://api-inference.huggingface.co/models/t5-base"  # Replace with the specific model you want to use

# Set up headers for API requests
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "application/json"
}

def generate_questions_with_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,
            "num_return_sequences": 3,
            "num_beams": 3,
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

@app.route('/')
def home():
    return "Welcome to the Question Generator API!"

@app.route('/generate', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        # Check if prompt is provided
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400

        # Generate questions based on the provided prompt
        result = generate_questions_with_huggingface(prompt)
        questions = [res['generated_text'] for res in result]

        return jsonify({'questions': questions})
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return jsonify({'error': 'Failed to call Hugging Face API.'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Ensure it listens on all interfaces
