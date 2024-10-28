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
        
        # Create the payload for the Hugging Face API
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 100,
                "num_return_sequences": 3,
                "num_beams": 3
            }
        }
        
        # Make a POST request to the Hugging Face API
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract generated questions from the response
        questions = response.json()
        questions = [res['generated_text'] for res in questions]
        
        return jsonify({'questions': questions})
    except Exception as e:
        app.logger.error(f"Error during model prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ensure the port matches the one you are trying to access
