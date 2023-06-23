from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.dynamo_db.add_column_in_table import add_column_in_table
from src.dynamo_db.put_item_in_table import put_item_in_table
from src.utils.check_exists_by_xpath import check_exists_by_xpath
from src.constants import HOST, DRIVER_PATH
import time
import json
from fake_useragent import UserAgent

total_execution_time_start = time.time()

URL = 'https://incidecoder.com/decode-inci'
path_chromedriver = DRIVER_PATH

with open('ing_list_test.json', 'r') as file:
    ing_list_full = json.load(file)

for index, product in enumerate(ing_list_full):
    # random user agent
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)

    options.add_argument(f'user-agent={userAgent}')
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
    time.sleep(1)

    print("#######################")
    print(f"[LOG] Start with product {product['PK']}")

    if "ingredients" not in product:
        ing_list_full.remove(product)
        print(f"El producto {product['ingredient-name']} en el índice {index} ha sido eliminado")

        with open('ing_list_test.json', 'w') as file:
            json.dump(ing_list_full, file, indent=2)
        continue

    product_ingredients = product["ingredients"]

    product_ingredients_string = ", ".join(product_ingredients)
    print(product_ingredients_string)

    # input ingredients in textarea
    textarea = driver.find_element(By.ID, "inci")
    submit_button = driver.find_element(By.ID, "submit-inci")

    textarea.send_keys(product_ingredients_string)
    time.sleep(1)
    # textarea.send_keys(Keys.ENTER)
    try:
        submit_button.click()
        time.sleep(5)
    except:
        print("[ERROR] Error submitting")
        continue

    # check if there are coincidences
    if not check_exists_by_xpath(driver, '//a[contains(@class, "ingred-link black")]'):
        continue

    # click "more" buttons
    if check_exists_by_xpath(driver, '//button[contains(@class, "link-like showmore-link-desktop showmore-link")]'):
        more_buttons = driver.find_elements(By.XPATH,
                                            '//button[contains(@class, "link-like showmore-link-desktop showmore-link")]')
        for button in more_buttons:
            button.click()
            time.sleep(0.5)

    #################################
    # KEY INGREDIENTS
    #################################
    key_ingredients = []
    key_ingredients_titles = driver.find_elements(By.XPATH,
                                                  "//h3[text()[contains(., 'Key Ingredients')]]/following-sibling::div")
    for key_ing_data in key_ingredients_titles:
        key_ingredient_dict = {}
        key_ing = key_ing_data.find_elements(By.TAG_NAME, "span")

        key_ing_category = key_ing[0].text
        key_ing.pop(0)

        key_ing_items = []
        key_ing_items_parsed = []
        for ing in key_ing:
            key_ing_items.append(ing.text)
        for ing in key_ing_items:
            if ing != '':
                key_ing_items_parsed.append(ing.rstrip(','))

        # create and append dictionary
        key_ingredient_dict[key_ing_category] = key_ing_items_parsed
        key_ingredients.append(key_ingredient_dict)

    # put key ingredients in product database
    add_column_in_table(product['PK'], "product#data_EN", "key-ingredients", "skinglow-products", key_ingredient_dict)

    print("#######################")
    print("[SUCCESS] key_ingredients", key_ingredients)

    #################################
    # INGREDIENT LIST DETAILS
    #################################
    data_ingredients_list_full = {}

    ingredient_list_all = driver.find_elements(By.XPATH,
                                               "//div[@id='showmore-section-ingredlist-long']/div[contains(@class, 'ingred-long')]")
    for ingredient_data in ingredient_list_all:
        data_ingredient_complete = {}

        # NAME
        if not check_exists_by_xpath(ingredient_data, "./div[@class='ingred-header']/a"):
            continue
        data_ingredient_name = ingredient_data.find_element(By.XPATH, "./div[@class='ingred-header']/a").text
        data_ingredient_complete["ingredient#ingredient-name"] = data_ingredient_name

        # quick info block
        if check_exists_by_xpath(ingredient_data, "./div[contains(@class, 'ingredquickinfo')]"):
            ingredient_quick_info = ingredient_data.find_element(By.XPATH, "./div[contains(@class, 'ingredquickinfo')]")

        # IRRITANCY
        if check_exists_by_xpath(ingredient_quick_info,
                                 "./span/span[contains(text(), 'Irritancy')]/following-sibling::span[@class='value']"):
            data_ingredient_irritancy = ingredient_quick_info.find_element(By.XPATH,
                                                                           "./span/span[contains(text(), 'Irritancy')]/following-sibling::span[@class='value']").text
            data_ingredient_complete["ingredient#irritancy"] = data_ingredient_irritancy

        # COMEDOGENICITY
        if check_exists_by_xpath(ingredient_quick_info,
                                 "./span/span[contains(text(), 'Comedogenicity')]/following-sibling::span[@class='value']"):
            data_ingredient_comedogenicity = ingredient_quick_info.find_element(By.XPATH,
                                                                                "./span/span[contains(text(), 'Comedogenicity')]/following-sibling::span[@class='value']").text
            data_ingredient_complete["ingredient#comedogenicity"] = data_ingredient_comedogenicity

        # WHAT IT DOES
        if check_exists_by_xpath(ingredient_quick_info,
                                 "./span/span[contains(text(), 'What-it-does')]/following-sibling::span[@class='value']"):
            data_what_it_does = []
            what_it_does_items = ingredient_quick_info.find_elements(By.XPATH,
                                                                     "./span/span[contains(text(), 'What-it-does')]/following-sibling::span[@class='value']/a")
            for wid in what_it_does_items:
                data_what_it_does.append(wid.text)
            data_ingredient_complete["ingredient#what-it-does"] = data_what_it_does

        # EXTRA
        if check_exists_by_xpath(ingredient_data, "./div[@class='ingreddescbox']"):
            ingredient_body = ingredient_data.find_element(By.XPATH, "./div[@class='ingreddescbox']")

            # check star lists
            if check_exists_by_xpath(ingredient_body, "./ul[contains(@class, 'starlist')]") \
                    and not check_exists_by_xpath(ingredient_body, "./p/img"):
                data_extra = "SPECIAL"

            if check_exists_by_xpath(ingredient_body, "./p") \
                    and not check_exists_by_xpath(ingredient_body, "./p/img") \
                    and not check_exists_by_xpath(ingredient_body, "./ul[contains(@class, 'starlist')]"):
                data_extra = []
                extra_text = ingredient_body.find_elements(By.XPATH, "./p")

                for text in extra_text:
                    if check_exists_by_xpath(text, "./strong"):
                        bold_text = text.find_elements(By.XPATH, "./strong")
                        for item in bold_text:
                            data_extra.append(item.text)

            data_ingredient_complete["ingredient#extra-info"] = data_extra

            if len(data_ingredient_complete["ingredient#extra-info"]) == 0:
                del data_ingredient_complete["ingredient#extra-info"]

        #################################
        # ADD INGREDIENT TO DATABASE
        #################################
        put_item_in_table(data_ingredient_complete, 'skinglow-ingredients')

        data_ingredient_complete["PK"] = product["PK"]
        data_ingredient_complete["SK"] = f'product#ingredient#{data_ingredient_name}'
        put_item_in_table(data_ingredient_complete, 'skinglow-products')

        print("#######################")
        print("[SUCCESS]", data_ingredient_name)
        print(data_ingredient_complete)

    # Delete JSON entry after finish
    ing_list_full.remove(product)

    with open('ing_list_test.json', 'w') as file:
        json.dump(ing_list_full, file, indent=2)

    driver.quit()
