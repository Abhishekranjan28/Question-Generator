import streamlit as st
import requests

# Backend URL (adjust if needed)
BACKEND_URL = "http://localhost:5000/generate"

st.title("Question Generation System")
st.write("Enter the following details to generate questions:")

# Text inputs for user to provide details
product_name = st.text_input("Product Name:")
organization = st.text_input("Organization Making It:")
place = st.text_input("Place of Production:")

# Button to generate questions
if st.button("Generate Questions"):
    if not product_name.strip() or not organization.strip() or not place.strip():
        st.error("Please enter all fields.")
    else:
        try:
            # Create a prompt based on user inputs
            prompt = f"Generate questions based on the following details:\nProduct Name: {product_name}\nOrganization: {organization}\nPlace: {place}"
            # Send POST request to the backend
            response = requests.post(BACKEND_URL, json={'prompt': prompt})
            response.raise_for_status()  # Raise error for bad responses
            data = response.json()
            
            # Display generated questions
            if 'questions' in data:
                st.write("Generated Questions:")
                for idx, question in enumerate(data['questions'], 1):
                    st.write(f"{idx}. {question}")
            else:
                st.error("Failed to generate questions.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
