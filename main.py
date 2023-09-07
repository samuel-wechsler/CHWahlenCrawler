# import required libraries
from queries import *
import sys
import hashlib
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# main function -> loops through all websites, calls is_changed function


def main():
    """
    Checks if any html has been changed.
    """
    mode = sys.argv[1]

    if mode == 'add':

        add_website(sys.argv[2])

    elif mode == 'check':
        # queries all current urls
        urls = get_all_urls()

        for url in urls:
            if is_changed(url):
                print(f"The website has been changed!\n{url}\n\n")
            else:
                print(f"No changes have been made.\n\n")


def extract_html(url):
    """
    Extracts text, links, headings and paragraphs from a given URL.
    """
    # Send a GET request to the URL and fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text content
    text_content = soup.get_text()

    # Extract links
    links = [link.get('href') for link in soup.find_all('a')]

    # Extract other content-related information (you can customize this based on your needs)
    # For example, extracting headings, paragraphs, images, etc.
    headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3',
                                                           'h4', 'h5', 'h6'])]
    paragraphs = [p.text for p in soup.find_all('p')]

    extracted_data = {
        'text': text_content,
        'links': links,
        'headings': headings,
        'paragraphs': paragraphs
    }

    return hashlib.sha256(str(extracted_data).encode()).hexdigest()


def is_changed(url):
    current_html = extract_html(url)
    previous_html = get_previous_html(url)

    # in case there hasn't been an html recorded
    if previous_html is None:
        insert_html(url, current_html)
        return False

    if previous_html != current_html:
        # update html
        insert_html(url, current_html)
        return True

    return False


def add_website(url):
    """
    Function checks if html for url can be read, if so, it adds the url to the database.
    """
    try:
        html = extract_html(url)
    except Exception as e:
        print("Error reading html: ")
        print(e)
        return

    conn = connect_db()

    # insert url into database
    conn.execute(text("INSERT INTO websites (url) VALUES (:url)"),
                 {"url": url})

def add_websites(file):
    links = open(file, 'r').readlines()

    
    for link in links:
        link = link.replace("\n", "")

        try:
            add_website(link)
        except:
            delete_all()
            print("Aborted.")
            return


if __name__ == "__main__":
    main()
