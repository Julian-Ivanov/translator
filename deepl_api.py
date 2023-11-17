# Import necessary libraries
import streamlit as st
import requests
from variables import deepl_key

# Set your DeepL API key here
deepl_api_key = deepl_key

# Define the list of available languages and their language codes
languages = {
    "English": "EN",
    "French": "FR", 
    "Dutch": "NL", 
    "Swedish": "SV",
    "Czech": "CS", 
    "Slovak": "SK",
    "German": "DE", 
}

# Create a function to translate text using DeepL
def translate_text_deepl(text_to_translate, target_language_code, api_key):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        'text': text_to_translate,
        'target_lang': target_language_code
    }
    headers = {
        'Authorization': f'DeepL-Auth-Key {api_key}'
    }
    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code != 200:
        st.error(f"Error: Received status code {response.status_code}")
        return "Translation Error!"
    
    translation_result = response.json()
    if "translations" in translation_result:
        return translation_result["translations"][0]["text"]
    else:
        return "Translation Error!"

# Create the Streamlit web app
def main():
    st.title("DeepL Translation with Streamlit")

    # Input text
    text = st.text_area("Enter the text to translate (Deepl automatically detects the language)")

    # Target language dropdown to select the languages
    target_language = st.selectbox("Select target language", list(languages.keys()))

    # Translate button to translate
    if st.button("Translate"):
        target_language_code = languages[target_language]
        translation = translate_text_deepl(text, target_language_code, deepl_api_key)
        st.markdown(f'<p style="color: blue; font-size: 25px;">{translation}</p>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()