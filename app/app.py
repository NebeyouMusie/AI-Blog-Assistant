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
    if 'topic_name' not in st.session_state:
        st.session_state.topic_name = ""
    st.session_state.topic_name = st.text_input("Topic")
    if 'target_audience' not in st.session_state:
        st.session_state.target_audience = ""
    st.session_state.target_audience = st.text_input("Target Audience")
    submit_btn = st.button("Submit")

if submit_btn: # Handle button click (submit_topic)
    title_suggestion_str = title_suggestion_chain.invoke({'topic': st.session_state.topic_name, 'target': st.session_state.target_audience})
    st.text(title_suggestion_str)
    
st.subheader('Blog Generation') # Display a subheader for the blog generation section
title_expander = st.expander("Input Blog Details") # Create an expander for title input

with title_expander:
    if 'title_of_the_blog' not in st.session_state:
        st.session_state.title_of_the_blog = ""
    st.session_state.title_of_the_blog = st.text_input("Title")
    if 'num_of_words' not in st.session_state:
        st.session_state.num_of_words = ""
    st.session_state.num_of_words = st.slider('Number of Words', min_value=100, max_value=1000, step=50)
    if 'keywords' not in st.session_state:
        st.session_state.keywords = []
    if 'keyword_input' not in st.session_state:
        st.session_state.keyword_input = ""
    st.session_state.keyword_input = st.text_input("Enter a keyword: ")
    keyword_button = st.button("Add keyword")
    if keyword_button:
        st.session_state.keywords.append(st.session_state.keyword_input)
        st.session_state.keyword_input = ""
        for keyword in st.session_state.keywords:
            st.write(f"<div style='display: inline-block; background-color: green; color: white; padding: 10px; margin: 5px; border: none; border-radius: 10px;'>{keyword}</div>", unsafe_allow_html=True)
            
    submit_title = st.button("Submit the Info")
    
if submit_title:
    formatted_keywords = []
    for i in st.session_state.keywords:
        if len(i) > 0:
            formatted_keywords.append(i.lstrip('0123456789 : ').strip('"').strip("'"))
    formatted_keywords = ', '.join(formatted_keywords)
    st.subheader(st.session_state.title_of_the_blog)
    with st.spinner("Generating your blog..."):
        generated_blog_content = title_chain.invoke({'title': st.session_state.title_of_the_blog, 'target': st.session_state.target_audience, 'keywords': formatted_keywords, 'blog_length': st.session_state.num_of_words})
        st.write(generated_blog_content)