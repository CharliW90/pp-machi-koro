from collections import Counter
from coins.coinage import *
from coins.transactions import *

class Bank:
  def __init__(self):
    self.name = "The Bank"
    self.coins = CoinPiles(42, 24, 12)
    self.total = 282
    
  def __repr__(self):
    self.updateTotal()
    output = (
    f"{self.name} contains {self.total} in coinage:\n"
    f"{len(self.coins.coppers)} Copper Ones, valuing {sum([coin.value for coin in self.coins.coppers])}\n"
    f"{len(self.coins.silvers)} Silver Fives, valuing {sum([coin.value for coin in self.coins.silvers])}\n"
    f"{len(self.coins.golds)} Gold Tens, valuing {sum([coin.value for coin in self.coins.golds])}"
    )
    return output

  def updateTotal(self):
    self.total = self.coins.total()

  def givePlayer(self, total):
    return giving(self, total)

  def takePayment(self, coins, totalToPay):
    payment = receiving(self, coins) # put payment into bank's coin pile
    print(f"{self.name} received {payment} towards {totalToPay} requested.")
    self.updateTotal()
    return giving(self, payment-totalToPay) # give change, if any

  def exchange(self, coins):
    intake = receiving(self, coins) # put all coins into the bank's coin pile
    return givePlayer(self, intake) # give back the same value in coins, starting with highest denomination

