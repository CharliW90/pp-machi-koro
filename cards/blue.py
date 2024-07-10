from cards.cardTypes import BlueCard

class WheatField(BlueCard):
  def __init__(self):
    super().__init__()
    self.title = "Wheat Field"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.cost = 1
    self.zIndex = 0
    self.triggers.extend([1])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Ranch(BlueCard):
  def __init__(self):
    super().__init__()
    self.title = "Ranch"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "farm"
    self.cost = 1
    self.zIndex = 1
    self.triggers.extend([2])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Forest(BlueCard):
  def __init__(self):
    super().__init__()
    self.title = "Forest"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.cost = 3
    self.zIndex = 5
    self.triggers.extend([5])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class Mine(BlueCard):
  def __init__(self):
    super().__init__()
    self.title = "Mine"
    self.description = "Get 5 coins from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.cost = 6
    self.zIndex = 11
    self.triggers.extend([9])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class AppleOrchard(BlueCard):
  def __init__(self):
    super().__init__()
    self.title = "Apple Orchard"
    self.description = "Get 3 coins from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.cost = 3
    self.zIndex = 13
    self.triggers.extend([10])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))
