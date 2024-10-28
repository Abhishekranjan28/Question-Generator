import os
import requests
import logging
from flask import Flask, request, jsonify

# Initialize Flask app and set up logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Get the Hugging Face API key from environment variables
HUGGING_FACE_API_KEY = os.environ.get('HUGGING_FACE_API_KEY')
HF_API_URL = "https://api-inference.huggingface.co/models/t5-base"  # Example model URL

# Ensure the API key is available
if not HUGGING_FACE_API_KEY:
    logging.error("Hugging Face API key is not set in the environment.")
    raise EnvironmentError("Missing API key for Hugging Face")

# Set up headers for API requests
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "application/json"
}

# Home route
@app.route('/')
def home():
    return "Welcome to the Question Generator API!"

# Function to generate questions using Hugging Face API
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
        # API call to Hugging Face
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an error for non-200 responses
        logging.info(f"Response from Hugging Face: {response.json()}")  # Log the response
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Hugging Face API returned an error: {e.response.text}")  # Log the error response
        raise  # Re-raise to be caught in the route

# Route to handle question generation
@app.route('/generate', methods=['POST'])
def generate_questions():
    data = request.get_json()
    prompt = data.get('prompt')
    
    # Validate the input prompt
    if not prompt:
        return jsonify({'error': 'Prompt is required.'}), 400

    try:
        # Generate questions based on the provided prompt
        result = generate_questions_with_huggingface(prompt)
        # Extract 'generated_text' from the result if the API response contains it
        questions = [res['generated_text'] for res in result if 'generated_text' in res]

        # Handle case where no questions are returned
        if not questions:
            return jsonify({'error': 'No questions generated. Try a different prompt.'}), 500

        return jsonify({'questions': questions})

    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return jsonify({'error': 'Failed to call Hugging Face API.'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error.'}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Adjust port if needed for Render
