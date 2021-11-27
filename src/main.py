from bot import Bot
import time
from constants import COINS, MAX_UPDATE_COIN_VALUE_TIME, MIN_UPDATE_COIN_VALUE_TIME, REFRESH_COIN_PAGE, REFRESH_COIN_PAGE_TIME_WAITING
import random


def main():
    bot = Bot(COINS)
    while True:
        bot.work(REFRESH_COIN_PAGE)
        print('\n')
        max_value = MAX_UPDATE_COIN_VALUE_TIME - REFRESH_COIN_PAGE_TIME_WAITING
        min_value = MIN_UPDATE_COIN_VALUE_TIME - REFRESH_COIN_PAGE_TIME_WAITING
        update_coin_value_time = random.randint(min_value, max_value)
        time.sleep(update_coin_value_time)


if __name__ == '__main__':
    main()
