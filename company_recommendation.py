import pandas as pd
from sentence_transformers import SentenceTransformer, util

def recommend_companies(resume_text, jd_text, dataset_path, top_k=5):
    # Load dataset
    df = pd.read_csv(dataset_path)

    # Initialize sentence transformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Combine resume and JD text for embedding
    combined_input = resume_text + " " + jd_text
    input_embedding = model.encode(combined_input, convert_to_tensor=True)

    # Combine resume and job description from dataset for embeddings
    df['Combined'] = df['Resume_Text'] + " " + df['Job_Description']
    company_embeddings = model.encode(df['Combined'].tolist(), convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.pytorch_cos_sim(input_embedding, company_embeddings)[0]

    # Get top-k results (similarity scores and indices)
    top_results = similarities.topk(k=top_k)

    # Prepare recommended list with correct column name 'Role'
    recommended = []
    for score, idx in zip(top_results.values, top_results.indices):
        idx = int(idx)
        recommended.append({
            'Company_Name': df.iloc[idx]['Company_Name'],
            'Job_Role': df.iloc[idx]['Role'],      # <-- updated here
            'Similarity_Score': float(score) * 100
        })

    return recommended
