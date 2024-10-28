from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
model = pipeline("text2text-generation", model="t5-base")

@app.route('/generate', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        # Generate questions based on the provided prompt
        result = model(prompt, max_length=100, num_return_sequences=3, num_beams=3)
        questions = [res['generated_text'] for res in result]
        
        return jsonify({'questions': questions})
    except Exception as e:
        app.logger.error(f"Error during model prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
