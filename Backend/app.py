
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the Hugging Face API URL and your API key
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/t5-base"
HUGGING_FACE_API_KEY = "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"  # Replace with your API key

# Function to generate questions using Hugging Face API
def generate_questions_with_huggingface(prompt):
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,
            "num_return_sequences": 3,
            "num_beams": 3,
        }
    }

    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

@app.route('/generate', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        # Generate questions based on the provided prompt
        result = generate_questions_with_huggingface(prompt)
        questions = [res['generated_text'] for res in result]

        return jsonify({'questions': questions})
    except Exception as e:
        app.logger.error(f"Error during model prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
