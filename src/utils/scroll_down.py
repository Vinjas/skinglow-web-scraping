import time


def scroll_down(driver):
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 50):
        driver.execute_script("window.scrollTo(0, {});".format(i))
