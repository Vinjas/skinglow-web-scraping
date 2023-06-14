from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
