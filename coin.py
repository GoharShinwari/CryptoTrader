import coinmarketcapapi
import time
import json
import os
import key
from twython import Twython, TwythonError
import key

# Initialize Twython with the API key
apiKey = key.api_key
twitter = Twython(apiKey)

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

def displayBank():
    global bankBalance
    roundedBankBalance = round(bankBalance, 2)  
    print(f"Your Bank Balance is: ${roundedBankBalance}.")
    
def displayBTCBalance():
    global btcBalance
    btcBalanceUSD = convertToUSD_BTC(btcBalance)
    formattedBTCBalance = '{:.8f}'.format(btcBalance) 
    print(f"Your BTC Balance is: {formattedBTCBalance}. (${round(btcBalanceUSD, 2)})")

def displayETHBalance():
    global ethBalance
    ethBalanceUSD = convertToUSD_ETH(ethBalance)
    formattedETHBalance = '{:.8f}'.format(ethBalance)
    print(f"Your ETH Balance is: {formattedETHBalance}. (${round(ethBalanceUSD, 2)})")

def convertToBTC(amount):
    btc_amount = amount / btcPrice
    return btc_amount

def convertToETH(amount):
    eth_amount = amount / ethPrice
    return eth_amount

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

    if decision == 'Y' and bankBalance >= amount:
        btc_amount = convertToBTC(amount)
        if btc_amount > -1:
            bankBalance -= amount
            btcBalance += btc_amount
            ## btcSupply -= btc_amount
            print(f"Successfully bought {round(btc_amount, 8)} BTC.")
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
         
    if decision == 'Y' and bankBalance >= amount:
        eth_amount = convertToETH(amount)
        if eth_amount > -1:
            bankBalance -= amount
            ethBalance += eth_amount
            ## ethSupply -= eth_amount
            print(f"Successfully bought {round(eth_amount, 8)} ETH.")
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
        print(f"Successfully sold {round(btcAmount, 8)} BTC for {round(amountUSDSold, 2)} USD.")
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
        print(f"Successfully sold {round(ethAmount, 8)} ETH for {round(amountUSDSold, 2)} USD.")
        print("")
        saveData()
        return amountUSDSold
    else:
        print("Cannot sell ETH at this time or insufficient ETH balance.")
        print("")

print("*****************************")
print("Welcome to CryptoTrader")
print("*****************************")
while (open):
    apiKey = apiKey
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
    print("If you would like to refresh prices, skip all.")
    print("The current price of BTC is: " + str(round(btcPrice, 3)))
    print("The current price of ETH is: " + str(round(ethPrice, 3)))
    print("")

    
    print("")
    decision = input("Would you like to buy BTC? (Y/N): ")
    if decision == "Y":
        amount = float(input("How much BTC do you want to buy? ($): "))
        buyBTC(amount)

    decision = input("Would you like to buy ETH? (Y/N): ")
    if decision == "Y":
        amount = float(input("How much ETH do you want to buy? ($): "))
        buyETH(amount)

    decision = input("Would you like to sell BTC? (Y/N): ")
    if decision == "Y":
        amount = float(input("How much BTC do you want to sell? ($): "))
        sellBTC(amount)

    decision = input("Would you like to sell ETH? (Y/N): ")
    if decision == "Y":
        amount = float(input("How much ETH do you want to sell? ($): "))
        sellETH(amount)

    time.sleep(5) 
saveData()