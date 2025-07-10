import os
import google.generativeai as genai
from django.conf import settings

def get_llm_response(question, context):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a knowledge assistant. Answer the following question based solely on the provided context. Do not add information beyond the context. If the context doesn't contain enough information, say so.

    Context:
    {context}

    Question:
    {question}

    Answer in a concise and accurate manner.
    """
    
    response = model.generate_content(prompt)
    return response.text