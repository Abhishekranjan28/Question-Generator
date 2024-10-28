from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API settings
HF_API_URL = "https://api-inference.huggingface.co/models/t5-base"  # Replace with the specific model you want to use
HF_API_TOKEN = "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"  # Replace with your Hugging Face API token

# Set up headers for API requests
headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

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
    app.run(debug=True, port=5000)  # Ensure the port matches the one you are trying to access
