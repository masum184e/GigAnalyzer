import requests
from bs4 import BeautifulSoup

def scrape_fiverr_gigs(keyword):
    url = f"https://www.fiverr.com/search/gigs?query={keyword}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        gigs = soup.find_all('div', class_='gig-wrapper')
        
        index=0
        for gig in gigs:
            title = gig.find('p', role='heading').string
            # price = gig.find("a",class_="hxtGeVp").find("span").find("span").string.replace("US$", "")
            # rating = gig.find("span", class_="rating-score").string
            # order = gig.find("span", class_="rating-count-number").string
            url=title.parent.parent.get("href").split('?')[0]
            print(f"{index}. {url}")
            index=index+1
            # seller = gig.find('span', class_='seller-name').text.strip()
            # price = gig.find('span', class_='gig-price').text.strip()
            # rating = gig.find('span', class_='gig-rating').text.strip()
            # print(f"Title: {title}\nSeller: {seller}\nPrice: {price}\nRating: {rating}\n")
    else:
        print("Failed to retrieve data.")

keyword = input("Enter keyword to search Fiverr gigs: ")
scrape_fiverr_gigs(keyword)
