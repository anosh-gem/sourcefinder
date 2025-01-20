import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# Set page configuration
st.set_page_config(page_title="Web Page Analyzer", layout="wide")

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

def extract_links_and_images(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    images = [img['src'] for img in soup.find_all('img', src=True)]
    return links, images

def extract_css_and_js(html):
    soup = BeautifulSoup(html, 'html.parser')
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    js_links = [script['src'] for script in soup.find_all('script', src=True)]
    return css_links, js_links

def main():
    st.title("Web Page Analyzer")
    url = st.text_input("Enter URL", "https://example.com")

    if st.button("Fetch"):
        html_content = fetch_url_content(url)
        if html_content:
            st.subheader("HTML Code")
            st.code(html_content, language='html')

            css_links, js_links = extract_css_and_js(html_content)
            st.subheader("CSS Links")
            st.write(css_links)

            st.subheader("JavaScript Links")
            st.write(js_links)

            links, images = extract_links_and_images(html_content)
            st.subheader("All Links")
            st.write(links)

            st.subheader("Image Sources")
            st.write(images)

            st.subheader("Image Directory Names")
            image_dirs = [os.path.dirname(img) for img in images if img.startswith('http')]
            st.write(set(image_dirs))

if __name__ == "__main__":
    main()

