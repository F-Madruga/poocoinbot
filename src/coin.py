import os
import time
from constants import POOCOIN_URL, REFRESH_COIN_PAGE_TIME_WAITING
from utils import change_tab, get_url, hasXpath, open_new_tab
import numpy as np


class Coin():
    def __init__(self, driver, poocoin_index, address, tab_index, entry_value, take_profit, stop_loss):
        self.address = address
        self.tab_index = tab_index
        self.amount = self.get_amount(driver, poocoin_index)
        self.url = os.path.join(POOCOIN_URL, 'tokens', self.address)
        open_new_tab(driver)
        self.go_to_coin(driver)
        self.name = self.get_coin_name(driver)
        self.entry_value = entry_value
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.value = None
        self.profit = None

    def go_to_coin(self, driver):
        change_tab(driver, self.tab_index)
        driver.get(self.url)

    def get_amount(self, driver, poocoin_index):
        change_tab(driver, poocoin_index)
        # Click trade options
        driver.find_element_by_xpath(
            '//*[@id="root"]/nav/div/div/div[2]/a[2]').click()
        # Select coin button
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div/div/form/div[2]/div/div[2]/div[2]').click()
        # Enter address
        driver.find_element_by_xpath(
            '/html/body/div[6]/div/div/div/div[3]/form/button').click()
        driver.find_element_by_xpath(
            '/html/body/div[6]/div/div/div/div[3]/form/div/input').send_keys(self.address)
        driver.find_element_by_xpath(
            '/html/body/div[6]/div/div/div/div[3]/form/div/button').click()
        # Get amount
        amount = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div/div/form/div[2]/div/div[1]/div').text.replace('Balance: ', '')
        return np.format_float_positional(float(amount))

    def get_coin_name(self, driver):
        driver.implicitly_wait(15)
        name = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1').text
        return name

    def refresh_coin_tab(self, driver):
        change_tab(driver, self.tab_index)
        driver.refresh()

    def update_value(self, driver):
        change_tab(driver, self.tab_index)
        if get_url(driver) != self.url:
            self.go_to_coin(driver)
            time.sleep(REFRESH_COIN_PAGE_TIME_WAITING)
        driver.implicitly_wait(15)
        value = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span').text.replace('$', '')
        while value == '':
            driver.implicitly_wait(15)
            value = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span').text.replace('$', '')
        self.value = float(value)

    def update_profit(self):
        self.profit = (self.value / self.entry_value) - 1.0

    def get_status(self):
        if self.profit >= self.take_profit:
            return 'TAKE PROFIT'
        elif self.profit <= self.stop_loss:
            return 'STOP LOSS'
        else:
            return 'HOLD'
