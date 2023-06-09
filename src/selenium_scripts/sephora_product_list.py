from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.utils.scroll_down import scroll_down
import time

host = 'https://www.sephora.com'
path_chromedriver = '/home/daniel/chromedriver/chromedriver'

options = webdriver.ChromeOptions()
service = Service(path_chromedriver)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# def sephora_product_list(driver, host):
url = f'{host}/shop/skincare'
driver.get(url)
time.sleep(1)

# close modal
modal_close = driver.find_elements(By.XPATH, '//button[@data-at="modal_close"]')
if modal_close.size() != 0:
    modal_close[0].click()

# define main category to scrap
category_to_scrap = 'Moisturizers'
categories_container = driver.find_element(By.XPATH, '//ul[@data-at="categories_large_view"]')
category = categories_container.find_element(By.XPATH, f'.//a[text()[contains(., "{category_to_scrap}")]]')

category.click()
time.sleep(2)

category_main = category_to_scrap.lower()

# navigate all subcategories
subcategories = driver.find_elements(By.XPATH, '//ul[@data-at="categories_large_view"]/li')

subcategories[-1].click()
time.sleep(2)
scroll_down(driver)

# check if there is more products to show
show_more_button = driver.find_elements(By.XPATH, '//button[text()[contains(., "Show More Products")]]')
if show_more_button.size() != 0:
    show_more_button[0].click()
    scroll_down(driver)

# get product links
product_links = []
product_tiles = driver.find_elements(By.XPATH, '//a[contains(@data-comp, "ProductTile")]')

for tile in product_tiles:
    product_links.append(tile.get_attribute('href'))

for link in product_links:
    sephora_scrape_product(link)

print(product_links)

#product_titles = driver.find_elements(By.XPATH, '//a[@data-comp="LazyLoad ProductTile "]/span[contains(@class, "ProductTile-name")]')

#for title in product_titles:
#   print(title.text)