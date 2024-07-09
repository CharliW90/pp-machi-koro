from cards.cardTypes import PurpleCard

class Stadium(PurpleCard):
  def __init__(self):
    super().__init__()
    self.title = "Stadium"
    self.description = "Take 2 coins from eachopponent.\n(your turn only)"
    self.industry = "major"
    self.cost = 6

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class TVStation(PurpleCard):
  def __init__(self):
    super().__init__()
    self.title = "TV Station"
    self.description = "Take 5 coins from an opponent.\n(your turn only)"
    self.industry = "major"
    self.cost = 7

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class BusinessCentre(PurpleCard):
  def __init__(self):
    super().__init__()
    self.title = "Business Centre"
    self.description = "Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only)"
    self.industry = "major"
    self.cost = 8

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))