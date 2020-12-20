import requests
from bs4 import BeautifulSoup
import time

headers = {
    'content-type': 'text/html;charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}


def geturl(url):
    resp = requests.get(url, headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup


def getdata(soup, datalist):
    products = soup.findAll('div', {'data-component-type': 's-search-result'})
    for item in products:
        # Selecting the non sponsored items
        #if not item.find('div', {'class': 'a-row a-spacing-micro'}):
        # Get the product title
        try:
            title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        except:
            title = item.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text.strip()
        # Get the product image link
        item_image = item.find('img', {'class': 's-image'}).get('src')
        # Get the product link
        link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        fulllink = 'www.amazon.ca' + link  # Full link
        try:
            product_price = item.find('span', {'class': 'a-price-symbol'}).text + ' ' + item.find('span', {
                    'class': 'a-price-whole'}).text.replace(',', '') + item.find('span', {
                    'class': 'a-price-fraction'}).text.strip()
        except:
            product_price = 'N/A'

        saleitem = {
            'Title': title,
            'Product Link': fulllink,
            'Image Link': item_image,
            'Price': product_price
        }
        datalist.append(saleitem)
    return datalist


def amazonpagination(soup):
    pages = soup.find('ul', {'class': 'a-pagination'})
    try:
        if not pages.find('li', {'class': 'a-disabled a-last'}):
            url = 'https://www.amazon.ca' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
            return url
        else:
            return
    except:
        error_message = "No Results Found! Check the Search Term or Product Category"
        return error_message
