import streamlit as st
import docx
import tempfile
import os
from PyPDF2 import PdfReader
import requests

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def call_llm_api(prompt, api_key=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=data, headers=headers)
    try:
        resp_json = response.json()
        if "choices" in resp_json and resp_json["choices"]:
            return resp_json["choices"][0]["message"]["content"]
        else:
            st.error(f"LLM API error: {resp_json.get('error', 'Unknown error')}")
            return ""
    except Exception as e:
        st.error(f"Failed to parse LLM API response: {e}")
        return ""

def fill_docx_template(template_path, key_values):
    doc = docx.Document(template_path)
    for p in doc.paragraphs:
        for key, value in key_values.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
    return doc

st.title("Insurance Template Filler")

template_file = st.file_uploader("Upload insurance template (.docx)", type="docx")
pdf_files = st.file_uploader("Upload photo reports (.pdf)", type="pdf", accept_multiple_files=True)
api_key = st.text_input("OpenRouter API Key (optional)", type="password")
output_filename = st.text_input("Output file name", value="Completed GLR Word Doc.docx")

if template_file and pdf_files and output_filename:
    all_text = ""
    for pdf in pdf_files:
        all_text += extract_text_from_pdf(pdf)

    prompt = f"Extract key-value pairs for insurance template filling from this report:\n{all_text}"
    llm_response = call_llm_api(prompt, api_key)
    key_values = {}
    for line in llm_response.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            key_values[k.strip()] = v.strip()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(template_file.read())
        tmp_path = tmp.name

    filled_doc = fill_docx_template(tmp_path, key_values)
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    filled_doc.save(output_path)

    with open(output_path, "rb") as f:
        st.download_button("Download filled template", f, file_name=output_filename)

    st.success(f"Template filled and saved to {output_path}!")
