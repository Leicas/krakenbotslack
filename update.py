import requests, json
with open("data.json","r") as data_file:
    historique = json.load(data_file)
response = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
prixnow = float(response.json()['result']['XXBTZEUR']['p'][1])
#historique = {}
augment = (prixnow - float(historique['prix']))/ float(historique['prix']) * 100.0
historique['prix']=prixnow
message = 'Le bitcoin est à : ' + "%.2f" % prixnow + '€, variation de : ' + "%.2f" % augment + '% depuis hier'
r = requests.post('https://hooks.slack.com/services/'+historique['slack'], json={"text": message})
#print (message)
with open("data.json","w") as outfile:
    json.dump(historique, outfile, indent=4)
