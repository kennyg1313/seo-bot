import requests
from bs4 import BeautifulSoup
import streamlit as st

# Streamlit App for SEO Bot
st.title("SEO Bot for Grewal Fine Homes")
st.write("Optimize your website's SEO effortlessly!")

# Predefined Keywords
predefined_keywords = [
    "Buy Home", "Sell Home", "Leasing", "Relocating", "Waterfront", "NH", "Lakes Region",
    "Meredith", "Laconia", "Wolfeboro", "Moultonborough", "Tilton"
]

# Sidebar Navigation
st.sidebar.header("SEO Analysis Input")
selected_feature = st.sidebar.selectbox("Choose a feature:", ["Keyword Research", "Content Analysis", "Technical SEO Check"])

# Keyword Research Function (Google Autocomplete)
def get_google_suggestions(query):
    url = f"https://www.google.com/complete/search?q={query}&client=chrome"
    response = requests.get(url)
    if response.status_code == 200:
        suggestions = response.json()[1]
        return [{"Keyword": suggestion} for suggestion in suggestions]
    else:
        st.error(f"Error fetching suggestions: {response.status_code}")
        return []

# Content Analysis Function
def analyze_content(url, target_keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    keyword_count = content.lower().count(target_keyword.lower())
    word_count = len(content.split())
    return keyword_count, word_count

# Technical SEO Check (Google PageSpeed Insights)
def check_pagespeed(api_key, url):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
        return performance_score
    else:
        st.error(f"Error: {response.status_code}")
        return None

# Feature Selection Logic
if selected_feature == "Keyword Research":
    st.subheader("Keyword Research")
    query = st.text_input("Enter Search Query", value=" ".join(predefined_keywords))
    if st.button("Fetch Keywords"):
        if query:
            keywords = get_google_suggestions(query)
            if keywords:
                st.write("Keyword Suggestions:")
                st.dataframe(keywords)
        else:
            st.error("Please provide a Search Query.")

elif selected_feature == "Content Analysis":
    st.subheader("Content Analysis")
    url = st.text_input("Enter Page URL")
    target_keyword = st.selectbox("Select Target Keyword", predefined_keywords)
    if st.button("Analyze Content"):
        if url and target_keyword:
            keyword_count, word_count = analyze_content(url, target_keyword)
            st.write(f"Keyword '{target_keyword}' appears {keyword_count} times.")
            st.write(f"Total word count: {word_count}")
        else:
            st.error("Please provide both URL and Target Keyword.")

elif selected_feature == "Technical SEO Check":
    st.subheader("Technical SEO Check")
    api_key = st.text_input("Enter PageSpeed Insights API Key")
    url = st.text_input("Enter Page URL")
    if st.button("Check Performance"):
        if api_key and url:
            score = check_pagespeed(api_key, url)
            if score is not None:
                st.write(f"Performance Score: {score}")
        else:
            st.error("Please provide both API Key and URL.")
