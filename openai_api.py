# Import necessary libraries
import streamlit as st
import openai
from variables import openai_key

# Set the OpenAI API key
openai.api_key = openai_key

# Define the list of available languages
languages = [
    "English",
    "French", 
    "Dutch", 
    "Swedish", 
    "Czech", 
    "Slovak",
    "German"
]

# Create a function to translate text
def translate_text(text, source_language, target_language):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Translate the following text from {source_language} to {target_language}:\n{text}",
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.0,  # Updated temperature to 0.0
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    translation = response.choices[0].text.strip().split("\n")[0]
    return translation

# Create the Streamlit web app
def main():
    st.title("text-davinci-003 Translation with Streamlit")

    # Input text
    text = st.text_area("Enter the text to translate")

    # Source language dropdown to select the languages
    source_language = st.selectbox("Select source language", languages)

    # Target language dropdown to select the languages
    target_language = st.selectbox("Select target language", languages)

    # Translate button to translate
    if st.button("Translate"):
        translation = translate_text(text, source_language, target_language)
        st.markdown(f'<p style="color: blue; font-size: 25px;">{translation}</p>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
