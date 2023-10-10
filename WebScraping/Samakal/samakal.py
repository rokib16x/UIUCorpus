import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Function to generate date strings from a start date to an end date
def date_range(start_date, end_date):
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime("%Y-%m-%d")
        current_date += delta

# Define the start and end date for scraping
start_date = datetime(2016, 1, 1)
end_date = datetime.today()

# Specify the base URL
base_url = "https://www.banglatribune.com/archive/"

# Initialize a list to store article links and names
article_data = []

# Iterate through the date range and scrape articles
for date_str in date_range(start_date, end_date):
    page_number = 1  # Start with page 1
    while True:
        url = f"{base_url}{date_str}?page={page_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("div", class_="each col_in")
            for article in articles:
                article_link = article.find("a", class_="link_overlay")["href"]
                article_name = article.find("span", class_="title").text.strip()
                article_data.append(f"{article_link}\t{article_name}")
                print(f"Article Name: {article_name}\nDate: {date_str}\nPage Number: {page_number}\n")
            # Check if there is a "Next" page available
            next_page = soup.find("a", class_="next_page")
            if next_page:
                page_number += 1
            else:
                break
        else:
            print(f"Failed to fetch data from {url}")
            break

# Save the collected data to a text file
with open("banglatribune.txt", "w", encoding="utf-8") as file:
    for entry in article_data:
        file.write(entry + "\n")

print("Scraping completed and data saved to 'banglatribune.txt'.")
