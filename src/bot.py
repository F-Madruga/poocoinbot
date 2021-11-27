import time
import numpy as np
from constants import CHROMEDRIVER_PATH, POOCOIN_URL, BRAVE, PANCAKESWAP_URL, REFRESH_COIN_PAGE_TIME_WAITING, WALLET_TYPE
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from utils import change_tab, hasXpath, open_new_tab
import os
from coin import Coin
import pandas as pd


class Bot():
    PANCAKESWAP_INDEX = 0
    POOCOIN_TAB_INDEX = 1

    def __init__(self, coins):
        if BRAVE:
            options = Options()
            options.binary_location = '/usr/bin/brave-browser'
            self.driver = webdriver.Chrome(
                options=options, executable_path=CHROMEDRIVER_PATH)
        else:
            self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        self.got_to_pancakeswap()
        open_new_tab(self.driver)
        self.got_to_poocoin()
        self.poocoin_connect_wallet()
        self._load_coins(coins)

    def work(self, refresh=False):
        if refresh:
            for coin in self.coins:
                coin.refresh_coin_tab(self.driver)
        time.sleep(REFRESH_COIN_PAGE_TIME_WAITING)
        coins_dict = {
            'COIN': [],
            'AMOUNT': [],
            'STOP LOSS': [],
            'TAKE PROFIT': [],
            'ENTRY_VALUE ($)': [],
            'VALUE ($)': [],
            'PROFIT': [],
            'STATUS': []
        }
        for coin in self.coins:
            coin.update_value(self.driver)
            coin.update_profit()
            coins_dict['COIN'].append(coin.name)
            coins_dict['AMOUNT'].append(coin.amount)
            coins_dict['STOP LOSS'].append(coin.stop_loss)
            coins_dict['TAKE PROFIT'].append(coin.take_profit)
            coins_dict['ENTRY_VALUE ($)'].append(
                np.format_float_positional(coin.entry_value))
            coins_dict['VALUE ($)'].append(
                np.format_float_positional(coin.value))
            coins_dict['PROFIT'].append(
                np.format_float_positional(coin.profit))
            coins_dict['STATUS'].append(coin.get_status())
        print(pd.DataFrame(coins_dict).to_string(index=False))

    def got_to_pancakeswap(self):
        change_tab(self.driver, Bot.PANCAKESWAP_INDEX)
        self.driver.get(PANCAKESWAP_URL)

    def got_to_poocoin(self):
        change_tab(self.driver, Bot.POOCOIN_TAB_INDEX)
        self.driver.get(POOCOIN_URL)

    def pancakeswap_connect_wallet(self):
        change_tab(self.driver, Bot.PANCAKESWAP_INDEX)
        self.driver.find_element_by_xpath(
            '//*[@id="root"]/div[1]/div[1]/nav/div[2]/button').click()
        if WALLET_TYPE == 'WalletConnect':
            self.driver.find_element_by_xpath(
                '//*[@id="wallet-connect-walletconnect"]').click()
            input('Press ENTER when you finish connect your wallet')

    def pancakeswap_wallet_is_connected(self):
        change_tab(self.driver, Bot.PANCAKESWAP_INDEX)
        return not hasXpath(self.driver, '//*[@id="root"]/div[1]/div[1]/nav/div[2]/button')

    def poocoin_connect_wallet(self):
        change_tab(self.driver, Bot.POOCOIN_TAB_INDEX)
        self.driver.implicitly_wait(15)
        self.driver.find_element_by_xpath(
            '//*[@id="root"]/nav/div/div/div[3]/button').click()
        if WALLET_TYPE == 'WalletConnect':
            self.driver.find_element_by_xpath(
                '/html/body/div[3]/div/div/div/button[2]').click()
            input('Press ENTER when you finish connect your wallet\n')

    def _load_coins(self, coins):
        self.coins = []
        for i, coin_dict in enumerate(coins):
            self.coins.append(Coin(self.driver,
                                   Bot.POOCOIN_TAB_INDEX,
                                   coin_dict['address'],
                                   i + Bot.POOCOIN_TAB_INDEX + 1,
                                   float(coin_dict['entry_value']),
                                   float(coin_dict['take_profit']),
                                   float(coin_dict['stop_loss'])))
