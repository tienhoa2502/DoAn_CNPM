from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import json
import time

keyWord = 'NITRO'

# Khởi tạo trình duyệt
driver = webdriver.Chrome('C:\Windows\System32\chromedriver.exe')
quotes=[]  # a list to store quotes


# Truy cập trang web cần thao tác
driver.get("https://cellphones.com.vn/catalogsearch/result?q=" + keyWord)
time.sleep(3)

while True: 
    try:
        btnShowMore = driver.find_element(By.CLASS_NAME, "load-more-btn")
        btnShowMore.click()
        time.sleep(3)
    except NoSuchElementException:
        break

html = driver.page_source
# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')

tableCell = soup.find('div', attrs = {'class':'product-list-filter is-flex is-flex-wrap-wrap'})
if tableCell:
    for row in tableCell.findAll('a',attrs = {'class', 'product__link'}):
        quote = {}
        quote['ProductLink'] = row['href']
        quote['ProductName'] = row.h3.text
        
        if row.find('p',attrs = {'class','product__price--show'}):
            quote['ProductPrice'] = row.find('p',attrs = {'class','product__price--show'}).text.strip().replace('\u00a0','').replace('\u20ab','').replace('.','')
        else:
            quote['ProductPrice'] = ''
            
        if row.find('p',attrs = {'class','product__price--through'}):
            quote['ProductPriceCurrent'] = row.find('p',attrs = {'class','product__price--through'}).text.strip().replace('\u00a0','').replace('\u20ab','').replace('.','')
        else:
            quote['ProductPriceCurrent'] = ''
            
        status_element = row.find('p', attrs={'class': 'product__more-info__item notification is-danger is-light'})
        if status_element:
            quote['status'] = status_element.text.strip()
        else:
            quote['status'] = 'Còn hàng'
        quote['ProductImg'] = row.find('img',attrs = {'class','product__img'})['src']
        quote['URL'] = 'cellphones'
        quotes.append(quote)

# Truy cập trang web cần thao tác
driver.get("https://www.thegioididong.com/tim-kiem?key=" + keyWord)
time.sleep(3)

while True: 
    try:
        btnShowMore = driver.find_element(By.XPATH, '//a[contains(@href, "javascript:") and contains(text(), "Còn")]')
        btnShowMore.click()
        time.sleep(3)
    except Exception:
        break

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
tableTheGioiDiDong = soup.find('ul', attrs = {'class':'listsearch item2020 listproduct'})
if tableTheGioiDiDong:
    for row in tableTheGioiDiDong.findAll('a',attrs = {'class', 'main-contain'}):
        quote = {}
        quote['ProductLink'] = 'https://www.thegioididong.com/' + row['href']
        quote['ProductName'] = row['data-name']
        quote['ProductPrice'] = row['data-price']
        if row.find('p',attrs = {'class','price-old black'}):
            quote['ProductPriceCurrent'] = row.find('p',attrs = {'class','price-old black'}).text.replace('\u20ab','').replace('.','')
        else:
            quote['ProductPriceCurrent'] = ''
            
        status_element = row.find('p', attrs={'class': 'item-txt-online'})
        if status_element:
            quote['status'] = status_element.text.strip()
        else:
            quote['status'] = 'Còn hàng'
        quote['ProductImg'] = row.find('img')['src']
        quote['URL'] = 'thegioididong'
        quotes.append(quote)

# Truy cập trang web cần thao tác
driver.get("https://gearvn.com/search?type=product&q=" + keyWord)
time.sleep(3)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
while True:
    try:   
        tableGearVN = soup.find('div', attrs = {'class':'results content-page content-product-list product-list'})
        if tableGearVN:
            for row in tableGearVN.findAll('div', attrs = {'class','product-row'}):
                quote = {}
                quote['ProductLink'] = 'https://gearvn.com/' + row.a['href']
                quote['ProductName'] = row.h2.text
                quote['ProductPrice'] = row.find('span',attrs = {'class','product-row-sale'}).text.strip().replace('\u20ab','').replace(',','')
                if row.find('del'): 
                    quote['ProductPriceCurrent'] = row.find('del').text.replace('\u20ab','').strip().replace(',','')
                else:
                    quote['ProductPriceCurrent'] = ''
                quote['status'] = 'Còn hàng'
                quote['ProductImg'] = row.find('img')['src']
                quote['URL'] = 'gearvn'
                quotes.append(quote)
        ul = driver.find_element(By.CLASS_NAME,'pagination-list')
        
        a = ul.find_elements(By.TAG_NAME, 'a')[-1]
        page = a.get_attribute('title')
        try:
            page_number = int(page)
            break
        except ValueError:
            a.click()
            time.sleep(3)
            html = driver.page_source

            # Sử dụng BeautifulSoup để parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            pass
    except Exception:
        break

# Truy cập trang web cần thao tác
driver.get("https://xgear.net/?s=" + keyWord)
time.sleep(3)

html = driver.page_source

# Sử dụng BeautifulSoup để parse HTML
soup = BeautifulSoup(html, 'html.parser')
while True:
    try: 
        tableXgear = soup.find('ul', attrs = {'class':'products elementor-grid columns-4'})
        if tableXgear:
            for row in tableXgear.findAll('a',attrs = {'class', 'woocommerce-LoopProduct-link woocommerce-loop-product__link'}):
                quote = {}
                quote['ProductLink'] = row['href']
                quote['ProductName'] = row.h2.text.replace('\u2026','')
                quote['ProductPrice'] = row.find('ins').text.replace('\u00a0','').replace('\u20ab','').replace(',','')
                quote['ProductPriceCurrent'] = row.find('del').text.replace('\u00a0','').replace('\u20ab','').replace(',','')
                quote['status'] = 'Còn hàng'
                quote['ProductImg'] = row.find('img')['src']
                quote['URL'] = 'xgear'
                quotes.append(quote)
        ul = driver.find_element(By.CLASS_NAME,'page-numbers')
        
        a = ul.find_element(By.CLASS_NAME, 'next')
        
        a.click()
        time.sleep(3)
        html = driver.page_source

        # Sử dụng BeautifulSoup để parse HTML
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        break
driver.close()

filename ='Data.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(quotes , f, ensure_ascii=False)

print('success!')