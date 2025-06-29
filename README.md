# Task 3 – GLR Pipeline with Streamlit

## Objective
Automate insurance template filling using photo reports and LLMs via a simple Streamlit interface.

## Features
- Upload an insurance template in `.docx` format
- Upload multiple photo reports in `.pdf` format
- Extracts text from photo reports
- Uses OpenRouter LLM API to extract key-value pairs
- Populates the template with extracted data
- Download the filled-in `.docx` document

## Setup

1. Clone the repository:
    ```
    git clone <your-repo-url>
    cd task_3_glr_pipeline
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```
    streamlit run task_3_code.py
    ```

4. Outputs will be saved in the `task_3_output/` directory.

## Notes
- You need an OpenRouter API key for LLM functionality.
- Demo video (`task_3.mp4`) should show end-to-end working as per assignment.

## Directory Structure
task_3_glr_pipeline/
├── task_3_code.py 
├── requirements.txt 
├── README.md 
└── task_3_output/
