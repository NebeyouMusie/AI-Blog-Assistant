from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import load_config, get_groq_api_key

load_config()

def get_llm():
    llm  = ChatGroq(api_key=get_groq_api_key(), model='llama-3.1-70b-versatile', temperature=0.7)
    return llm


def get_prompt_template_for_title_suggestion():
    # define a ChatPromptTempalte for title suggestions
    prompt_template_for_title_suggestion = ChatPromptTemplate.from_template(
        """I'm planning a blog post on topic : {topic}.
        The title is informative, or humorous, or persuasive. 
        The target audience is : {target}  
        Suggest a list of ten creative and attention-grabbing titles for this blog post. 
        Don't give any explanation or overview to each title.
        IMPORTANT: ONLY RETURN THE TOPICS NOTHING MORE.
        """
    )

    # define the title suggestion chain
    title_suggestion_chain = prompt_template_for_title_suggestion | get_llm() | StrOutputParser()

    
    return title_suggestion_chain


def get_prompt_template_for_title():
    # define a ChatPromptTemplate for blog content generation
    prompt_tempalte_for_title = ChatPromptTemplate.from_template(
        """Write a high-quality, informative, and plagiarism-free blog post on the topic: "{title}". 
        Target the content towards a {target} audience. 
        Use a conversational writing style and structure the content with an introduction, body paragraphs, and a conclusion. 
        Try to incorporate these keywords: {keywords}. 
        Aim for a content length of {blog_length} words. 
        Make the content engaging and capture the reader's attention.
        """
    )

    # define the title generation chain
    title_chain = prompt_tempalte_for_title | get_llm() | StrOutputParser()
    
    return title_chain