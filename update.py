# -*- coding: utf-8 -*-
import requests, json, time
with open("data.json","r") as data_file:
    historique = json.load(data_file)
for attempt in range(10):
    try:
        response = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR,ETHEUR')
        prixnow = {}
        prixnow['btc'] = float(response.json()['result']['XXBTZEUR']['p'][1])
        prixnow['eth'] = float(response.json()['result']['XETHZEUR']['p'][1])
        end = int(time.time())
        start = end - 86400
        responsepoloniex = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair=USDT_DASH&start='+str(start)+'&end='+str(end)+'&period=86400')
        prixnow['dash'] = float(responsepoloniex.json()[0]['weightedAverage'])
        responsepoloniex = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair=BTC_BTS&start='+str(start)+'&end='+str(end)+'&period=86400')
        prixnow['bts'] = float(responsepoloniex.json()[0]['weightedAverage'])*1e06
        #historique = {}
        #historique['prix'] = {}
        augment = {}
        augment['btc'] = (prixnow['btc'] - float(historique['prix']['btc']))/ float(historique['prix']['btc']) * 100.0
        augment['eth'] = (prixnow['eth'] - float(historique['prix']['eth']))/ float(historique['prix']['eth']) * 100.0
        augment['dash'] = (prixnow['dash'] - float(historique['prix']['dash']))/ float(historique['prix']['dash']) * 100.0
        augment['bts'] = (prixnow['bts'] - float(historique['prix']['bts']))/ float(historique['prix']['bts']) * 100.0
        historique['prix']['btc']=prixnow['btc']
        historique['prix']['eth']=prixnow['eth']
        historique['prix']['dash']=prixnow['dash']
        historique['prix']['bts']=prixnow['bts']
        message = 'Bitcoin(kraken) est à : ' + "%.2f" % prixnow['btc'] + '€, variation de : ' + "%.2f" % augment['btc'] + '% depuis hier \n'
        message = message + 'Ethereum(kraken) est à : ' + "%.2f" % prixnow['eth'] + '€, variation de : ' + "%.2f" % augment['eth'] + '% depuis hier \n'
        message = message + 'Dash(Poloniex) est à : ' + "%.2f" % prixnow['dash'] + '$, variation de : ' + "%.2f" % augment['dash'] + '% depuis hier \n'
        message = message + 'Bitshares(Poloniex) est à : ' + "%.2f" % prixnow['bts'] + 'µbtc, variation de : ' + "%.2f" % augment['bts'] + '% depuis hier \n'
        r = requests.post('https://hooks.slack.com/services/'+historique['slack'], json={"text": message})
        #print (message)
        with open("data.json","w") as outfile:
            json.dump(historique, outfile, indent=4)
    except:
        print('erreur')
    else:
        break
