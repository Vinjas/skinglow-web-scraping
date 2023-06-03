from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium_scripts.sephora_product_list import sephora_product_list

host = 'https://www.sephora.com'
path_chromedriver = '/home/daniel/chromedriver/chromedriver'

options = webdriver.ChromeOptions()
service = Service(path_chromedriver)
driver = webdriver.Chrome(service=service, options=options)

sephora_product_list(driver, host)
