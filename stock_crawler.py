import time
import twstock
import colorama
import requests

def process_message(stock, stock_hist):
    output_message = stock['info']['time'] + '\t'
    output_message += stock['info']['name'] + '\t'
    output_message += 'now price:'
    if stock['realtime']['latest_trade_price'] == stock['realtime']['best_bid_price'][0]:
        output_message += colorama.Fore.GREEN + stock['realtime']['latest_trade_price'] + colorama.Style.RESET_ALL + '\t'
    else:
        output_message += colorama.Fore.RED + stock['realtime']['latest_trade_price'] + colorama.Style.RESET_ALL + '\t'
    output_message += 'volume:' + stock['realtime']['trade_volume'] + '\t'
    change_range = float(stock['realtime']['latest_trade_price']) - float(stock_hist.price[-1])#float(stock['realtime']['open'])
    change_range = round(change_range + 0.001, 2)
    output_message += 'change range:'
    if change_range > 0:
        output_message += colorama.Fore.RED + str(change_range) + colorama.Style.RESET_ALL + '\t'
    else:
        output_message += colorama.Fore.GREEN + str(change_range) + colorama.Style.RESET_ALL + '\t'
    return output_message


colorama.init()

semi_num = ['5371', '2880', '6525', '2457']
stock_old = {}
stock_hist = {}
for i in range(0, len(semi_num)):
    stock = twstock.realtime.get(semi_num[i])
    if stock['success']:
        stock_old.update({semi_num[i]: stock})
        stock_hist.update({semi_num[i]: twstock.Stock(semi_num[i])})

while True:
    for i in range(0, len(semi_num)):
        time.sleep(1)
        try:
            stock = twstock.realtime.get(semi_num[i])
            if stock['success']:
                if stock_old[semi_num[i]]['realtime']['accumulate_trade_volume'] != stock['realtime']['accumulate_trade_volume']:
                    stock_old.update({semi_num[i]: stock})

                    print(process_message(stock, stock_hist[semi_num[i]]))
        except (requests.ConnectionError) as error:
            continue
        #break
