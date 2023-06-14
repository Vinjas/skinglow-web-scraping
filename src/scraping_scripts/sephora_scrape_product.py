import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src.utils.check_exists_by_xpath import check_exists_by_xpath
from src.utils.find_matching_data import find_matching_skin, find_matching_highlights, find_matching_concerns
from src.utils.list_file_iteration import iterate_file_list
from src.utils.parse_ingredients_list import parse_ingredients_list
from src.constants import OVERVIEW_OPTION, CLINICAL_RESULTS_OPTION, IMPORTANT_INGREDIENTS_OPTION, SKIN_TYPE_OPTION, \
    CONCERNS_OPTION, EXTRA_INFO_OPTION, SKIN_TYPES_LIST, HIGHLIGHT_LIST, CONCERNS_LIST, VEGAN, HOST
from src.translation.deepl_tranlate import deepl_translate
from src.translation.google_translate import google_translate
from src.dynamo_db.put_item_in_table import put_item_in_table

import time
import decimal


CATEGORY = "cleansers"
LANGUAGES_TO_TRANSLATE = []


# selenium set-up
start_scrape_time = time.time()
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

# open links file
current_dir = os.getcwd()
folder_path = os.path.join(current_dir, '..', '..', 'product_links', CATEGORY.lower())

print(f'Files to scrape: {os.listdir(folder_path)}')

for filename in os.listdir(folder_path):
    file_link = os.path.join(folder_path, filename)
    if os.path.isfile(file_link):
        links_list = iterate_file_list(file_link)

        print(links_list)

        for index, link in enumerate(links_list):
            URL = link

            driver.get(URL)
            # if index == 0:
            #     driver.get(URL)
            # else

            # close modal
            if check_exists_by_xpath(driver, '//button[@data-at="modal_close"]'):
                modal_close = driver.find_element(By.XPATH, '//button[@data-at="modal_close"]')
                modal_close.click()

            # open everything needed
            if check_exists_by_xpath(driver, '//button[text()[contains(., "Show more")]]'):
                show_more_button = driver.find_element(By.XPATH, '//button[text()[contains(., "Show more")]]')
                show_more_button.click()

            if check_exists_by_xpath(driver, '//button[@data-at="ingredients"]'):
                ingredients_button = driver.find_element(By.XPATH, '//button[@data-at="ingredients"]')
                ingredients_button.click()

            if check_exists_by_xpath(driver, '//button[@data-at="how_to_use_btn"]'):
                how_to_use_button = driver.find_element(By.XPATH, '//button[@data-at="how_to_use_btn"]')
                how_to_use_button.click()

            ##################################

            # scrape data
            # PK
            PK = int(driver.find_element(By.XPATH, '//*[@data-at="item_sku"]').text.split(" ")[1])
            print('###########################')
            print(f'[LOG] Start scraping [{PK}]...')

            # category_name
            category_name = filename.split("_")[0]

            # brand
            brand = driver.find_element(By.XPATH, '//*[@data-at="brand_name"]').text

            # volume
            if check_exists_by_xpath(driver, '//*[@data-at="sku_name_label"]'):
                volume = driver.find_element(By.XPATH, '//*[@data-at="sku_name_label"]').text.replace("Size: ", "")
            else:
                volume = None

            print('25%')

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
            else:
                clinical_results = None

            print('50%')

            # highlight-ingredients
            if IMPORTANT_INGREDIENTS_OPTION in overview_titles:
                index = overview_titles.index(IMPORTANT_INGREDIENTS_OPTION)
                next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

                important_ingredients = about_text.split(IMPORTANT_INGREDIENTS_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

                if len(important_ingredients.split()) == 1:
                    important_ingredients = None
            else:
                important_ingredients = None

            # extra_info
            if EXTRA_INFO_OPTION in overview_titles:
                index = overview_titles.index(EXTRA_INFO_OPTION)
                next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

                extra_info = about_text.split(EXTRA_INFO_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

                if len(extra_info.split()) == 1:
                    extra_info = None
            else:
                extra_info = None

            # concerns
            if CONCERNS_OPTION in overview_titles:
                index = overview_titles.index(CONCERNS_OPTION)
                next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

                concerns_unparsed = about_text.split(CONCERNS_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")

                concerns = find_matching_concerns(concerns_unparsed, CONCERNS_LIST)

                if len(concerns) == 0:
                    concerns = None
            else:
                concerns = None

            # skin_type
            if SKIN_TYPE_OPTION in overview_titles:
                index = overview_titles.index(SKIN_TYPE_OPTION)
                next_element = overview_titles[index + 1] if index < len(overview_titles) - 1 else None

                skin_type_unparsed = about_text.split(SKIN_TYPE_OPTION)[1].split(next_element)[0].strip().replace("\n", " ")
                skin_type = find_matching_skin(skin_type_unparsed, SKIN_TYPES_LIST)
            else:
                skin_type = None

            print('75%')

            # highlights
            if check_exists_by_xpath(driver, '//h2[text()[contains(., "Highlights")]]'):
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

                if len(highlights) == 0:
                    highlights = None
            else:
                highlights = None

            # ingredients
            if check_exists_by_xpath(driver, '//div[@aria-labelledby="ingredients_heading"]/div/div'):
                ingredients_list = driver.find_element(By.XPATH, '//div[@aria-labelledby="ingredients_heading"]/div/div').text
                ingredients = parse_ingredients_list(ingredients_list)
                if len(ingredients) == 0:
                    ingredients = None
            else:
                ingredients = None

            # how_to
            if check_exists_by_xpath(driver, '//div[@data-at="how_to_use_section"]'):
                how_to = driver.find_element(By.XPATH, '//div[@data-at="how_to_use_section"]').text.replace("\n", " ")

                if len(how_to.split()) == 1:
                    how_to = None
            else:
                how_to = None

            # review_score
            if check_exists_by_xpath(driver, '//span[@data-at="number_of_reviews"]'):
                review_button = driver.find_element(By.XPATH, '//span[@data-at="number_of_reviews"]')
                review_button.click()
                time.sleep(1)

                if check_exists_by_xpath(driver, '//div[contains(@data-comp, "HistogramChart")]/../following-sibling::div/div/span'):
                    review_score = decimal.Decimal(driver.find_element(By.XPATH, '//div[contains(@data-comp, "HistogramChart")]/../following-sibling::div/div/span').text)
                else:
                    review_score = None
            else:
                review_score = None

            print('100%')

            # create dictionary
            unparsed_product_dictionary_EN = {
                "PK": PK,
                "SK": "product#data_EN",
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

            # filter dictionary for None values
            product_dictionary_EN = {key: value for key, value in unparsed_product_dictionary_EN.items() if value is not None}

            print(product_dictionary_EN)

            put_item_in_table(product_dictionary_EN)

            # translation of data
            # product_dictionary_translations = {}
            #
            # print(f'[LOG] Translating into {LANGUAGES_TO_TRANSLATE}...')
            #
            # for language in LANGUAGES_TO_TRANSLATE:
            #     translated_ingredients = []
            #     for i in ingredients:
            #         translated_ingredients.append(google_translate(i, language).capitalize())
            #
            #     product_dictionary_translations[f'{language.upper()}'] = {
            #         "PK": PK,
            #         "SK": f"product#data_{language.upper()}",
            #         "brand": brand,
            #         "category#name": category_name,
            #         "clinical-results": google_translate(clinical_results, language),
            #         "concerns": concerns,
            #         "extra-info": google_translate(extra_info, language),
            #         "highlights": highlights,
            #         "how-to": google_translate(how_to, language),
            #         "important-ingredients": google_translate(important_ingredients, language),
            #         "ingredients": translated_ingredients,
            #         "overview": deepl_translate(overview, language),
            #         "product-name": deepl_translate(product_name, language),
            #         "review-score": review_score,
            #         "skin-type": skin_type,
            #         "vegan": vegan,
            #         "volume": volume
            #     }
            #
            #     print(f'"{language}" done!')

# finish scrape
execution_time = time.time() - start_scrape_time
execution_time_rounded = round(execution_time, 2)
print(f'[SUCCESS] Successfully scraped everything in {"--- %.2f seconds ---" % execution_time_rounded}')
print('###########################')
