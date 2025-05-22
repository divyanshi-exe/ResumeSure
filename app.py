from flask import Flask, render_template, request, jsonify
from ats_with_skills import ats_analysis, extract_text_from_pdf
from company_recommendation import recommend_companies
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.files:
        return jsonify({'error': 'Please upload both resume and job description'}), 400
    
    resume = request.files['resume']
    job_description = request.files['job_description']
    
    # Save files temporarily
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resume.pdf')
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_description.pdf')
    
    resume.save(resume_path)
    job_description.save(jd_path)
    
    try:
        # Calculate ATS score
        ats_score = ats_analysis(resume_path, jd_path)
        
        # Extract text
        resume_text = extract_text_from_pdf(resume_path)
        jd_text = extract_text_from_pdf(jd_path)
        
        # Get company recommendations
        dataset_path = "expanded_tech_resume_job_dataset.csv"
        recommended_companies = recommend_companies(resume_text, jd_text, dataset_path)
        
        # Clean up temporary files
        os.remove(resume_path)
        os.remove(jd_path)
        
        return jsonify({
            'ats_score': round(ats_score, 2),
            'recommended_companies': recommended_companies
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)