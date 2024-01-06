import coinmarketcapapi
import time
import json
import os
import key
from twython import Twython, TwythonError

apiKey = Twython(key.api_key)

def initializeBankData():
    if not os.path.exists('bank.json') or os.path.getsize('bank.json') == 0:
        default_data = {
            'bankBalance': 10000,
            'btcBalance': 0,
            'ethBalance': 0
        }
        with open('bank.json', 'w') as file:
            json.dump(default_data, file)

initializeBankData()

with open('bank.json', 'r') as file:
    data = json.load(file)
    bankBalance = data['bankBalance']
    btcBalance = data['btcBalance']
    ethBalance = data['ethBalance']

def saveData():
    data = {
        'bankBalance': bankBalance,
        'btcBalance': btcBalance,
        'ethBalance': ethBalance
    }
    with open('bank.json', 'w') as file:
        json.dump(data, file)

def roundPrice(price):
    return round(price, 4)

def displayBank():
    global bankBalance
    print(f"Your Bank Balance is: {bankBalance}.")
    
def displayBTCBalance():
    global btcBalance
    print(f"Your BTC Balance is: {btcBalance}. (${roundPrice(convertToUSD_BTC(btcBalance))})")
    
def displayETHBalance():
    global ethBalance
    print(f"Your ETH Balance is: {ethBalance}. (${roundPrice(convertToUSD_ETH(ethBalance))})")

def convertToBTC(amount):
    btc_amount = amount / btcPrice
    return roundPrice(btc_amount)

def convertToETH(amount):
    eth_amount = amount / ethPrice
    return roundPrice(eth_amount)

def convertToUSD_BTC(BTC):
    USD = BTC * btcPrice
    return USD

def convertToUSD_ETH(ETH):
    USD = ETH * ethPrice
    return USD

## add bitcoin supply here
def buyBTC(amount):
    global bankBalance
    global btcBalance

    if decision == 'Y' and bankBalance > amount:
        btc_amount = convertToBTC(amount)
        if btc_amount > -1:
            bankBalance -= amount
            btcBalance += btc_amount
            ## btcSupply -= btc_amount
            print(f"Successfully bought {btc_amount} BTC.")
            print("")
            saveData() 
        else:
            print("")
            print("Insufficient BTC supply available.")
    else: 
        print("Cannot buy BTC at this time.")
        print("")

def buyETH(amount):   
    global bankBalance
    global ethBalance
         
    if decision == 'Y' and bankBalance > amount:
        eth_amount = convertToETH(amount)
        if eth_amount > -1:
            bankBalance -= amount
            ethBalance += eth_amount
            ## ethSupply -= eth_amount
            print(f"Successfully bought {eth_amount} ETH.")
            print("")
            saveData()
        else:
            print("")
            print("Insufficient ETH supply available.")
    else: 
        print("Cannot buy ETH at this time.")
        print("")

def sellBTC(amountUSD):
    global bankBalance
    global btcBalance

    btcAmount = convertToBTC(amountUSD)
    
    if decision == 'Y' and btcBalance >= btcAmount:
        bankBalance += btcAmount * btcPrice
        btcBalance -= btcAmount
        amountUSDSold = btcAmount * btcPrice
        print(f"Successfully sold {btcAmount} BTC for {amountUSDSold} USD.")
        print("")
        saveData()
        return amountUSDSold
    else:
        print("Cannot sell BTC at this time or insufficient BTC balance.")
        print("")

def sellETH(amountUSD):
    global bankBalance
    global ethBalance

    ethAmount = convertToETH(amountUSD)
    
    if decision == 'Y' and ethBalance >= ethAmount:
        bankBalance += ethAmount * ethPrice
        ethBalance -= ethAmount
        amountUSDSold = ethAmount * ethPrice
        print(f"Successfully sold {ethAmount} ETH for {amountUSDSold} USD.")
        print("")
        saveData()
        return amountUSDSold
    else:
        print("Cannot sell ETH at this time or insufficient ETH balance.")
        print("")

placeHolder = True
print("*****************************")
print("Welcome to CryptoTrader")
print("*****************************")
while (placeHolder):
    apiKey = '1a5f0d93-e8eb-4195-bdb9-5ff5fc35cae4' 
    cmcClient = coinmarketcapapi.CoinMarketCapAPI(apiKey)

    btcResponse = cmcClient.tools_priceconversion(amount = 1, symbol = 'BTC', convert = 'USD')
    btcData=btcResponse.data
    btcInfo = cmcClient.cryptocurrency_info(symbol='BTC')
    btcPrice = btcData[0]['quote']['USD']['price']

    ethReponse = cmcClient.tools_priceconversion(amount=1, symbol='ETH', convert='USD')
    ethData = ethReponse.data
    ethInfo = cmcClient.cryptocurrency_info(symbol='ETH')
    ethPrice = ethData[0]['quote']['USD']['price']
    
    print("")
    displayBank()
    displayBTCBalance()
    displayETHBalance()
    print("")
    
    print("If you would like to refresh prices, skip all. To exit enter X")
    print("The current price of BTC is: "+str(roundPrice(btcPrice)))
    print("The current price of BTC is: "+str(roundPrice(ethPrice)))
    
    print("")
    decision = input("Would you like to buy BTC? (Y/N): ")
    if decision == "Y": 
        amount = int(input("How much BTC do you wanna buy? ($): "))
        buyBTC(amount)
        
    decision = input("Would you like to buy ETH? (Y/N): ")
    if decision == "Y": 
        amount = int(input("How much ETH do you wanna buy? ($): "))
        buyETH(amount)
            
    decision = input("Would you like to sell BTC? (Y/N): ")
    if decision == "Y": 
        amount = int(input("How much BTC do you wanna sell? ($): "))
        sellBTC(amount)
               
    decision = input("Would you like to sell ETH? (Y/N): ")
    if decision == "Y": 
        amount = int(input("How much ETH do you wanna sell? ($): "))
        sellETH(amount)
    if decision == "X":
        placeHolder = False
        
    time.sleep(5)
saveData()