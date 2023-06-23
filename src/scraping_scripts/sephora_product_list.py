from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from src.utils.check_exists_by_xpath import check_exists_by_xpath
from src.utils.clear_subcategory_name import clear_subcategory_name
from src.utils.list_file_iteration import save_list_in_file
from src.utils.save_links_file import save_links_file
from src.utils.scroll_down import scroll_down
from src.constants import HOST, DRIVER_PATH
import time


total_execution_time_start = time.time()

# define main category to scrap
CATEGORY = 'Self Tanners'


# selenium set-up
URL = f'{HOST}/shop/skincare'
path_chromedriver = DRIVER_PATH

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
# block chrome notifications
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)

service = Service(path_chromedriver)
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
time.sleep(2)

# close modal
if check_exists_by_xpath(driver, '//button[@data-at="modal_close"]'):
    modal_close = driver.find_element(By.XPATH, '//button[@data-at="modal_close"]')
    modal_close.click()

categories_container = driver.find_element(By.XPATH, '//ul[@data-at="categories_large_view"]')
category = categories_container.find_element(By.XPATH, f'.//a[text()[contains(., "{CATEGORY}")]]')

category.click()
time.sleep(2)
# close modal
if check_exists_by_xpath(driver, '//button[@data-at="modal_close"]'):
    modal_close = driver.find_element(By.XPATH, '//button[@data-at="modal_close"]')
    modal_close.click()

category_main = CATEGORY.lower()

# navigate all subcategories
if check_exists_by_xpath(driver, '//ul[@data-at="categories_large_view"]/li'):
    subcategories = driver.find_elements(By.XPATH, '//ul[@data-at="categories_large_view"]/li')
else:
    SUBCATEGORY = clear_subcategory_name(category_main)
    time.sleep(2)

    scroll_down(driver)

    # check if there is more products to show
    show_more_xpath = '//button[text()[contains(., "Show More Products")]]'
    while check_exists_by_xpath(driver, show_more_xpath):
        show_more_button = driver.find_element(By.XPATH, '//button[text()[contains(., "Show More Products")]]')
        show_more_button.click()
        time.sleep(2)
        scroll_down(driver)

    # get product links
    product_links = []
    product_tiles = driver.find_elements(By.XPATH, '//a[contains(@data-comp, "ProductTile")]')

    for tile in product_tiles:
        product_links.append(tile.get_attribute('href'))

    filename = f'{CATEGORY.lower()}::{SUBCATEGORY.lower()}_{len(product_links)}_links'
    save_links_file(filename, CATEGORY.lower(), product_links)

    driver.quit()

for index, subcategory in enumerate(subcategories, start=1):
    start_scrape_time = time.time()
    time.sleep(2)

    try:
        subcategory = subcategories[0]
        subcategory.click()
    except:
        subcategory = driver.find_element(By.XPATH, f'//ul[@data-at="categories_large_view"]/li[{index}]')
        subcategory.click()

    SUBCATEGORY = clear_subcategory_name(subcategory.text)
    time.sleep(2)

    scroll_down(driver)

    # check if there is more products to show
    show_more_xpath = '//button[text()[contains(., "Show More Products")]]'
    while check_exists_by_xpath(driver, show_more_xpath):
        show_more_button = driver.find_element(By.XPATH, '//button[text()[contains(., "Show More Products")]]')
        show_more_button.click()
        time.sleep(2)
        scroll_down(driver)

    # get product links
    product_links = []
    product_tiles = driver.find_elements(By.XPATH, '//a[contains(@data-comp, "ProductTile")]')

    for tile in product_tiles:
        product_links.append(tile.get_attribute('href'))

    filename = f'{CATEGORY.lower()}::{SUBCATEGORY.lower()}_{len(product_links)}_links'
    save_links_file(filename, CATEGORY.lower(), product_links)

    # finish scrape
    execution_time = time.time() - start_scrape_time
    execution_time_rounded = round(execution_time, 2)
    print('###########################')
    print(
        f'[SUCCESS] Successfully scraped [{CATEGORY}::{SUBCATEGORY}] in {"--- %.2f seconds ---" % execution_time_rounded}')
    print('###########################')

    breadcrumbs = driver.find_element(By.XPATH, f'//nav[@aria-label="Breadcrumb"]')
    driver.execute_script("arguments[0].scrollIntoView();", breadcrumbs)

    previous_category = breadcrumbs.find_element(By.XPATH, f'./ol/li[2]/a')
    previous_category.click()

    # finish scrape
    total_execution_time = time.time() - total_execution_time_start
    total_execution_time_rounded = round(execution_time, 2)
    print('###########################')
    print(
        f'[SUCCESS] everything in {"--- %.2f seconds ---" % execution_time_rounded}')
    print('###########################')
