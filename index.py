import requests
from bs4 import BeautifulSoup

def scrape_gig_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(f"https://www.fiverr.com{url}", headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        gig_overview = soup.find('div', class_='gig-overview')
        title = gig_overview.find("h1").string
        number_of_order = soup.find('span', class_='rating-count-number').string
        price = soup.find('span', class_='price').string.replace("US$", "")

        tag_list = []
        tags_container = soup.find("div", class_='gig-tags-container')
        if tags_container:
            tags = tags_container.find("ul").find_all("li")
            for tag in tags:
                tag_text = tag.find("a").text
                tag_list.append(tag_text)

        # with open('output.txt', 'a') as file:
        #     file.write(f"{','.join(tag_list)},")

        output = "{:<50} {:<10} {:<10} {}".format(title[:50], number_of_order[:10], price[:10], ', '.join(tag_list))
        print(output)
    else:
        print("Failed to retrieve Details.")

def scrape_fiverr_gigs(keyword):
    url = f"https://www.fiverr.com/search/gigs?query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        gigs = soup.find_all('div', class_='gig-wrapper')
        
        print("                         Title                    | Order   | Price     | Tags")
        for gig in gigs:
            title = gig.find('p', role='heading').string
            url = title.parent.parent.get("href").split('?')[0]
            scrape_gig_details(url)
    else:
        print("Failed to retrieve List")

keyword = input("Enter keyword to search Fiverr gigs: ")
scrape_fiverr_gigs(keyword)
