from reference import reference
from coins.coinage import CoinPiles
from coins.transactions import giving, receiving

class Bank:
  def __init__(self):
    self.name = "The Bank"
    self.colour = 'cyan'
    self.colorize = reference['ansiColours'][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.coins = CoinPiles(24, 24, 12)
    self.total = 282
    
  def __str__(self):
    self.updateTotal()
    output = (
    f"{self.name} contains {self.total} in coinage:\n"
    f"{len(self.coins.coppers)} Copper Ones, valuing {sum([coin.value for coin in self.coins.coppers])}\n"
    f"{len(self.coins.silvers)} Silver Fives, valuing {sum([coin.value for coin in self.coins.silvers])}\n"
    f"{len(self.coins.golds)} Gold Tens, valuing {sum([coin.value for coin in self.coins.golds])}"
    )
    return output
  
  def declareAction(self, str):
    print(f"{self.colorize}{str}{self.reset}")

  def updateTotal(self):
    self.total = self.coins.total()

  def givePlayer(self, total):
    return giving(self, total)

  def takePayment(self, coins, totalToPay):
    payment = receiving(self, coins) # put payment into bank's coin pile
    self.updateTotal()
    return giving(self, payment-totalToPay) # give change, if any

  def check(self, game):
    ones = len(self.coins.coppers)
    fives = len(self.coins.silvers)
    if ones < 5 or fives < 2:
      if ones < 5:
        self.declareAction(f"{self.name} has {ones} copper One coins remaining - exchanging up with players...")
      elif fives < 2:
        self.declareAction(f"{self.name} has {fives} silver Five coins remaining - exchanging up with players...")
      for player in game.players:
        print(len(player.coins.coppers), len(player.coins.silvers), len(player.coins.golds))
        coins = player.giveAll()
        player.receive(self.exchange(coins))
        print(len(player.coins.coppers), len(player.coins.silvers), len(player.coins.golds))

  def exchange(self, coins):
    intake = receiving(self, coins) # put all coins into the bank's coin pile
    return self.givePlayer(intake) # give back the same value in coins, starting with highest denomination

