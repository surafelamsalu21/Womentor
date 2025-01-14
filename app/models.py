import os
import PyPDF2
import docx
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure your API key is set in the environment

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
def process_resume(file_path):
    """Process the uploaded resume and extract its text content."""
    try:
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX files are allowed.")
        
        if not text.strip():
            logging.error("Extracted text is empty.")
            raise ValueError("The uploaded file does not contain readable text.")
        
        logging.debug(f"Extracted Text: {text}")
        return text
    except Exception as e:
        logging.error(f"Error processing resume: {e}")
        raise

import logging
logging.basicConfig(level=logging.DEBUG)

import json
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_resume_with_openai(resume_text):
    """Evaluate a resume using OpenAI API."""
    prompt = f"""
    You are an AI assistant helping to evaluate resumes based on predefined criteria. Given the following resume text:

    "{resume_text}"

    Please analyze the resume and determine:
    1. Is the candidate female? Answer "Yes" or "No" and explain how you determined it.
    2. Is the candidate a beneficiary of a scholar program? Provide evidence if possible.
    3. Has the candidate demonstrated leadership experience? Mention relevant roles or achievements.
    4. Is the candidate a graduate of an African business school? Provide evidence if possible.
    5. Does the candidate have at least 1 year of investment experience? Explain your reasoning.
    6. Is the candidate an aspiring investment professional? Explain your reasoning.
    7. Is the candidate fluent in English (and proficient in French)? Provide evidence.

    Return the results in the following JSON format:
    {{
        "gender": "Yes/No",
        "gender_reasoning": "...",
        "scholar_beneficiary": "Yes/No",
        "scholar_reasoning": "...",
        "leadership": "Yes/No",
        "leadership_reasoning": "...",
        "african_business_school": "Yes/No",
        "business_school_reasoning": "...",
        "investment_experience": "Yes/No",
        "investment_reasoning": "...",
        "aspiring_professional": "Yes/No",
        "professional_reasoning": "...",
        "language_proficiency": "Yes/No",
        "language_reasoning": "..."
    }}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and clean the response content
        raw_content = response.choices[0].message.content
        cleaned_content = re.sub(r"```json|```", "", raw_content).strip()  # Remove code block markers
        return cleaned_content
    except Exception as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")
