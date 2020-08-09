import requests
import json
import math
from time import sleep
from fractions import Fraction

currencies = ['alt', 'jew', 'chroma']

url = 'http://www.pathofexile.com/api/trade/exchange/Standard' 
headers = {'content-type': 'application/json', 'X-Requested-With' : 'XMLHttpRequest'}

name = input("Name >> ")
camount = int(input('Chaos Amount >> '))
eamount = int(input('Exalt Amount >> '))
print()

def wait(minutes):
    for i in range(minutes):
        print("Refetching in " + str(minutes-i) + " minutes!")
        sleep(60)
    
    
def getQuery(buy, sell):
    return {"exchange": { "want":[sell], "have":[buy], "status": "online"}}

def fetch(buy, sell):
    r1 = json.loads(requests.post(url, data=json.dumps(getQuery(buy, sell)), headers=headers).text)
    tradeID = r1["id"]
    tradeNR = r1["result"][0]
    url2 = 'http://www.pathofexile.com/api/trade/fetch/' + tradeNR + '?exchange=true&query=' + tradeID
    response = json.loads(requests.get(url2, headers=headers).text)
    buyAmount  = response["result"][0]['listing']['price']['exchange']['amount']
    sellAmount = response["result"][0]['listing']['price']['item']['amount']
    seller = response['result'][0]['listing']['account']['name']
    return float(buyAmount), float(sellAmount), seller

def trade(cur, curamount):
    for c in currencies:
        print('CHECKING '+cur+'/'+c)
        b1, s1, seller1 = fetch(cur, c)
        b2, s2, seller2 = fetch(c, cur)

        k1 = Fraction(b1/s1 * 0.99)
        k2 = Fraction(b2/s2 * 0.99)

        f1 = curamount/k1.numerator
        n1 = math.ceil(k1.numerator * f1)
        d1 = math.ceil(k1.denominator * f1)

        f2 = curamount/k2.denominator
        n2 = math.ceil(k2.numerator * f2)
        d2 = math.ceil(k2.denominator * f2)
        
        marge = n1*n2/d1/d2
        if (marge > 1.1):
            print(str(n1)+'/'+str(d1)+' '+cur+'/'+c + ' ' + seller1)
            if (seller1 == name):
                print("MARKTFÜHRER VERKAUF")
            print(str(n2)+'/'+str(d2)+' '+c+'/'+cur + ' ' + seller2)
            if (seller2 == name):
                print("MARKTFÜHRER EINKAUF")
            print(str(round((marge-1)*100, 2))+"%")
        elif ((seller1 == name) and (seller2 == name)):
            print(str(n1)+'/'+str(d1)+' '+cur+'/'+c + ' ' + seller1)
            print(str(n2)+'/'+str(d2)+' '+c+'/'+cur + ' ' + seller2)
        print()
        

while(True):    
    trade('chaos', camount)
    trade('exa', eamount)
    wait(2 * len(currencies))
    print()
    print()
    print()
