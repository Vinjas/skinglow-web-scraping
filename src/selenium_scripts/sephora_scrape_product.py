from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src.utils.find_matching_data import find_matching_skin, find_matching_highlights, find_matching_concerns
from src.utils.parse_ingredients_list import parse_ingredients_list
from src.utils.scroll_down import scroll_down

from src.constants import OVERVIEW_OPTION, CLINICAL_RESULTS_OPTION, IMPORTANT_INGREDIENTS_OPTION, SKIN_TYPE_OPTION, \
    CONCERNS_OPTION, EXTRA_INFO_OPTION, SKIN_TYPES_LIST, HIGHLIGHT_LIST, CONCERNS_LIST, VEGAN

import time
import pandas as pd


host = 'https://www.sephora.com/product/the-dewy-skin-cream-P441101?skuId=2181006&icid2=products%20grid:p441101:product'
path_chromedriver = '/home/daniel/chromedriver/chromedriver'

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

driver.get(host)
time.sleep(1)

# close modal
modal_close = driver.find_elements(By.XPATH, '//button[@data-at="modal_close"]')
modal_close[0].click()

# open everything needed
show_more_button = driver.find_element(By.XPATH, '//button[text()[contains(., "Show more")]]')
show_more_button.click()
ingredients_button = driver.find_element(By.XPATH, '//button[@data-at="ingredients"]')
ingredients_button.click()
how_to_use_button = driver.find_element(By.XPATH, '//button[@data-at="how_to_use_btn"]')
how_to_use_button.click()

##################################

# scrape data
# PK
PK = driver.find_element(By.XPATH, '//*[@data-at="item_sku"]').text.split(" ")[1]

# SK
SK = "product#data_EN"

# brand
brand = driver.find_element(By.XPATH, '//*[@data-at="brand_name"]').text

# category_name
breadcrumbs = driver.find_elements(By.XPATH, '//*[@aria-label="Breadcrumb"]/ol/li')
category_name = f"{breadcrumbs[1].text}::{breadcrumbs[2].text}"

# volume
volume = driver.find_element(By.XPATH, '//*[@data-at="sku_name_label"]').text.replace("Size: ", "")

# product_name
product_name = driver.find_element(By.XPATH, '//*[@data-at="product_name"]').text


# data from untagged text
about_container = driver.find_element(By.XPATH, '//*[@data-at="item_sku"]/../../div[not(@data-comp)]/div/div')
element_siblings = about_container.find_elements(By.XPATH, "./b")

overview_titles = []
for sibling in element_siblings:
    overview_titles.append(sibling.text)

about_text = about_container.text

# overview
if OVERVIEW_OPTION in overview_titles:
    index = overview_titles.index(OVERVIEW_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    overview = about_text.split(OVERVIEW_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

# clinical-results
if CLINICAL_RESULTS_OPTION in overview_titles:
    index = overview_titles.index(CLINICAL_RESULTS_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    clinical_results = about_text.split(CLINICAL_RESULTS_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

# highlight-ingredients
if IMPORTANT_INGREDIENTS_OPTION in overview_titles:
    index = overview_titles.index(IMPORTANT_INGREDIENTS_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    important_ingredients = about_text.split(IMPORTANT_INGREDIENTS_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

# extra_info
if EXTRA_INFO_OPTION in overview_titles:
    index = overview_titles.index(EXTRA_INFO_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    extra_info = about_text.split(EXTRA_INFO_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

# concerns
if CONCERNS_OPTION in overview_titles:
    index = overview_titles.index(CONCERNS_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    concerns_unparsed = about_text.split(CONCERNS_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

concerns = find_matching_concerns(concerns_unparsed, CONCERNS_LIST)

# skin_type
if SKIN_TYPE_OPTION in overview_titles:
    index = overview_titles.index(SKIN_TYPE_OPTION)
    next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

    skin_type_unparsed = about_text.split(SKIN_TYPE_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")
    skin_type = find_matching_skin(skin_type_unparsed, SKIN_TYPES_LIST)

# highlights
highlights_container = driver.find_element(By.XPATH, '//h2[text()[contains(., "Highlights")]]')
highlights_options = highlights_container.find_elements(By.XPATH, './following-sibling::div/div/span')

highlights_unparsed = []
for highlights_option in highlights_options:
    highlights_unparsed.append(highlights_option.text)

highlights = find_matching_highlights(highlights_unparsed, HIGHLIGHT_LIST)


# vegan
if VEGAN in highlights:
    vegan = 1
else:
    vegan = 0

# ingredients
ingredients_list = driver.find_element(By.XPATH, '//div[@aria-labelledby="ingredients_heading"]/div/div').text
ingredients = parse_ingredients_list(ingredients_list)

# how_to
how_to = driver.find_element(By.XPATH, '//div[@data-at="how_to_use_section"]').text.replace("\n", " ")

# review_score
scroll_down(driver)
review_score = driver.find_element(By.XPATH, '//div[contains(@data-comp, "HistogramChart")]/../following-sibling::div/div/span').text


# create dictionary
product_dictionary = {
    "PK": PK,
    "SK": SK,
    "brand": brand,
    "category#name": category_name,
    "clinical-results": clinical_results,
    "concerns": concerns,
    "extra-info": extra_info,
    "highlights": highlights,
    "how-to": how_to,
    "important-ingredients": important_ingredients,
    "ingredients": ingredients,
    "overview": overview,
    "product-name": product_name,
    "review-score": review_score,
    "skin-type": skin_type,
    "vegan": vegan,
    "volume": volume
}

print(product_dictionary)

# create DataFrame
df = pd.DataFrame({
    "PK": PK,
    "SK": SK,
    "brand": brand,
    "category#name": category_name,
    "clinical-results": clinical_results,
    "overview": overview
}, index=[0])

