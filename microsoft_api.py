import streamlit as st
import requests
import json
import uuid

# Set your Microsoft Translator API key here
microsoft_translator_api_key = '909ee48eb983487bb43a2dc397ff64e9'

# Define the list of available languages and their language codes
languages = {
    "English": "en",
    "French": "fr",
    "Dutch": "nl",
    "Swedish": "sv",
    "Czech": "cs",
    "Slovak": "sk",
    "German": "de",
}

# Create a function to translate text using Microsoft Translator
def translate_text_microsoft(text_to_translate, target_language_code, api_key):
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate?api-version=3.0"
    params = "&to=" + target_language_code
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': 'germanywestcentral',  # Replace with your region
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text_to_translate}]
    response = requests.post(constructed_url, headers=headers, json=body)

    if response.status_code != 200:
        st.error(f"Error: Received status code {response.status_code}")
        return "Translation Error!"

    translation_result = response.json()
    if translation_result:
        return translation_result[0]["translations"][0]["text"]
    else:
        return "Translation Error!"

# Create the Streamlit web app
def main():
    st.title("Microsoft Translator with Streamlit")

    # Input text
    text = st.text_area("Enter the text to translate (Microsoft Translator automatically detects the language))")

    # Target language dropdown to select the languages
    target_language = st.selectbox("Select target language", list(languages.keys()))

    # Translate button to translate
    if st.button("Translate"):
        target_language_code = languages[target_language]
        translation = translate_text_microsoft(text, target_language_code, microsoft_translator_api_key)
        st.markdown(f'<p style="color: blue; font-size: 25px;">{translation}</p>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
