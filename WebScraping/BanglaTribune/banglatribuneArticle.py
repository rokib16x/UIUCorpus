import requests
from bs4 import BeautifulSoup
import time
link_list = []

# Open the 'samakal.txt' file for reading
with open('samakal.txt', 'r', encoding='utf-8') as file:
    # Read each line from the file
    for line in file:
        # Remove leading and trailing whitespaces, if any
        line = line.strip()
        # Append the line (link) to the list
        link_list.append(line)


# Create or open the output text file in write mode
with open('samakalBigData.txt', 'w', encoding='utf-8') as output_file:
    # Iterate through the list of article links
    for link in link_list:
        try:
            # Send an HTTP GET request to the article link
            response = requests.get(link)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the HTML content of the article page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title/header and paragraphs
            title = soup.find('h1', class_='fontSize32').text.strip()
            paragraphs = soup.find_all('div', class_='description')[0].find_all('p')

            # Write the title and paragraphs to the output file
            output_file.write(title + '\n')
            for paragraph in paragraphs:
                output_file.write(paragraph.text.strip() + '\n')

            # Print a message to indicate successful scraping
            print(f'Successfully scraped: {title}')

            # Add a delay of a few seconds to be polite to the server
            time.sleep(3)  # Adjust the delay as needed

        except Exception as e:
            # Handle exceptions (e.g., network errors, missing elements)
            print(f'Error scraping {link}: {str(e)}')

# Print a message to indicate the scraping process is complete
print('Scraping completed. Data saved to samakalBigData.txt.')
