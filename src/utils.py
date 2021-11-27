def hasXpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def get_url(driver):
    return driver.current_url


def open_new_tab(driver):
    driver.execute_script("window.open('');")


def change_tab(driver, tab_index):
    driver.switch_to.window(driver.window_handles[tab_index])
