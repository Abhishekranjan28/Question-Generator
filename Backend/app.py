from flask import Flask, request, jsonify
import requests
import logging
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Hugging Face API setup
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
HF_API_URL = "https://api-inference.huggingface.co/models/t5-base"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def home():
    return "Welcome to the Question Generator API!"

def generate_questions_with_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,
            "num_return_sequences": 3,
            "num_beams": 3,
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        logging.info(f"Response from Hugging Face API: {result}")
        return result
    except requests.exceptions.HTTPError as e:
        logging.error(f"Hugging Face API HTTP error: {e.response.text}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise

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
        
        # Extract generated questions or handle unexpected responses
        questions = [res.get('generated_text', 'No text generated') for res in result if 'generated_text' in res]
        
        if not questions:
            return jsonify({'error': 'No questions generated.'}), 500

        return jsonify({'questions': questions})
    except requests.exceptions.HTTPError:
        return jsonify({'error': 'Failed to call Hugging Face API. Check API key or model compatibility.'}), 500
    except Exception as e:
        logging.error(f"Error during model prediction: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ensure the port matches the one you are trying to access
