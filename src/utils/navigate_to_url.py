def navigate_to_urls(driver, url):
    driver.execute_script("window.history.pushState({}, '', arguments[0]);", url)
    print(f"Navigating to: {url}")
