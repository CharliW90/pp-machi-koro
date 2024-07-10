from cards.blue import *
from cards.green import *
from cards.red import *
from cards.purple import *
from cards.landmark import *

class CardStacks:
  def __init__(self):
    self.wheatFields = []
    self.ranches = []
    self.bakeries = []
    self.cafes = []
    self.convenienceStores = []
    self.forests = []
    self.majorEstablishments = []
    self.cheeseFactories = []
    self.furnitureFactories = []
    self.mines = []
    self.familyRestaurants = []
    self.appleOrchards = []
    self.farmersMarkets = []

  def add(self, card):
    pile = lookup(card.title)
    self[pile].append(card)
    print(f"Added {card.name} to the {pile or 'major establishments'} pile - there are now {len(self[pile])} cards in this pile")
    return len(self[pile])
  
  def remove(self, name):
    pile = lookup(name)
    card = self[pile].pop()
    print(f"Removed {card.name} from the {pile} pile - there are now {len(self[pile])} cards in this pile")
    return card

class Deck(CardStacks):
  def __init__(self, playerCount):
    super().__init__()
    self.playerCount = playerCount

  def initialise(self):
    cards = startingDeck(self.playerCount)
    for card in cards:
      pile = lookup(card.title)
      stack = getattr(self, pile)
      stack.append(card)
  
  def contents(self, cash = 100):
    allCards = []
    if len(self.wheatFields) > 0:
      card = self.wheatFields[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.wheatFields)}",
        ])
    if len(self.ranches) > 0:
      card = self.ranches[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.ranches)}",
        ])
    if len(self.bakeries) > 0:
      card = self.bakeries[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.bakeries)}",
        ])
    if len(self.cafes) > 0:
      card = self.cafes[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.cafes)}",
        ])
    if len(self.convenienceStores) > 0:
      card = self.convenienceStores[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.convenienceStores)}",
        ])
    if len(self.forests) > 0:
      card = self.forests[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.forests)}",
        ])
    if len(self.majorEstablishments) > 0:
      stadiums = []
      tvStations = []
      businessCentres = []
      for card in self.majorEstablishments:
        if card.title == "Stadium":
          stadiums.append(card)
        if card.title == "TV Station":
          tvStations.append(card)
        if card.title == "Business Centre":
          businessCentres.append(card)
      if len(stadiums) > 0:
        card = stadiums[0]
        plural = "s" if card.cost > 1 else ""
        style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
        reset = "\x1b[0m"
        allCards.append([
          f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
          f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
          f"{style}{card.cost} coin{plural}{reset}",
          f"Qty: {len(stadiums)}",
          ])
      if len(tvStations) > 0:
        card = tvStations[0]
        plural = "s" if card.cost > 1 else ""
        style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
        reset = "\x1b[0m"
        allCards.append([
          f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
          f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
          f"{style}{card.cost} coin{plural}{reset}",
          f"Qty: {len(tvStations)}",
          ])
      if len(businessCentres) > 0:
        card = businessCentres[0]
        plural = "s" if card.cost > 1 else ""
        style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
        reset = "\x1b[0m"
        allCards.append([
          f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
          f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
          f"{style}{card.cost} coin{plural}{reset}",
          f"Qty: {len(businessCentres)}",
          ])
    if len(self.furnitureFactories) > 0:
      card = self.furnitureFactories[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.furnitureFactories)}",
        ])
    if len(self.mines) > 0:
      card = self.mines[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.mines)}",
        ])
    if len(self.familyRestaurants) > 0:
      card = self.familyRestaurants[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.familyRestaurants)}",
        ])
    if len(self.appleOrchards) > 0:
      card = self.appleOrchards[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.appleOrchards)}",
        ])
    if len(self.farmersMarkets) > 0:
      card = self.farmersMarkets[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{plural}{reset}",
        f"Qty: {len(self.farmersMarkets)}",
        ])
    return allCards

class Hand():
  def __init__(self):
    self.blue = [WheatField()]
    self.green = [Bakery()]
    self.red = []
    self.purple = []
    self.landmarks = [TrainStation(), ShoppingMall(), AmusementPark(), RadioTower()]
  
  def add(self, card):
    stack = getattr(self, card.colour)
    stack.append(card)
  
  def remove(self, colour, name):
    stack = getattr(self, colour)
    for card, i in enumerate(stack):
      if card.name == name:
        stack.pop(i)
        return card
    return ValueError(f"No {name} card")

def lookup(name):
  match name:
    case "Wheat Field":
      return "wheatFields"
    case "Ranch":
      return "ranches"
    case "Bakery":
      return "bakeries"
    case "Cafe":
      return "cafes"
    case "Convenience Store":
      return "convenienceStores"
    case "Forest":
      return "forests"
    case "Stadium" | "TV Station" | "Business Centre": 
      return "majorEstablishments"
    case "Cheese Factory":
      return "cheeseFactories"
    case "Furniture Factory":
      return "furnitureFactories"
    case "Mine":
      return "mines"
    case "Family Restaurant":
      return "familyRestaurants"
    case "Apple Orchard":
      return "appleOrchards"
    case "Farmers Market":
      return "farmersMarkets"
    case _:
      print(f"Error: {name} is not one of the expected names")
      return

def startingDeck(playerCount):
  cards = []
  for x in range(6):
    cards.append(WheatField())
    cards.append(Ranch())
    cards.append(Bakery())
    cards.append(Cafe())
    cards.append(ConvenienceStore())
    cards.append(Forest())
    cards.append(CheeseFactory())
    cards.append(FurnitureFactory())
    cards.append(Mine())
    cards.append(FamilyRestaurant())
    cards.append(AppleOrchard())
    cards.append(FarmersMarket())
  for x in range(playerCount):
    cards.append(Stadium())
    cards.append(TVStation())
    cards.append(BusinessCentre())
  return cards