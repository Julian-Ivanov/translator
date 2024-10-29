import streamlit as st
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import requests
from io import BytesIO

# DeepL API key
deepl_api_key = '25f727f2-4270-6944-171f-da78e41dcef0:fx'

# Function to create a glossary and get its ID
def create_glossary(api_key, name, source_lang, target_lang, entries):
    url = "https://api-free.deepl.com/v2/glossaries"
    headers = {'Authorization': f'DeepL-Auth-Key {api_key}'}
    data = {
        'name': name,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'entries': entries  # TSV format string
    }
    response = requests.post(url, headers=headers, data=data)
    
    # Debug: Print the response
    print("Glossary creation response:", response.json())
    
    glossary_id = response.json().get('glossary_id')
    
    # Debug: Log the glossary ID
    print("Glossary ID:", glossary_id)
    
    return glossary_id

# Example glossary entries in TSV format
glossary_entries = "Welt\tChupapi\nBeispiel\tMunjanju"

# Create a glossary and get its ID
glossary_id = create_glossary(deepl_api_key, "MyGlossary", "DE", "EN", glossary_entries)

# Check if the glossary ID is valid
if glossary_id:
    print("Glossary created successfully with ID:", glossary_id)
else:
    print("Failed to create glossary.")
