from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from scraping_scripts.sephora_product_list import sephora_product_list
from constants import HOST

path_chromedriver = '/home/daniel/chromedriver/chromedriver'

options = webdriver.ChromeOptions()
service = Service(path_chromedriver)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

sephora_product_list(driver, HOST)
