import requests
import time

# Will create a new record file if it does not already exist
file = open("record.txt", "a")
file.close()

# Required for API
url = 'https://rest.coinapi.io/v1/exchangerate/ETH/USD'
headers = {'X-CoinAPI-Key': 'BB37B983-7254-4CA5-BC64-138C4F91ED86'}


class Trader:

    def __init__(self):

        self.portfolio = {"balance": 100000,
        "crypto": {"BTC": {"quantity": 0, "average price": 0, "selling price": 0, "profit": 0}, 
                           "ETH": {"quantity": 0, "average price": 0, "selling price": 0, "profit": 0}}}
        self.login()

    def login(self):
        file = open("record.txt", "r")
        portfolio = file.read()

        # data is present in portfolio
        if portfolio != "":
            self.portfolio = eval(portfolio)

    def updatePortfolio(self):
        currentPortfolio = open("record.txt", "w")
        currentPortfolio.write(str(self.portfolio))
        currentPortfolio.close()

    def getExchangeRate(self, cryptoName):
        url = f'https://rest.coinapi.io/v1/exchangerate/{cryptoName}/USD'
        response = requests.get(url, headers=headers)
        data = response.json()
        rate = round(data["rate"], 2)

        return rate

    def buyCrypto(self, name, quantity):
        currentPrice = self.getExchangeRate(name)
        print(self.portfolio["balance"])

        if currentPrice * quantity <= self.portfolio["balance"]:
            self.portfolio["balance"] -= currentPrice * quantity
            #To do: Handle average price
            self.portfolio["crypto"][name]["quantity"] += quantity
            self.portfolio["crypto"][name]["average price"] = currentPrice
            self.updatePortfolio()

        else:
            print("Error: Insufficent funds for transaction")

        return self.portfolio

    def sellCrypto(self, name, quantity):
        currentPrice = self.getExchangeRate(name)

        if self.portfolio["crypto"][name]["quantity"] >=  quantity:
            self.portfolio["crypto"][name]["quantity"] -= quantity
            #To Do: Handle average price
            self.portfolio["crypto"][name]["selling price"] = currentPrice
            self.portfolio["crypto"][name]["profit"] = (currentPrice - self.portfolio["crypto"][name]["average price"]) * quantity
            self.updatePortfolio()
        
        else:
            print("Error: Trying to sell more crypto currency than avaliable.")

        print(self.portfolio)


test = Trader()

while True:
    print("\n-----Menu-----")
    option = input("Enter 1 to see exchange rates\nEnter 2 to buy cryptocurrency\nEnter 3 to sell cryptocurrency\nEnter 4 to view your portfolio\nEnter 5 to exit the program.")

    if option == "1":
        name = input(
            "Enter then name of the cryptocurrency to get the exchange rate(BTC or ETH): ").upper()
        print(test.getExchangeRate(name))

    elif option == "2":
        cryptoToBuy = input("Would you like to buy bitcoin(BTC) or ethereum(ETH): ").upper()

        buyQuantity=int(
            input(f"How many {cryptoToBuy} would you like to purchase: "))
        portfolio=test.buyCrypto(cryptoToBuy, buyQuantity)

    elif option == "3":
        cryptoToSell=input("Would you like to sell bitcoin(BTC) or ethereum(ETH): ").upper()
        cryptoSellQuantity= int(input(
            f"How many {cryptoToSell} would you like to sell: "))

        test.sellCrypto(cryptoToSell, cryptoSellQuantity)

    elif option == "4":
        print(test.portfolio)

    elif option == "5":
        break

    else:
        print("Invalid input")