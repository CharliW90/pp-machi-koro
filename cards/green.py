from cards.cardTypes import GreenCard

class Bakery(GreenCard):
  def __init__(self):
    super().__init__()
    self.title = "Bakery"
    self.description = "Get 1 coin from the bank.\n(your turn only)"
    self.industry = "store"
    self.cost = 1
    self.triggers.extend([2, 3])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class ConvenienceStore(GreenCard):
  def __init__(self):
    super().__init__()
    self.title = "Convenience Store"
    self.description = "Get 3 coins from the bank.\n(your turn only)"
    self.industry = "store"
    self.cost = 2
    self.triggers.extend([4])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class CheeseFactory(GreenCard):
  def __init__(self):
    super().__init__()
    self.title = "Cheese Factory"
    self.description = "Get 3 coins from the bank for each farm establishment you own.\n(your turn only)"
    self.industry = "factory"
    self.cost = 5
    self.triggers.extend([7])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class FurnitureFactory(GreenCard):
  def __init__(self):
    super().__init__()
    self.title = "Furniture Factory"
    self.description = "Get 3 coins from the bank for each industrial establishment you own.\n(your turn only)"
    self.industry = "factory"
    self.cost = 3
    self.triggers.extend([8])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class FarmersMarket(GreenCard):
  def __init__(self):
    super().__init__()
    self.title = "Farmers Market"
    self.description = "Get 2 coins from the bank for each field establishment you own.\n(your turn only)"
    self.industry = "market"
    self.cost = 2
    self.triggers.extend([11, 12])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))