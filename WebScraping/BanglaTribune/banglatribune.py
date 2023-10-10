import random

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# Define the base URL for the archive
base_url = "https://www.banglatribune.com/archive/"

# Define the start date as January 1, 2016
start_date = datetime(2015, 11, 16)

# Define the end date, for example, December 31, 2023
end_date = datetime(2023, 10, 4)

# Initialize a variable to keep track of the current date
current_date = start_date

# Define a User-Agent header to mimic a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Create or open a file for writing
with open("file.txt", "w", encoding="utf-8") as file:
    while current_date <= end_date:
        # Format the current date as 'yyyy-mm-dd'
        date_str = current_date.strftime("%Y-%m-%d")

        # Initialize a variable to keep track of the current page
        page_number = 1

        while True:
            # Construct the URL for the current page and date
            url = f"{base_url}{date_str}?page={page_number}"

            # Send an HTTP GET request to the current page URL with headers
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, "html.parser")

                # Find the container that holds the articles
                articles_container = soup.find("div", {"class": "contents_listing"})

                # Find all article elements
                articles = articles_container.find_all("div", {"class": "each col_in has_image image_top content_capability_blog content_type_news responsive_image_hide_"})

                # Loop through each article and extract the title and URL
                for article in articles:
                    article_url = article.find("a", {"class": "link_overlay"})["href"]

                    # Write the title, URL, and date to the file
                    file.write(f"{article_url}\n")

                print(f"Page {page_number} for {date_str} done.")

                # Find the "Next" link for pagination
                next_link = soup.find("a", {"class": "next_page"})

                # Check if there's a "Next" link, if not, break the loop for this date
                if not next_link:
                    break

                # Increment the page number to go to the next page
                page_number += 1
            else:
                print(f"Failed to retrieve the page {date_str}. Status code:", response.status_code)
                break

        # Move to the next date
        current_date += timedelta(days=1)

        # Add a delay between requests to mimic human behavior (e.g., 1-3 seconds)
        time.sleep(1 + 2 * random.random())  # Randomize the sleep time slightly

print("Scraping completed and data has been written to file.txt")
