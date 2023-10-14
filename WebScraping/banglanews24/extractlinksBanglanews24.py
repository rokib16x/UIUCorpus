import requests
from bs4 import BeautifulSoup
import time

links = [
    "https://www.banglanews24.com/category/জাতীয়/1",
    "https://www.banglanews24.com/category/রাজনীতি/2",
    "https://www.banglanews24.com/category/আইন ও আদালত/18",
    "https://www.banglanews24.com/category/আন্তর্জাতিক/4",
    "https://www.banglanews24.com/category/%E0%A6%96%E0%A7%87%E0%A6%B2%E0%A6%BE/5",
    "https://www.banglanews24.com/category/%E0%A6%AC%E0%A6%BF%E0%A6%A8%E0%A7%8B%E0%A6%A6%E0%A6%A8/6",
    "https://www.banglanews24.com/category/তথ্যপ্রযুক্তি/7",
    "https://www.banglanews24.com/category/%E0%A6%B6%E0%A6%BF%E0%A6%B2%E0%A7%8D%E0%A6%AA-%E0%A6%B8%E0%A6%BE%E0%A6%B9%E0%A6%BF%E0%A6%A4%E0%A7%8D%E0%A6%AF/11",
    "https://www.banglanews24.com/category/%E0%A6%86%E0%A6%B0%E0%A6%93/1258",
    "https://www.banglanews24.com/district",
    "https://www.banglanews24.com/category/চট্টগ্রাম প্রতিদিন/14",
    "https://www.banglanews24.com/category/%E0%A6%85%E0%A6%B0%E0%A7%8D%E0%A6%A5%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A6%BF-%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%AC%E0%A6%B8%E0%A6%BE/3",
    "https://www.banglanews24.com/category/স্বাস্থ্য/19",
    "https://www.banglanews24.com/category/শিক্ষা/20",
    "https://www.banglanews24.com/category/ইসলাম/15",
    "https://www.banglanews24.com/category/%E0%A6%AD%E0%A6%BE%E0%A6%B0%E0%A6%A4/22",
    "https://www.banglanews24.com/category/ক্যারিয়ার/32",
    "https://www.banglanews24.com/category/রাশিফল/10",
    "https://www.banglanews24.com/category/বাজেট/1213",
    "https://www.banglanews24.com/category/শেয়ারবাজার/1208",
    "https://www.banglanews24.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%8D%E0%A6%AC%E0%A6%95%E0%A6%BE%E0%A6%AA%20%E0%A6%95%E0%A7%8D%E0%A6%B0%E0%A6%BF%E0%A6%95%E0%A7%87%E0%A6%9F",
    "https://www.banglanews24.com/category/%E0%A6%86%E0%A6%B0%E0%A6%93/1258"
]
# Function to scrape a single URL
def scrape_url(base_url):
    page_number = 1

    while True:
        try:
            # Create the URL for the current page
            url = f"{base_url}?page={page_number}"

            # Send an HTTP GET request to the page with a User-Agent header
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            # Check if the request was successful
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find and print the articles on the current page
            articles = soup.find_all("div", class_="col-md-8 list")
            for article in articles:
                link = article.find("a")["href"]
                title = article.find("a").text
                print(f"from base url {base_url} and page number {page_number} ")

                # Write the link to the file
                with open('banglanews24.txt', 'a') as file:
                    file.write(link + '\n')

            # Check if there is a "Next »" link
            next_link = soup.find("a", string="›")
            if not next_link:
                break

            # Increment the page number to navigate to the next page
            page_number += 1

            # Add a delay to be respectful of the server
            time.sleep(2)  # Adjust the delay as needed

        except Exception as e:
            # Print the error message
            print(f"An error occurred for {base_url}, page {page_number}: {str(e)}")
            # You can choose to log the error or take other actions here
            break

# Scraping loop
for base_url in links:
    scrape_url(base_url)

# Print a message when everything is finished
print("Scraping completed.")
