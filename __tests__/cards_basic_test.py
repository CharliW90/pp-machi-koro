import pytest
from unittest.mock import create_autospec
from reference import ansiColours
from player import Player
from cards.cardTypes import BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard
from cards.blue import *
from cards.green import *
from cards.red import *
from cards.purple import *
from cards.landmark import *
from game import Game

class MockPlayer(Player):
  def __init__(self):
    super().__init__('PlayerNameHere', 1)
    self.current = False
  
  def declareAction(self, x):
    print(x)

  def startTurn(self):
    self.current = True
  
  def endTurn(self):
    self.current = False

cardOrder = [
  "Wheat Field","Ranch","Bakery", "Cafe", "Convenience Store",
  "Forest", "Stadium", "TV Station", "Business Centre", "Cheese Factory",
  "Furniture Factory", "Mine", "Family Restaurant", "Apple Orchard", "Farmers Market",
  "Train Station", "Shopping Mall", "Amusement Park", "Radio Tower"
  ]

mockPlayer = MockPlayer()

mockGame = create_autospec(Game)

def mockActivation(game, diceRoll) -> None: # Mock the .activate() function of the card, to test that .trigger() calls this function
  print(f"Card Activated on a roll of {diceRoll}.")

def assessCardTriggers(card: BlueCard|GreenCard|RedCard|PurpleCard, name: str, triggers: list[int], capsys) -> None:
  """
  This function takes a card, and attempts to trigger it for every possible dice roll (1 to 12) and asserts that it will trigger on the correct triggers and will not trigger on other rolls.
  Also checks that the trigger calls the card's activate function by checking for the console output of the card's mocked activate function.
  """

  for n in range(12):
    mockPlayer.startTurn()    # player is now active player
    card.trigger(mockGame, mockPlayer, n)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()

    if n in triggers:
      if isinstance(card, BlueCard | GreenCard | PurpleCard):   # active player should have their Blue, Green or Purple cards trigger
        assert len(consoleLines) == 2
        assert consoleLines[0] == f"Triggered {name} for PlayerNameHere"    # print() statement from trigger()
        assert consoleLines[1] == f"Card Activated on a roll of {n}."       # print() statement from the card's mocked activate() function
    else:
      assert len(consoleLines) == 0

  for n in range(12):
    mockPlayer.endTurn()    # player is now not active player
    card.trigger(mockGame, mockPlayer, n)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()

    if n in triggers:
      if isinstance(card, BlueCard | RedCard):    # non-active players should have their Blue or Red cards trigger
        assert len(consoleLines) == 2
        assert consoleLines[0] == f"Triggered {name} for PlayerNameHere"
        assert consoleLines[1] == f"Card Activated on a roll of {n}."
    else:
      assert len(consoleLines) == 0

class TestBlueCards:
  def assessBlueCard(self, test: BlueCard) -> None:
    """
    Checks for the attributes and corresponding values that all Blue cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "blue"

    assert hasattr(test, 'colorize')
    assert test.colorize == ansiColours["blue"]

    assert hasattr(test, 'reset')
    assert test.reset == ansiColours["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Blue cards trigger for everyone, on everyone's turn."

    assert hasattr(test, 'cardType')
    assert test.cardType == "Primary"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_BlueTemplate(self, capsys):
    # Arrange
    testCard = BlueCard()

    # Act / Assert
    self.assessBlueCard(testCard)

    assert testCard.title == "A Blue card"
    assert testCard.description == "A template for cards that are Primary Industries"
    assert str(testCard) == f"{ansiColours['blue']}A Blue card{ansiColours['reset']}\n{ansiColours['blue']}A template for cards that are Primary Industries{ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    testCard.trigger(mockGame, mockPlayer, 1)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0
    with pytest.raises(RuntimeError) as error:
      testCard.activate(mockGame, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      consoleLines = captured.out.splitlines()
      assert len(consoleLines) == 2
      assert consoleLines[0] == f"This is {ansiColours['blue']}A Blue card{ansiColours['reset']}; {ansiColours['blue']}A template for cards that are Primary Industries{ansiColours['reset']}"
      assert consoleLines[1] == "it has not been used to create an actual card yet."

  def test_WheatField(self, capsys):
    # Arrange
    testCard = WheatField()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessBlueCard(testCard)
    assessCardTriggers(testCard, "Wheat Field", [1], capsys)

    assert testCard.cost == 1
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Wheat Field"
    assert testCard.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(testCard) == f"{ansiColours['blue']}Wheat Field{ansiColours['reset']}\n{ansiColours['blue']}Get 1 coin from the bank.\n(anyone's turn){ansiColours['reset']}"

  def test_Ranch(self, capsys):
    # Arrange
    testCard = Ranch()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessBlueCard(testCard)
    assessCardTriggers(testCard, "Ranch", [2], capsys)

    assert testCard.cost == 1
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Ranch"
    assert testCard.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(testCard) == f"{ansiColours['blue']}Ranch{ansiColours['reset']}\n{ansiColours['blue']}Get 1 coin from the bank.\n(anyone's turn){ansiColours['reset']}"

  def test_Forest(self, capsys):
    # Arrange
    testCard = Forest()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessBlueCard(testCard)
    assessCardTriggers(testCard, "Forest", [5], capsys)

    assert testCard.cost == 3
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Forest"
    assert testCard.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(testCard) == f"{ansiColours['blue']}Forest{ansiColours['reset']}\n{ansiColours['blue']}Get 1 coin from the bank.\n(anyone's turn){ansiColours['reset']}"

  def test_Mine(self, capsys):
    # Arrange
    testCard = Mine()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessBlueCard(testCard)
    assessCardTriggers(testCard, "Mine", [9], capsys)

    assert testCard.cost == 6
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Mine"
    assert testCard.description == "Get 5 coins from the bank.\n(anyone's turn)"
    assert str(testCard) == f"{ansiColours['blue']}Mine{ansiColours['reset']}\n{ansiColours['blue']}Get 5 coins from the bank.\n(anyone's turn){ansiColours['reset']}"

  def test_AppleOrchard(self, capsys):
    # Arrange
    testCard = AppleOrchard()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessBlueCard(testCard)
    assessCardTriggers(testCard, "Apple Orchard", [10], capsys)

    assert testCard.cost == 3
    assert testCard.zIndex == cardOrder.index(testCard.title)

    assert testCard.title == "Apple Orchard"
    assert testCard.description == "Get 3 coins from the bank.\n(anyone's turn)"
    assert str(testCard) == f"{ansiColours['blue']}Apple Orchard{ansiColours['reset']}\n{ansiColours['blue']}Get 3 coins from the bank.\n(anyone's turn){ansiColours['reset']}"

class TestGreenCards:
  def assessGreenCard(self, test: GreenCard):
    """
    Checks for the attributes and corresponding values that all Green cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "green"

    assert hasattr(test, 'colorize')
    assert test.colorize == ansiColours["green"]

    assert hasattr(test, 'reset')
    assert test.reset == ansiColours["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Green cards trigger for the current player only."

    assert hasattr(test, 'cardType')
    assert test.cardType == "Secondary"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_GreenTemplate(self, capsys):
    # Arrange
    testCard = GreenCard()

    # Act / Assert
    self.assessGreenCard(testCard)

    assert testCard.title == "A Green card"
    assert testCard.description == "A template for cards that are Secondary Industries"
    assert str(testCard) == f"{ansiColours['green']}A Green card{ansiColours['reset']}\n{ansiColours['green']}A template for cards that are Secondary Industries{ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    testCard.trigger(mockGame, mockPlayer, 1)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    with pytest.raises(RuntimeError) as error:
      testCard.activate(mockGame, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      consoleLines = captured.out.splitlines()
      assert len(consoleLines) == 2
      assert consoleLines[0] == f"This is {ansiColours['green']}A Green card{ansiColours['reset']}; {ansiColours['green']}A template for cards that are Secondary Industries{ansiColours['reset']}"
      assert consoleLines[1] == "it has not been used to create an actual card yet."

  def test_Bakery(self, capsys):
    # Arrange
    testCard = Bakery()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessGreenCard(testCard)
    assessCardTriggers(testCard, "Bakery", [2, 3], capsys)

    assert testCard.cost == 1
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Bakery"
    assert testCard.description == "Get 1 coin from the bank.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['green']}Bakery{ansiColours['reset']}\n{ansiColours['green']}Get 1 coin from the bank.\n(your turn only){ansiColours['reset']}"

  def test_ConvenienceStore(self, capsys):
    # Arrange
    testCard = ConvenienceStore()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessGreenCard(testCard)
    assessCardTriggers(testCard, "Convenience Store", [4], capsys)

    assert testCard.cost == 2
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Convenience Store"
    assert testCard.description == "Get 3 coins from the bank.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['green']}Convenience Store{ansiColours['reset']}\n{ansiColours['green']}Get 3 coins from the bank.\n(your turn only){ansiColours['reset']}"
  
  def test_CheeseFactory(self, capsys):
    # Arrange
    testCard = CheeseFactory()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessGreenCard(testCard)
    assessCardTriggers(testCard, "Cheese Factory", [7], capsys)

    assert testCard.cost == 5
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Cheese Factory"
    assert testCard.description == "Get 3 coins from the bank per Ranch you own.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['green']}Cheese Factory{ansiColours['reset']}\n{ansiColours['green']}Get 3 coins from the bank per Ranch you own.\n(your turn only){ansiColours['reset']}"

  def test_FurnitureFactory(self, capsys):
    # Arrange
    testCard = FurnitureFactory()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessGreenCard(testCard)
    assessCardTriggers(testCard, "Furniture Factory", [8], capsys)

    assert testCard.cost == 3
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Furniture Factory"
    assert testCard.description == "Get 3 coins from the bank per Forest/Mine you own.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['green']}Furniture Factory{ansiColours['reset']}\n{ansiColours['green']}Get 3 coins from the bank per Forest/Mine you own.\n(your turn only){ansiColours['reset']}"

  def test_FarmersMarket(self, capsys):
    # Arrange
    testCard = FarmersMarket()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessGreenCard(testCard)
    assessCardTriggers(testCard, "Farmers Market", [11, 12], capsys)

    assert testCard.cost == 2
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Farmers Market"
    assert testCard.description == "Get 2 coins from the bank per Field/Orchard you own.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['green']}Farmers Market{ansiColours['reset']}\n{ansiColours['green']}Get 2 coins from the bank per Field/Orchard you own.\n(your turn only){ansiColours['reset']}"

class TestRedCards:
  def assessRedCard(self, test: RedCard):
    """
    Checks for the attributes and corresponding values that all Red cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "red"

    assert hasattr(test, 'colorize')
    assert test.colorize == ansiColours["red"]

    assert hasattr(test, 'reset')
    assert test.reset == ansiColours["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Red cards trigger for everyone except the current player."

    assert hasattr(test, 'cardType')
    assert test.cardType == "Restaurant"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_RedTemplate(self, capsys):
    # Arrange
    testCard = RedCard()

    # Act / Assert
    self.assessRedCard(testCard)

    assert testCard.title == "A Red card"
    assert testCard.description == "A template for cards that are Restaurants"
    assert str(testCard) == f"{ansiColours['red']}A Red card{ansiColours['reset']}\n{ansiColours['red']}A template for cards that are Restaurants{ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    testCard.trigger(mockGame, mockPlayer, 1)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    with pytest.raises(RuntimeError) as error:
      testCard.activate(mockGame, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      consoleLines = captured.out.splitlines()
      assert len(consoleLines) == 2
      assert consoleLines[0] == f"This is {ansiColours['red']}A Red card{ansiColours['reset']}; {ansiColours['red']}A template for cards that are Restaurants{ansiColours['reset']}"
      assert consoleLines[1] == "it has not been used to create an actual card yet."

  def test_Cafe(self, capsys):
    # Arrange
    testCard = Cafe()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessRedCard(testCard)
    assessCardTriggers(testCard, "Cafe", [3], capsys)

    assert testCard.cost == 2
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Cafe"
    assert testCard.description == "Take 1 coin from the active player.\n(opponent's turn)"
    assert str(testCard) == f"{ansiColours['red']}Cafe{ansiColours['reset']}\n{ansiColours['red']}Take 1 coin from the active player.\n(opponent's turn){ansiColours['reset']}"

  def test_FamilyRestaurant(self, capsys):
    # Arrange
    testCard = FamilyRestaurant()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessRedCard(testCard)
    assessCardTriggers(testCard, "Family Restaurant", [9, 10], capsys)

    assert testCard.cost == 3
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Family Restaurant"
    assert testCard.description == "Take 2 coins from the active player.\n(opponent's turn)"
    assert str(testCard) == f"{ansiColours['red']}Family Restaurant{ansiColours['reset']}\n{ansiColours['red']}Take 2 coins from the active player.\n(opponent's turn){ansiColours['reset']}"

class TestPurpleCards:
  def assessPurpleCard(self, test: PurpleCard):
    """
    Checks for the attributes and corresponding values that all Purple cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "purple"

    assert hasattr(test, 'colorize')
    assert test.colorize == ansiColours["purple"]

    assert hasattr(test, 'reset')
    assert test.reset == ansiColours["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Purple cards trigger for the current player only."

    assert hasattr(test, 'cardType')
    assert test.cardType == "Major Establishment"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_PurpleTemplate(self, capsys):
    # Arrange
    testCard = PurpleCard()

    # Act / Assert
    self.assessPurpleCard(testCard)

    assert testCard.title == "A Purple card"
    assert testCard.description == "A template for cards that are Major Establishments"
    assert str(testCard) == f"{ansiColours['purple']}A Purple card{ansiColours['reset']}\n{ansiColours['purple']}A template for cards that are Major Establishments{ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    testCard.trigger(mockGame, mockPlayer, 1)
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    with pytest.raises(RuntimeError) as error:
      testCard.activate(mockGame, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      consoleLines = captured.out.splitlines()
      assert len(consoleLines) == 2
      assert consoleLines[0] == f"This is {ansiColours['purple']}A Purple card{ansiColours['reset']}; {ansiColours['purple']}A template for cards that are Major Establishments{ansiColours['reset']}"
      assert consoleLines[1] == "it has not been used to create an actual card yet."

  def test_Stadium(self, capsys):
    # Arrange
    testCard = Stadium()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessPurpleCard(testCard)
    assessCardTriggers(testCard, "Stadium", [6], capsys)

    assert testCard.cost == 6
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Stadium"
    assert testCard.description == "Take 2 coins from each opponent.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['purple']}Stadium{ansiColours['reset']}\n{ansiColours['purple']}Take 2 coins from each opponent.\n(your turn only){ansiColours['reset']}"

  def test_TVStation(self, capsys):
    # Arrange
    testCard = TVStation()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessPurpleCard(testCard)
    assessCardTriggers(testCard, "TV Station", [6], capsys)

    assert testCard.cost == 7
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "TV Station"
    assert testCard.description == "Take 5 coins from an opponent.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['purple']}TV Station{ansiColours['reset']}\n{ansiColours['purple']}Take 5 coins from an opponent.\n(your turn only){ansiColours['reset']}"

  def test_BusinessCentre(self, capsys):
    # Arrange
    testCard = BusinessCentre()
    testCard.activate = mockActivation

    # Act / Assert
    self.assessPurpleCard(testCard)
    assessCardTriggers(testCard, "Business Centre", [6], capsys)

    assert testCard.cost == 8
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Business Centre"
    assert testCard.description == "Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only)"
    assert str(testCard) == f"{ansiColours['purple']}Business Centre{ansiColours['reset']}\n{ansiColours['purple']}Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only){ansiColours['reset']}"

class TestLandmarks:
  def assessLandmarkCard(self, test: LandmarkCard):
    """
    Checks for the attributes and corresponding values that all Landmark cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "orange"

    assert hasattr(test, 'colorize')
    assert test.colorize == ansiColours["orange"]

    assert hasattr(test, 'reset')
    assert test.reset == ansiColours["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Orange cards do not trigger, they grant special abilities.\nBuilding all 4 landmarks achieves victory."

    assert hasattr(test, 'cardType')
    assert test.cardType == "Landmark"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger') == False
    assert hasattr(test, 'activate') == False
    assert hasattr(test, 'built')
    assert hasattr(test, 'ability')
    assert hasattr(test, 'build')

  def test_LandmarkTemplate(self, capsys):
    # Arrange
    testCard = LandmarkCard()

    # Act / Assert
    self.assessLandmarkCard(testCard)

    assert testCard.title == "An Orange card"
    assert testCard.description == "A template for cards that are Landmarks"

    assert str(testCard) == f"{ansiColours['orange']}An Orange card (unbuilt) - building this will grant:{ansiColours['reset']}\n{ansiColours['orange']}A template for cards that are Landmarks{ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    assert testCard.built == False

    ability = testCard.ability()
    assert ability == "This is An Orange card - it has not been used to create an actual card yet."
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    ability = testCard.build(mockPlayer)
    assert ability == "This is An Orange card - it has not been used to create an actual card yet."
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"PlayerNameHere has built their An Orange card"

    assert testCard.built == True
    assert str(testCard) == f"{ansiColours['orange']}An Orange card{ansiColours['reset']}\n{ansiColours['orange']}A template for cards that are Landmarks{ansiColours['reset']}"

  def test_TrainStation(self, capsys):
    # Arrange
    testCard = TrainStation()

    # Act / Assert
    self.assessLandmarkCard(testCard)

    assert testCard.cost == 4
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Train Station"
    assert testCard.description == "You may roll 1 or 2 dice.\n(Ability)"
    assert str(testCard) == f"{ansiColours['orange']}Train Station (unbuilt) - building this will grant:{ansiColours['reset']}\n{ansiColours['orange']}You may roll 1 or 2 dice.\n(Ability){ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    assert testCard.built == False

    ability = testCard.ability()
    assert ability == 'doubleDice'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    ability = testCard.build(mockPlayer)
    assert ability == 'doubleDice'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert consoleLines[0] == f"PlayerNameHere has built their Train Station"

    assert testCard.built == True
    assert str(testCard) == f"{ansiColours['orange']}Train Station{ansiColours['reset']}\n{ansiColours['orange']}You may roll 1 or 2 dice.\n(Ability){ansiColours['reset']}"

  def test_ShoppingMall(self, capsys):
    # Arrange
    testCard = ShoppingMall()

    # Act / Assert
    self.assessLandmarkCard(testCard)

    assert testCard.cost == 10
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Shopping Mall"
    assert testCard.description == "Your Restaurant and Store establishments earn +1 coin each when activated.\n(Ability)"
    assert str(testCard) == f"{ansiColours['orange']}Shopping Mall (unbuilt) - building this will grant:{ansiColours['reset']}\n{ansiColours['orange']}Your Restaurant and Store establishments earn +1 coin each when activated.\n(Ability){ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    assert testCard.built == False

    ability = testCard.ability()
    assert ability == 'plusOne'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    ability = testCard.build(mockPlayer)
    assert ability == 'plusOne'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert consoleLines[0] == f"PlayerNameHere has built their Shopping Mall"

    assert testCard.built == True
    assert str(testCard) == f"{ansiColours['orange']}Shopping Mall{ansiColours['reset']}\n{ansiColours['orange']}Your Restaurant and Store establishments earn +1 coin each when activated.\n(Ability){ansiColours['reset']}"

  def test_AmusementPark(self, capsys):
    # Arrange
    testCard = AmusementPark()

    # Act / Assert
    self.assessLandmarkCard(testCard)

    assert testCard.cost == 16
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Amusement Park"
    assert testCard.description == "If you roll a double, take another turn after this one.\n(Ability)"
    assert str(testCard) == f"{ansiColours['orange']}Amusement Park (unbuilt) - building this will grant:{ansiColours['reset']}\n{ansiColours['orange']}If you roll a double, take another turn after this one.\n(Ability){ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    assert testCard.built == False

    ability = testCard.ability()
    assert ability == 'doubleTurns'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    ability = testCard.build(mockPlayer)
    assert ability == 'doubleTurns'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert consoleLines[0] == f"PlayerNameHere has built their Amusement Park"

    assert testCard.built == True
    assert str(testCard) == f"{ansiColours['orange']}Amusement Park{ansiColours['reset']}\n{ansiColours['orange']}If you roll a double, take another turn after this one.\n(Ability){ansiColours['reset']}"

  def test_RadioTower(self, capsys):
    # Arrange
    testCard = RadioTower()

    # Act / Assert
    self.assessLandmarkCard(testCard)

    assert testCard.cost == 22
    assert testCard.zIndex == cardOrder.index(testCard.title)
    assert testCard.title == "Radio Tower"
    assert testCard.description == "Once per turn, you may choose to reroll the dice.\n(Ability)"
    assert str(testCard) == f"{ansiColours['orange']}Radio Tower (unbuilt) - building this will grant:{ansiColours['reset']}\n{ansiColours['orange']}Once per turn, you may choose to reroll the dice.\n(Ability){ansiColours['reset']}"

    assert len(testCard.triggers) == 0
    assert testCard.built == False

    ability = testCard.ability()
    assert ability == 'reRolls'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert len(consoleLines) == 0

    ability = testCard.build(mockPlayer)
    assert ability == 'reRolls'
    captured = capsys.readouterr()
    consoleLines = captured.out.splitlines()
    assert consoleLines[0] == f"PlayerNameHere has built their Radio Tower"

    assert testCard.built == True
    assert str(testCard) == f"{ansiColours['orange']}Radio Tower{ansiColours['reset']}\n{ansiColours['orange']}Once per turn, you may choose to reroll the dice.\n(Ability){ansiColours['reset']}"

