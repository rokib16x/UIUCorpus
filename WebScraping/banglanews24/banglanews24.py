import requests
from bs4 import BeautifulSoup
import time  # Import the time module

# Function to scrape content from a URL with a delay
def scrape_content_with_delay(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        # Send a GET request to the URL with user agent headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title from the specified location
        title = soup.select_one(".col-md-8.left-container.details h1").text.strip()

        # Extract and clean the content
        content = ' '.join([p.text.strip() for p in soup.find_all('p')])
        content = content.replace('\n', '')  # Remove newline characters

        # Return the title and content
        return title, content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {url}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for {url}: {req_err}")
    except Exception as err:
        print(f"An error occurred for {url}: {err}")

    return None, None

# Read the list of URLs from 'banglanews24.txt'
with open('banglanews24.txt', 'r', encoding='utf-8') as url_file:
    urls = url_file.read().splitlines()

# Initialize a counter for the number of lines scraped and the number of articles scraped
line = 1
articles_scraped = 0

# Open 'banglanews24bigdata.txt' in append mode
with open("banglanews24bigdata.txt", "a", encoding="utf-8") as output_file:
    for url in urls:
        # Scrape content from the URL with a delay of 5 seconds
        title, content = scrape_content_with_delay(url)
        if title or content:
            # Append the title and content to 'banglanews24bigdata.txt'
            output_file.write(f"{title}\n")
            output_file.write(f"{content}\n")
            print(f"Scraped line number: {line}")
            articles_scraped += 1

        line += 1

        # Check if 10 articles have been scraped, and if so, pause for 5 seconds
        if articles_scraped % 10 == 0:
            print("Pausing for 5 seconds...")
            time.sleep(3)  # Add a 5-second pause

print("All content has been saved to 'banglanews24bigdata.txt'.")
