from selenium import webdriver
from selenium.webdriver.common.by import By
from src.utils.selenium_scroll_page import scroll_down


def sephora_product_list(driver, host):
    url = f'{host}/shop/skincare'

    driver.get(url)

    modal_close = driver.find_element(By.XPATH, '//button[@data-at="modal_close"]')
    modal_close.click()

    scroll_down(driver)

    product_titles = driver.find_elements(By.XPATH, '//a[@data-comp="LazyLoad ProductTile "]/span[contains(@class, "ProductTile-name")]')

    for title in product_titles:
        print(title.text)