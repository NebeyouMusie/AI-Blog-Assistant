import re
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import get_llm

llm = get_llm()

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
title_suggestion_chain = prompt_template_for_title_suggestion | llm | StrOutputParser()


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
title_chain = prompt_tempalte_for_title | llm | StrOutputParser()

# The UI(User Interface)
st.set_page_config(page_title='AI Blog Assistant', page_icon='📰')
st.title("AI Blog Content Assistant 📰")

st.subheader("Title Generation")
topic_expander = st.expander("Input the topic and target audience")

with topic_expander:
    topic_name = st.text_input("Topic", key="topic_name")
    target_audience = st.text_input("Target Audience", key="target_audience")
    submit_btn = st.button("Submit")

if submit_btn: # Handle button click (submit_topic)
    title_selection_text = '' # Initialize an empty string to store title suggestions
    title_suggestion_str = title_suggestion_chain.invoke({'topic': topic_name, 'target': target_audience})
    st.text(title_suggestion_str)
    
st.subheader('Blog Generation') # Display a subheader for the blog generation section
title_expander = st.expander("Input the title") # Create an expander for title input

with title_expander:
    title_of_the_blog = st.text_input("", key="title_of_the_blog")
    num_of_words = st.slider("Number of words", min_value=100, max_value=1000, step=50)
    
    if 'keywords' not in st.session_state:
        st.session_state.keywords = []
    keyword_input = st.text_input("Enter a keyword: ")
    keyword_button = st.button("Add keyword")
    if keyword_button:
        st.session_state.keywords.append(keyword_input)
        st.session_state.keyword_input = ""
        for keyword in st.session_state.keywords:
            st.write(f"<div style='display: inline-block; background-color: lightgray; padding: 5px; margin: 5px;'>{keyword}</div>", unsafe_allow_html=True)