import time
from loguru import logger
import random
import ccxt
from colorama import Fore
from tqdm import trange

# ===================================== options ===================================== #

shuffle = False                                                     # True / False. если нужно перемешать кошельки
delay_wallets = [10, 20]                                            # минимальная и максимальная задержка между кошельками
need_fee = 200                                                      # максимальная комиссия в MEME
amount_MEME_for_withdrawal = [269, 270]                             # кол-во MEME для вывода с учетом комиссии!!!
time_sleep = 180                                                    # время через которое проверяет комиссию

# BingX API
bingx_apikey = ""
bingx_apisecret = ""

# =================================== end-options =================================== #

def intro(wallets):
    print()
    print(f'Subscribe: https://t.me/CryptoMindYep')
    print(f'Total wallets: {len(wallets)}\n')
    #input('Press ENTER: ')

    print()
    print(f'| {Fore.LIGHTGREEN_EX}BingX Withdrawal{Fore.RESET} |'.center(100, '='))
    print('\n')

def outro():
    for i in trange(3, desc=f'{Fore.LIGHTBLACK_EX}End process...', ncols=50, bar_format='{desc} {percentage:3.0f}%'):
        time.sleep(1)
    print(f'{Fore.RESET}\n')
    print(f'| {Fore.LIGHTGREEN_EX}END{Fore.RESET} |'.center(100, '='))
    print()
    print(input(f'Если помог скрипт: https://t.me/CryptoMindYep\nMetamask: 0x5AfFeb5fcD283816ab4e926F380F9D0CBBA04d0e'))

def sleeping_between_wallets():
    x = random.randint(delay_wallets[0], delay_wallets[1])
    for i in trange(x, desc=f'{Fore.LIGHTBLACK_EX}sleep...', ncols=50, bar_format='{desc}  {n_fmt}/{total_fmt}s |{bar}| {percentage:3.0f}%'):
        time.sleep(1)
    print()

def bingx_withdraw(address):

    exchange = ccxt.bingx({
        'apiKey': bingx_apikey,
        'secret': bingx_apisecret,
        'options': {
            'adjustForTimeDifference': True,
            'defaultType': 'spot',
        },
    })

    try:
        while True:
            responce = exchange.fetch_deposit_withdraw_fee('MEME')
            fee = float(responce['info']['networkList'][0]['withdrawFee'])
            if fee < need_fee:
                logger.info(f"Fee - {fee} Работаем")
                break
            logger.info(f"Fee - {fee} Ушел спать на {time_sleep} сек...")
            time.sleep(time_sleep)

        amount_for_withdrawal = random.randint(amount_MEME_for_withdrawal[0], amount_MEME_for_withdrawal[1])
        
        exchange.withdraw(
            code='MEME',
            amount=amount_for_withdrawal,
            address=address,
            tag=None,
            params={
                "network": 'ERC20'
            }
        )
        logger.success(f'Вывел {amount_for_withdrawal} MEME ')

    except Exception as error:
        logger.error(f' {error}')

def main():
    with open('wallets.txt', 'r') as file:
        wallets = [row.strip() for row in file]
    intro(wallets)
    count_wallets = len(wallets)

    data = [(wallets[i]) for i in range(len(wallets))]

    if shuffle:
        random.shuffle(data)

    for idx, (wallet) in enumerate(data, start=1):
        address = wallet

        print(f'{idx}/{count_wallets} : {address}\n')

        try:
            bingx_withdraw(address)
        except Exception as e:
            logger.error(f'{idx}/{count_wallets} Failed: {str(e)}')

        if idx != count_wallets:
            sleeping_between_wallets()

    outro()

main()
