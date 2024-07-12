import time
from cards.cardTypes import BlueCard

class WheatField(BlueCard):
  cost = 1
  zIndex = 0

  def __init__(self):
    super().__init__()
    self.title = "Wheat Field"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.triggers = [1]

  def activate(self, dice):
    time.sleep(0.2)
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Ranch(BlueCard):
  cost = 1
  zIndex = 1

  def __init__(self):
    super().__init__()
    self.title = "Ranch"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "farm"
    self.triggers = [2]

  def activate(self, dice):
    time.sleep(0.2)
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Forest(BlueCard):
  cost = 3
  zIndex = 5
  
  def __init__(self):
    super().__init__()
    self.title = "Forest"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.triggers = [5]

  def activate(self, dice):
    time.sleep(0.2)
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Mine(BlueCard):
  cost = 6
  zIndex = 11

  def __init__(self):
    super().__init__()
    self.title = "Mine"
    self.description = "Get 5 coins from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.triggers = [9]

  def activate(self, dice):
    time.sleep(0.2)
    print(self.title + ": triggered on Dice roll: " + str(dice))

class AppleOrchard(BlueCard):
  cost = 3
  zIndex = 13
  
  def __init__(self):
    super().__init__()
    self.title = "Apple Orchard"
    self.description = "Get 3 coins from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.triggers = [10]

  def activate(self, dice):
    time.sleep(0.2)
    print(self.title + ": triggered on Dice roll: " + str(dice))
