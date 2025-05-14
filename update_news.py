# update_news.py

import requests
from bs4 import BeautifulSoup
import re
import os

# --- Configuration ---
KASPERSKY_NEWS_URL = "https://www.kaspersky.com.br/blog/category/news/"
OLHAR_DIGITAL_SECURITY_URL = "https://olhardigital.com.br/tag/seguranca-da-informacao/"
MAX_SUMMARY_LENGTH = 590
MAX_NEWS_ITEMS_PER_SOURCE = 5 # Limit the number of news items to keep the page concise
HTML_TEMPLATE_FILE = "index.html"
HTML_OUTPUT_FILE = "index_updated.html"
NEWS_SECTION_MARKER_START = "<!-- NEWS_CONTENT_START -->"
NEWS_SECTION_MARKER_END = "<!-- NEWS_CONTENT_END -->"

# --- Helper Functions ---

def_make_title_phrase(text, max_len=100):
    """Creates a concise title phrase from text."""
    text = text.strip()
    if len(text) <= max_len:
        return text if text.endswith('.') else text + '.'
    
    # Try to find a sentence end near max_len
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current_title = ""
    for sentence in sentences:
        if len(current_title) + len(sentence) + 1 <= max_len:
            current_title += (sentence if current_title == "" else " " + sentence)
        else:
            break
    if not current_title:
        return text[:max_len-3] + "..."
    return current_title if current_title.endswith('.') else current_title + '.'

def_smart_summary(text, max_length=MAX_SUMMARY_LENGTH):
    """Creates a summary within the max_length, trying to keep full sentences."""
    text = text.strip()
    if len(text) <= max_length:
        return text

    # Try to cut at the last sentence end before max_length
    summary = text[:max_length]
    last_period = summary.rfind('.')
    if last_period > 0:
        summary = summary[:last_period + 1]
    else:
        # If no period, cut at last space
        last_space = summary.rfind(' ')
        if last_space > 0:
            summary = summary[:last_space] + "..."
        else:
            summary = summary[:max_length-3] + "..."
    return summary

# --- Scraping Functions (Simplified Placeholders - Real implementation is complex) ---

def_scrape_kaspersky():
    """Scrapes news from Kaspersky. Returns a list of {'title_raw': ..., 'summary_raw': ..., 'url': ...}"""
    news_list = []
    try:
        print(f"Fetching Kaspersky news from {KASPERSKY_NEWS_URL}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(KASPERSKY_NEWS_URL, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This selector is an example and WILL LIKELY NEED ADJUSTMENT
        # based on current Kaspersky blog structure.
        articles = soup.find_all('article', class_='o-singlePost', limit=MAX_NEWS_ITEMS_PER_SOURCE + 2) # Fetch a bit more to filter
        
        for article in articles:
            if len(news_list) >= MAX_NEWS_ITEMS_PER_SOURCE:
                break
            title_tag = article.find('h3', class_='o-singlePost__title')
            # Kaspersky often has a lead paragraph that can serve as a summary
            summary_tag = article.find('div', class_='o-singlePost__text') 
            link_tag = title_tag.find('a') if title_tag else None

            if title_tag and link_tag and link_tag.has_attr('href'):
                title_raw = title_tag.get_text(strip=True)
                url = link_tag['href']
                summary_raw = ""
                if summary_tag:
                    summary_p = summary_tag.find('p')
                    if summary_p:
                        summary_raw = summary_p.get_text(strip=True)
                
                if not summary_raw and title_raw: # Fallback if specific summary tag not found
                    # Try to get some text from the article body if no explicit summary
                    # This is highly dependent on site structure
                    pass

                if title_raw and url:
                    news_list.append({'title_raw': title_raw, 'summary_raw': summary_raw if summary_raw else "Clique para ler mais.", 'url': url, 'source_name': 'Kaspersky'})
        print(f"Found {len(news_list)} news items from Kaspersky.")
    except Exception as e:
        print(f"Error scraping Kaspersky: {e}")
    return news_list

def_scrape_olhar_digital():
    """Scrapes news from Olhar Digital. Returns a list of {'title_raw': ..., 'summary_raw': ..., 'url': ...}"""
    news_list = []
    try:
        print(f"Fetching Olhar Digital news from {OLHAR_DIGITAL_SECURITY_URL}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(OLHAR_DIGITAL_SECURITY_URL, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This selector is an example and WILL LIKELY NEED ADJUSTMENT
        articles = soup.find_all('li', class_='item', limit=MAX_NEWS_ITEMS_PER_SOURCE + 2)

        for article in articles:
            if len(news_list) >= MAX_NEWS_ITEMS_PER_SOURCE:
                break
            title_tag = article.find('h3', class_='title')
            summary_tag = article.find('span', class_='excerpt')
            link_tag = article.find('a', class_='link')

            if title_tag and summary_tag and link_tag and link_tag.has_attr('href'):
                title_raw = title_tag.get_text(strip=True)
                summary_raw = summary_tag.get_text(strip=True)
                url = link_tag['href']
                if not url.startswith('http'):
                    url = "https://olhardigital.com.br" + url # Ensure full URL
                news_list.append({'title_raw': title_raw, 'summary_raw': summary_raw, 'url': url, 'source_name': 'Olhar Digital'})
        print(f"Found {len(news_list)} news items from Olhar Digital.")
    except Exception as e:
        print(f"Error scraping Olhar Digital: {e}")
    return news_list

# --- HTML Generation ---

def_format_news_html(news_items):
    """Formats a list of news items into HTML string.
       Each item in news_items is a dict: {'title_raw': ..., 'summary_raw': ..., 'url': ..., 'source_name': ...}
    """
    html_output = ""
    if not news_items:
        html_output = "<p>Nenhuma notícia encontrada no momento. Tente novamente mais tarde.</p>"
        return html_output

    for item in news_items:
        title_phrase = _make_title_phrase(item['title_raw'])
        summary_text = _smart_summary(item['summary_raw'])
        
        html_output += "<div class=\"news-item\">\n"
        html_output += f"    <h3>{title_phrase}</h3>\n"
        html_output += f"    <p>{summary_text}</p>\n"
        html_output += f"    <p><a href=\"{item['url']}\" target=\"_blank\">Leia mais [{item['source_name']}]</a></p>\n"
        html_output += "</div>\n\n"
    return html_output

# --- Main Function ---

def_main():
    print("Starting news update process...")
    # Step 1: Scrape news (using placeholder data for now)
    kaspersky_items = _scrape_kaspersky()
    olhar_digital_items = _scrape_olhar_digital()
    
    all_news_items = kaspersky_items + olhar_digital_items
    # Sort by some logic if needed, e.g., date (requires date scraping)
    # For now, just combine them.

    if not all_news_items:
        print("No news items fetched. Exiting.")
        # Create an empty news section or keep the old one
        news_html_content = "<p>Não foi possível carregar as notícias no momento. Por favor, tente novamente mais tarde.</p>"
    else:
        # Step 2: Format news into HTML
        news_html_content = _format_news_html(all_news_items)

    # Step 3: Read HTML template
    try:
        print(f"Reading HTML template from {HTML_TEMPLATE_FILE}...")
        with open(HTML_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{HTML_TEMPLATE_FILE}' not found. Make sure it's in the same directory as the script.")
        return
    except Exception as e:
        print(f"Error reading template file: {e}")
        return

    # Step 4: Replace news section placeholder
    # Ensure the markers are unique and not part of other content.
    start_index = template_content.find(NEWS_SECTION_MARKER_START)
    end_index = template_content.find(NEWS_SECTION_MARKER_END)

    if start_index != -1 and end_index != -1 and start_index < end_index:
        print("Replacing news content in template...")
        # The content to insert includes the start marker, the news, and then the end marker is after.
        # So we replace the content *between* the start marker's end and the end marker's start.
        updated_content = (template_content[:start_index + len(NEWS_SECTION_MARKER_START)] +
                           "\n" + news_html_content + "\n            " +
                           template_content[end_index:])
    else:
        print(f"Error: News section markers ('{NEWS_SECTION_MARKER_START}', '{NEWS_SECTION_MARKER_END}') not found or in wrong order in '{HTML_TEMPLATE_FILE}'.")
        print("Please add these comments around the area where news items should be inserted in your index.html:")
        print(f"{NEWS_SECTION_MARKER_START}")
        print("    ... (old news items or placeholder here) ...")
        print(f"{NEWS_SECTION_MARKER_END}")
        return

    # Step 5: Write updated HTML to output file
    try:
        print(f"Writing updated HTML to {HTML_OUTPUT_FILE}...")
        with open(HTML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated news. Output saved to: {os.path.abspath(HTML_OUTPUT_FILE)}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    _main()

