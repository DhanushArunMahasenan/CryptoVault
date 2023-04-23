import requests
import time

#Will create a new record file if it does not already exist
file = open("record.txt", "a")
file.close()

#Required for API
url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
headers = {'X-CoinAPI-Key' : 'BB37B983-7254-4CA5-BC64-138C4F91ED86'}


class Trader:
    
    def __init__(self):
        if open("record.txt", "r").read() == "":
            self.portfolio = {"balance" : 100000,
            "crypto" : [{"name" : "BTC", "quantity": 0, "average price": 0, "selling price": 0, "profit": 0}, 
                    {"name" : "ETH", "quantity": 0, "average price": 0, "selling price": 0, "profit": 0}]}
        else:
            self.portfolio = dict(open("record.txt", "r").read())
    
    def updatePortfolio(self, latestPortfolio):
        currentPortfolio = open("record.txt", "w")
        currentPortfolio.write(str(latestPortfolio))
        currentPortfolio.close()

        self.portfolio = latestPortfolio


    def getExchangeRate(self, cryptoName):
        url = f'https://rest.coinapi.io/v1/exchangerate/{cryptoName}/USD'
        response = requests.get(url, headers=headers)
        data = response.json()
        rate = round(data["rate"], 2)

        return rate

    def buyCrypto(self, name, quantity):
        currentPrice = self.getExchangeRate(name)
        print(self.getCurrentPortfolio()["balance"])
        
        if currentPrice * quantity <= self.getCurrentPortfolio()["balance"]:
            self.getCurrentPortfolio()["balance"] -= currentPrice * quantity
        
        else:
            print("Error: Insufficent funds for transaction")

        latestPortfolio = {"balance": self.getCurrentPortfolio()["balance"] - currentPrice * quantity, "crypto": [{"name" : name, "quantity": quantity, "average price": 0, "selling price": 0, "profit": 0}]}
        
        self.updatePortfolio(latestPortfolio)
                
        return self.portfolio

    def sellCrypto(self, name, quantity):        
        currentPrice = self.getExchangeRate(name)
        self.balance += currentPrice * quantity
        
        for i in self.getCurrentPortfolio():
            if i["name"] == name:
                if quantity > i["quantity"]:
                    print("Error: Selling more cryptocurrency than avaliable")
                    return 
                
                i["quantity"] -= quantity
                i["profit"] = (currentPrice - i["average price"]) * quantity
                if i["quantity"] == 0:
                    i["average price"] = 0
        
        print(self.portfolio) 
    
    def getCurrentPortfolio(self):
        portfolio = open("record.txt", "r")
        currentPortfolio = portfolio.read()
        if currentPortfolio == "":
            return self.portfolio
        #currentPortfolio = dict(currentPortfolio)
        return currentPortfolio

test = Trader()

while True:
    print("\n-----Menu-----")
    option = input("Enter 1 to see exchange rates\nEnter 2 to buy cryptocurrency\nEnter 3 to sell cryptocurrency\nEnter 4 to view your portfolio\nEnter 5 to exit the program.")
    
    if option == "1":
        name = input("Enter then name of the cryptocurrency to get the exchange rate: ")
        print(test.getExchangeRate(name))
    
    if option == "2":
        cryptoToBuy = input("Would you like to buy bitcoin or ethereum: ")
        
        buyQuantity = int(input(f"How many {cryptoToBuy} would you like to purchase: "))
        portfolio = test.buyCrypto(cryptoToBuy, buyQuantity)

    if option == "3":
        cryptoToSell = input("Would you like to sell bitcoin or ethereum: ")
        cryptoSellQuantity = input(f"How many {cryptoToSell} would you like to sell: ")
        
        test.sellCrypto(cryptoToSell, cryptoSellQuantity)
    
    if option == "4":
        print(test.getCurrentPortfolio())