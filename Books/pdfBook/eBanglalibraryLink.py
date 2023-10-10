import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Function to extract lesson link from a given URL and store it in a file
async def extract_and_store_lesson_link(session, url, lesson_file, direct_file):
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()

            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the <a> tag with class "ld-item-name ld-primary-color-hover"
            lesson_link = soup.find('a', class_='ld-item-name ld-primary-color-hover', href=True)

            # Check if the lesson link element is found
            if lesson_link:
                lesson_url = lesson_link['href']
                lesson_file.write(lesson_url + '\n')  # Store the lesson link immediately in the file
            else:
                print(f"Lesson link not found for URL: {url}")
                direct_file.write(url + '\n')  # Store the URL in 'directbook.txt'

        else:
            print(f"Failed to retrieve URL: {url}. Status code: {response.status}")
            direct_file.write(url + '\n')  # Store the URL in 'directbook.txt'

# Read links from the 'elibrary.txt' file
with open('elibrary.txt', 'r') as input_file, open('lesson_links.txt', 'w') as lesson_output_file, open('directbook.txt', 'w') as direct_output_file:
    links = input_file.read().splitlines()

    # Initialize an asyncio event loop
    loop = asyncio.get_event_loop()

    async def scrape_links():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for index, link in enumerate(links, start=1):
                task = extract_and_store_lesson_link(session, link, lesson_output_file, direct_output_file)
                tasks.append(task)
                print(f"Scraping link {index}/{len(links)}")
            await asyncio.gather(*tasks)

    # Run the asyncio event loop
    loop.run_until_complete(scrape_links())

print(f"Finished scraping lesson links from 'elibrary.txt' and saved them to 'lesson_links.txt'.")
