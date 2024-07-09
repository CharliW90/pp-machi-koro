class One:
  def __init__(self):
    self.value = 1
    self.colour = "Copper"

class Five:
  def __init__(self):
    self.value = 5
    self.colour = "Silver"

class Ten:
  def __init__(self):
    self.value = 10
    self.colour = "Gold"

class CoinPiles:
  def __init__(self, coppers, silvers, golds):
    self.coppers = []
    for copper in range(coppers):
      self.coppers.append(One())
    self.silvers = []
    for silver in range(silvers):
      self.silvers.append(Five())
    self.golds = []
    for gold in range(golds):
      self.golds.append(Ten())
  
  def total(self):
    coppers = 0
    silvers = 0
    golds = 0
    for coin in self.coppers:
      coppers += coin.value
    for coin in self.silvers:
      silvers += coin.value
    for coin in self.golds:
      golds += coin.value
    return coppers + silvers + golds