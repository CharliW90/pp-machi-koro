from cards.cardTypes import LandmarkCard

class TrainStation(LandmarkCard):
  def __init__(self):
    super().__init__()
    self.title = "Train Station"
    self.description = "You may roll 1 or 2 dice."
    self.cost = 4

  def ability(self):
    return "doubleDice"


class ShoppingMall(LandmarkCard):
  def __init__(self):
    super().__init__()
    self.title = "Shopping Mall"
    self.description = "Your Restaurant and Store establishments earn +1 coin each when activated."
    self.cost = 10
    
  def ability(self):
    return "plusOne"


class AmusementPark(LandmarkCard):
  def __init__(self):
    super().__init__()
    self.title = "Amusement Park"
    self.description = "If you roll a double, take another turn after this one."
    self.cost = 16
  
  def ability(self):
    return "doubleTurns"


class RadioTower(LandmarkCard):
  def __init__(self):
    super().__init__()
    self.title = "Radio Tower"
    self.description = "Once per turn, you may choose to reroll the dice."
    self.cost = 22
  
  def ability(self):
    return "reRolls"
  
class Abilities():
  def __init__(self):
    self.doubleDice = False
    self.plusOne = False
    self.doubleTurns = False
    self.reRolls = False