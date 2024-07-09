from cards.cardTypes import RedCard

class Cafe(RedCard):
  def __init__(self):
    super().__init__()
    self.title = "Cafe"
    self.description = "Take 1 coin from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.cost = 2
    self.triggers.extend([3])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))

class FamilyRestaurant(RedCard):
  def __init__(self):
    super().__init__()
    self.title = "Family Restaurant"
    self.description = "Take 2 coins from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.cost = 3
    self.triggers.extend([9, 10])

  def activate(self, dice):
    print(self.title + ": triggered on Dice roll: " + str(dice))