import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Developed by Anosh Gem
st.set_page_config(page_title="Web Page Analyzer", layout="wide")

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

def extract_links_and_images(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    images = [urljoin(base_url, img['src']) for img in soup.find_all('img', src=True) if img['src']]
    return links, images

def extract_css_and_js(html):
    soup = BeautifulSoup(html, 'html.parser')
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    js_links = [script['src'] for script in soup.find_all('script', src=True)]
    return css_links, js_links

def main():
    st.title("Web Page Analyzer")
    
    # Developed by Anosh Gem
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <h3>Developed by Anosh Gem</h3>
        <h4>For Project: MINU</h4>
    </div>
    """, unsafe_allow_html=True)
    
    url = st.text_input("Enter URL", "https://example.com")
    
    # Ensure the URL starts with http or https
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    if st.button("Fetch"):
        with st.spinner('Fetching data...'):
            html_content = fetch_url_content(url)
            if html_content:
                st.subheader("HTML Code")
                truncated_html = html_content[:2000]  # Truncate to 2000 characters
                st.code(truncated_html, language='html')

                css_links, js_links = extract_css_and_js(html_content)
                st.subheader("CSS Links")
                st.write(css_links)

                st.subheader("JavaScript Links")
                st.write(js_links)

                links, images = extract_links_and_images(html_content, url)
                st.subheader("All Links")
                st.write(links)

                st.subheader("Image Sources")
                st.write(images)

                st.subheader("Image Directory Names")
                image_dirs = [os.path.dirname(img) for img in images if img.startswith('http')]
                st.write(set(image_dirs))

if __name__ == "__main__":
    main()
