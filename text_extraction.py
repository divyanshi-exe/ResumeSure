import docx2txt
import PyPDF2
import re

def extract_text(file_path):
    text = ''
    if file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.lower().endswith('.docx'):
        text = docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")
    
    return preprocess_text(text)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)            # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)         # Remove punctuation
    return text.strip()

# Run this script directly for testing
if __name__ == "__main__":
    #  CHANGE THESE to your actual file paths
    resume_file = "resume.pdf"
    jd_file = "job_description.pdf"

    print("\n--- Extracted Resume Text ---")
    print(extract_text(resume_file))

    print("\n--- Extracted Job Description Text ---")
    print(extract_text(jd_file))
