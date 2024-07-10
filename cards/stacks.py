from collections import Counter
from cards.blue import *
from cards.green import *
from cards.red import *
from cards.purple import *
from cards.landmark import *

class Deck:
  def __init__(self, playerCount):
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
    self.playerCount = playerCount

  def initialise(self):
    cards = startingDeck(self.playerCount)
    for card in cards:
      pile = lookup(card.title)
      stack = getattr(self, str(pile))
      stack.append(card)
  
  def contents(self, cash = 100):
    allCards = []
    cardStacks = []
    for attribute in dir(self):
      actual = getattr(self, attribute)
      if isinstance(actual, list):
        cardStacks.append(actual)
    cardCounts = []
    for stack in cardStacks:
      counts = Counter(card.title for card in stack)
      cardCounts.extend([title, count] for title, count in counts.items())
    for [title, qty] in cardCounts:
      cards = getattr(self, str(lookup(title)))
      card = cards[0]
      plural = "s" if card.cost > 1 else ""
      style = "\x1b[9;2m" if card.cost > cash else "\x1b[3;32m"
      reset = "\x1b[0m"
      allCards.append([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{card.colorize}{card.title}{card.reset}\n{style}{card.cost} coin{plural}{reset}",
        f"Qty: {qty}",
        ])
    return allCards

  def add(self, card):
    pile = lookup(card.title)
    stack = getattr(self, str(pile))
    stack.append(card)
    print(f"Added {card.title} to the {pile or 'major establishments'} pile - there are now {len(stack)} cards in this pile")
    return len(stack)
  
  def remove(self, name):
    pile = lookup(name)
    stack = getattr(self, str(pile))
    card = stack.pop()
    print(f"Removed {card.title} from the {pile} pile - there are now {len(stack)} cards in this pile")
    return card

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
    for i, card in enumerate(stack):
      if card.title == name:
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