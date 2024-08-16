from langchain_groq import ChatGroq
from config import load_config, get_groq_api_key

load_config()

def get_llm():
    llm  = ChatGroq(api_key=get_groq_api_key(), model='llama-3.1-70b-versatile', temperature=0.7)
    return llm