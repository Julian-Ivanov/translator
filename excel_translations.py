import streamlit as st
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import requests
import uuid
from io import BytesIO

# DeepL API key
deepl_api_key = '25f727f2-4270-6944-171f-da78e41dcef0:fx'

# Microsoft Translator API key
microsoft_translator_api_key = '909ee48eb983487bb43a2dc397ff64e9'

# Function to translate text using DeepL
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
        print(f"Error: Received status code {response.status_code}")
        return "Translation Error"
    
    translation_result = response.json()
    if "translations" in translation_result:
        return translation_result["translations"][0]["text"]
    else:
        return "Translation Error"

# Function to translate text using Microsoft Translator
def translate_text_microsoft(text_to_translate, target_language_code, api_key):
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate?api-version=3.0"
    params = "&to=" + target_language_code
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': 'germanywestcentral',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text_to_translate}]
    response = requests.post(constructed_url, headers=headers, json=body)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return "Translation Error!"

    translation_result = response.json()
    if translation_result:
        return translation_result[0]["translations"][0]["text"]
    else:
        return "Translation Error!"

def translate_excel(file):
    # Load the workbook from the uploaded file
    workbook = load_workbook(filename=BytesIO(file.read()))

    # Define languages for DeepL and Microsoft Translator
    deepl_languages = {
        "English": {"code": "EN", "column": "B"},
        "French": {"code": "FR", "column": "C"},
        "Dutch": {"code": "NL", "column": "D"},
        "Swedish": {"code": "SV", "column": "E"},
        "Czech": {"code": "CS", "column": "F"},
        "Slovak": {"code": "SK", "column": "G"},
    }

    microsoft_languages = {
        "English": {"code": "en", "column": "B"},
        "French": {"code": "fr", "column": "C"},
        "Dutch": {"code": "nl", "column": "D"},
        "Swedish": {"code": "sv", "column": "E"},
        "Czech": {"code": "cs", "column": "F"},
        "Slovak": {"code": "sk", "column": "G"},
    }

    # Function to update a cell with translation while preserving formatting
    def update_cell(sheet, cell_ref, new_value):
        cell = sheet[cell_ref]
        old_fill = cell.fill.copy()
        cell.value = new_value
        cell.alignment = Alignment(wrap_text=True)
        cell.fill = old_fill

    # Process DeepL and Microsoft Translator sheets
    for sheet_name in ['DeepL', 'Microsoft Translator']:
        sheet = workbook[sheet_name]
        for row in range(2, sheet.max_row + 1):
            german_text_cell = sheet['A{}'.format(row)]
            german_text = german_text_cell.value
            if german_text:
                languages = deepl_languages if sheet_name == 'DeepL' else microsoft_languages
                for language, info in languages.items():
                    target_cell_ref = '{}{}'.format(info["column"], row)
                    if not sheet[target_cell_ref].value:
                        translate_func = translate_text_deepl if sheet_name == 'DeepL' else translate_text_microsoft
                        translated_text = translate_func(german_text, info["code"], deepl_api_key if sheet_name == 'DeepL' else microsoft_translator_api_key)
                        update_cell(sheet, target_cell_ref, translated_text)

    # Save the translated workbook to a BytesIO object
    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output

def main():
    st.title("Excel File Translator Tool (DeepL and Microsoft Translator)")

    # Explanation text
    st.markdown("""
        This program translates German text in an Excel file to English, French, Dutch, Swedish, Czech, and Slovak using different translators. 
        The Excel file should contain two sheets, one named 'DeepL' and the other named 'Microsoft Translator'. 
        Each sheet must start with the German column and follow this column order: German, English, French, Dutch, Swedish, Czech, Slovak. 
        The German column should be filled with the texts to translate.
        The exact names of the columns are not important, just the order.
    """)

    # File uploader
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])

    if uploaded_file is not None:
        # Run Translation button
        if st.button('Translate Excel File'):
            with st.spinner('Translating...'):
                # Call the translate_excel function
                output_file = translate_excel(uploaded_file)

                # Provide a link to download the output file
                st.success('Translation Completed!')
                st.download_button('Download Translated File', 
                                   data=output_file, 
                                   file_name='translated_excel.xlsx',
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    main()
