

import requests
from bs4 import BeautifulSoup
from dateparser import parse
import cloudscraper
scraper = cloudscraper.create_scraper()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

data=[]


def la_hora(url):
    url ='https://www.lahora.com.ec'+url
    response = scraper.get(url)
    response.raise_for_status()  # Raise an error if the request was unsuccessful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else 'No title found'

    # Extract the subtitle (if available)
    subtitle_tag = soup.find('strong')
    subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else 'No subtitle found'

    # Extract the publication date
    date_tag = soup.find('div',class_='entry-meta').find('span')
    date = parse(date_tag.get_text(strip=True) if date_tag else 'No date found',languages=['es'])

    # Extract tags
    tags = []
    tag_section = soup.find('span', class_='tags-links')  # Replace with the actual class name if different
    if tag_section:
        tag_links = tag_section.find_all('a')
        tags = [tag.get_text(strip=True) for tag in tag_links]

    # Extract category
    category = 'No category found'
    breadcrumb = soup.find('div', class_='breadcrumb')  # Replace with the actual class name if different
    if breadcrumb:
        category_links = breadcrumb.find_all('a')
        if category_links:
            category = category_links[-1].get_text(strip=True)
    return {'tags':tags,'label':category,'title':title,'subtitle':subtitle,'date':date,'body':soup.find('div',class_='entry-content').get_text()}



def get_articles_links(parroquia,i):
    url = f"https://www.lahora.com.ec/{parroquia}"
    response = scraper.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    urls=[]
    # Find the posts section
 
    for posts_section in soup.find_all("section", class_="styles_content__Pdsau")[0].find_all("a", class_="styles_linkStyled__pYJA9"): # all links
    
        article = posts_section
        if article:
            urls.append(article["href"])
    for url in set(urls):
        try:
            data.append(la_hora(url))
        except:
            pass
    return urls

for parroquia in ['esmeraldas','losrios']:
    for i in range(1,2):
        try:
            c = get_articles_links(parroquia,i)
            if not c:
                break
        except Exception as e: 
            print(e)
