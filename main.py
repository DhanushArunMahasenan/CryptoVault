import requests
import time


url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
headers = {'X-CoinAPI-Key' : 'BB37B983-7254-4CA5-BC64-138C4F91ED86'}

class Trader:
    
    def __init__(self):
        self.balance = 100000
        self.portfolio = [{"name" : "BTC", "quantity": 0, "average price": 0, "selling price": 0, "profit": 0, "balance": 100000}, 
                    {"name" : "ETH", "quantity": 0, "average price": 0, "selling price": 0, "profit": 0}]
    
    def getExchangeRate(self, cryptoName):
        url = f'https://rest.coinapi.io/v1/exchangerate/{cryptoName}/USD'
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print(data)

        rate = round(data["rate"], 2)
        return rate

    def buyCrypto(self, name, quantity):
        currentPrice = self.getExchangeRate(name)
        
        if currentPrice * quantity <= self.balance:
            self.balance -= currentPrice * quantity
        
        else:
            print("Error: Insufficent funds for transaction")
        
        for i in self.getCurrentPortfolio():
            if i["name"] == name:
                i["quantity"] = quantity
                i["average price"] = currentPrice
                i["balance"] = self.getBalance() - currentPrice * quantity
                
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
        try:
            portfolio = open("record.txt", "r")
            currentPortfolio = portfolio.read()
            #currentPortfolio = dict(currentPortfolio)
            return currentPortfolio
        
        except Exception as e:
            print(e)
            print("No historial transactions found.")
            return self.portfolio
    
    def getBalance(self):
        portfolio = self.getCurrentPortfolio()
        portfolio = dict(portfolio)
        
        balance = portfolio[0]["balance"]
        
        return balance

test = Trader()

while True:
    option = input("Enter 1 to see exchange rates, enter 2 to buy cryptocurrency, 3 to sell cryptocurrency, 4 to view your portfolio, and enter 5 to exit the program.")
    
    if option == "1":
        name = input("Enter then name of the cryptocurrency to get the exchange rate: ")
        print(test.getExchangeRate(name))
    
    if option == "2":
        cryptoToBuy = input("Would you like to buy bitcoin or ethereum: ")
        
        buyQuantity = int(input(f"How many {cryptoToBuy} would you like to purchase: "))
        portfolio = test.buyCrypto(cryptoToBuy, buyQuantity)
        file = open("record.txt", "w")
        file.write(str(portfolio))
        file.close()

    if option == "3":
        cryptoToSell = input("Would you like to sell bitcoin or ethereum: ")
        cryptoSellQuantity = input(f"How many {cryptoToSell} would you like to sell: ")
        
        test.sellCrypto(cryptoToSell, cryptoSellQuantity)
    
    if option == "4":
        print(test.getCurrentPortfolio())