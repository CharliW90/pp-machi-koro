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
    self._index = 0
  
  def __iter__(self):
    return self
  
  def __next__(self):
    sequence = [self.coppers, self.silvers, self.golds]
    if self._index < len(sequence):
      iteration = sequence[self._index]
      self._index += 1
      return iteration
    else:
      self._index = 0
      raise StopIteration

  def total(self):
    total = 0
    for stack in self:
      for coin in stack:
        total += coin.value
    return total