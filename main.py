import requests
from bs4 import BeautifulSoup as BS

main_url = input('put your link of category there: ')
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}

def get_soup(url: str) -> BS:
   response = requests.get(url)
   html = response.text
   soup = BS(html, 'lxml')
   return soup

def get_all_products_from_page(soup: BS) -> list:
   products = []
   for product in soup.find_all('div', {'class': 'ut2-gl__body'}):
      product_info = get_product_info(product)
      products.append(product_info)
   return products

def get_product_info(product: BS) -> dict:
   title = product.find('div', {'class': 'ut2-gl__name'}).text.strip()
   desc = product.find('div', {'class': 'ut2-gl__bottom'}).text.strip()
   try:
      image = product.find('div', {'class': 'ut2-gl__image'}).find('img')['src']
   except:
      image = 'None'
   price = product.find('div', {'class': 'ut2-gl__price'}).text.strip()
   return {'title': title, 'description': desc, 'image': image, 'price': price}

def get_last_page(soup: BS):
   pag = soup.find('div', {'class': 'ty-pagination__bottom'})
   last_page = soup.find('a', {'hidden-phone'})
   text = last_page.text
   parts = text.split("-")
   number = parts[-1]
   return int(number)

def get_data_by_category(url:BS) -> dict:
   soup = get_soup(url)
   last_page = get_last_page(soup)
   all_products = []
   for page in range(1, last_page + 1):
      print(f'{main_url}?page={page}')
      soup = get_soup(f'{main_url}?page={page}')
      products = get_all_products_from_page(soup)
      all_products.extend(products)
   return {'products_of_category': all_products}

def write_to_db(data):
   import json
   with open('first.json', 'w', encoding='utf-8') as json_file:
      json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
   data = get_data_by_category(main_url)
   write_to_db(data)

if __name__ == '__main__':
   main()
