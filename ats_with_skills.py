from sentence_transformers import SentenceTransformer, util
import PyPDF2
import re

skills_list = [  
    'python', 'java', 'c++', 'machine learning', 'deep learning', 'data analysis', 'sql', 'flask', 'django'
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

def calculate_ats_score(resume_text, jd_text):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    # using cosine similarity to calculate ats score
    similarity = util.pytorch_cos_sim(resume_embedding, jd_embedding)
    return float(similarity[0][0]) * 100

def ats_analysis(resume_path, jd_path):
    resume_text = extract_text_from_pdf(resume_path)
    jd_text = extract_text_from_pdf(jd_path)

    ats_score = calculate_ats_score(resume_text, jd_text)

    # Removed skills extraction and matching

    return ats_score
