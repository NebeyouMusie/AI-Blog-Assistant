import re
import streamlit as st
from utils import get_llm, get_prompt_template_for_title_suggestion, get_prompt_template_for_title

title_suggestion_chain = get_prompt_template_for_title_suggestion()
title_chain = get_prompt_template_for_title()


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
    title_suggestion_str = title_suggestion_chain.invoke({'topic': topic_name, 'target': target_audience})
    st.text(title_suggestion_str)
    
st.subheader('Blog Generation') # Display a subheader for the blog generation section
title_expander = st.expander("Input the title") # Create an expander for title input

with title_expander:
    title_of_the_blog = st.text_input("Title", key="title_of_the_blog")
    num_of_words = st.number_input("Number of words", min_value=100, max_value=1000, step=50)
    if 'keywords' not in st.session_state:
        st.session_state.keywords = []
    keyword_input = st.text_input("Enter a keyword: ")
    keyword_button = st.button("Add keyword")
    if keyword_button:
        st.session_state.keywords.append(keyword_input)
        st.session_state.keyword_input = ""
        for keyword in st.session_state.keywords:
            st.write(f"<div style='display: inline-block; background-color: green; color: white; padding: 10px; margin: 5px; border: none; border-radius: 10px;'>{keyword}</div>", unsafe_allow_html=True)
            
    submit_title = st.button("Submit Info")
    
if submit_title:
    formatted_keywords = []
    for i in st.session_state.keywords:
        if len(i) > 0:
            formatted_keywords.append(i.lstrip('0123456789 : ').strip('"').strip("'"))
    formatted_keywords = ', '.join(formatted_keywords)
    st.subheader(title_of_the_blog)
    generated_blog_content = title_chain.invoke({'title': title_of_the_blog, 'target': target_audience, 'keywords': formatted_keywords, 'blog_length': num_of_words})
    st.write(generated_blog_content)