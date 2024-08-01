import pytest
import re
from unittest.mock import create_autospec
from reference import reference
from player import Player
from cards.card_types import BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard
from cards.blue import WheatField, Ranch, Forest, Mine, AppleOrchard
from cards.green import Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket
from cards.red import Cafe, FamilyRestaurant
from cards.purple import Stadium, TVStation, BusinessCentre
from cards.landmark import TrainStation, ShoppingMall, AmusementPark, RadioTower
from cards.stacks import Deck, Hand
from game import Game

class MockPlayer(Player):
  def __init__(self):
    super().__init__('PlayerNameHere', 1)
    self.current = False
  
  def declare_action(self, x):
    print(x)

  def start_turn(self):
    self.current = True
  
  def end_turn(self):
    self.current = False

card_order = [
  "Wheat Field","Ranch","Bakery", "Cafe", "Convenience Store",
  "Forest", "Stadium", "TV Station", "Business Centre", "Cheese Factory",
  "Furniture Factory", "Mine", "Family Restaurant", "Apple Orchard", "Farmers Market",
  "Train Station", "Shopping Mall", "Amusement Park", "Radio Tower"
  ]

mock_player = MockPlayer()

mock_game = create_autospec(Game)

def mock_activation(game, dice_roll: int) -> None: # Mock the .activate() function of the card, to test that .trigger() calls this function
  print(f"Card Activated on a roll of {dice_roll}.")

def assess_card_triggers(card: BlueCard|GreenCard|RedCard|PurpleCard, name: str, triggers: list[int], capsys) -> None:
  """
  This function takes a card, and attempts to trigger it for every possible dice roll (1 to 12) and asserts that it will trigger on the correct triggers and will not trigger on other rolls.
  Also checks that the trigger calls the card's activate function by checking for the console output of the card's mocked activate function.
  """

  for n in range(12):
    mock_player.start_turn()    # player is now active player
    card.trigger(mock_game, mock_player, n)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()

    if n in triggers:
      if isinstance(card, BlueCard | GreenCard | PurpleCard):   # active player should have their Blue, Green or Purple cards trigger
        assert len(console_lines) == 2
        assert console_lines[0] == f"Triggered {name} for PlayerNameHere"    # print() statement from trigger()
        assert console_lines[1] == f"Card Activated on a roll of {n}."       # print() statement from the card's mocked activate() function
    else:
      assert len(console_lines) == 0

  for n in range(12):
    mock_player.end_turn()    # player is now not active player
    card.trigger(mock_game, mock_player, n)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()

    if n in triggers:
      if isinstance(card, BlueCard | RedCard):    # non-active players should have their Blue or Red cards trigger
        assert len(console_lines) == 2
        assert console_lines[0] == f"Triggered {name} for PlayerNameHere"
        assert console_lines[1] == f"Card Activated on a roll of {n}."
    else:
      assert len(console_lines) == 0

class TestBlueCards:
  def assess_blue_card(self, test: BlueCard) -> None:
    """
    Checks for the attributes and corresponding values that all Blue cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "blue"

    assert hasattr(test, 'colorize')
    assert test.colorize == reference['ansi_colours']["blue"]

    assert hasattr(test, 'reset')
    assert test.reset == reference['ansi_colours']["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Blue cards trigger for everyone, on everyone's turn."

    assert hasattr(test, 'card_type')
    assert test.card_type == "Primary"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_Blue_Template(self, capsys):
    # Arrange
    test_card = BlueCard()

    # Act / Assert
    self.assess_blue_card(test_card)

    assert test_card.title == "A Blue card"
    assert test_card.description == "A template for cards that are Primary Industries"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}A Blue card{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}A template for cards that are Primary Industries{reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    test_card.trigger(mock_game, mock_player, 1)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0
    with pytest.raises(RuntimeError) as error:
      test_card.activate(mock_game, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      console_lines = captured.out.splitlines()
      assert len(console_lines) == 2
      assert console_lines[0] == f"This is {reference['ansi_colours']['blue']}A Blue card{reference['ansi_colours']['reset']}; {reference['ansi_colours']['blue']}A template for cards that are Primary Industries{reference['ansi_colours']['reset']}"
      assert console_lines[1] == "it has not been used to create an actual card yet."

  def test_WheatField(self, capsys):
    # Arrange
    test_card = WheatField()
    test_card.activate = mock_activation

    # Act / Assert
    self.assess_blue_card(test_card)
    assess_card_triggers(test_card, "Wheat Field", [1], capsys)

    assert test_card.cost == 1
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Wheat Field"
    assert test_card.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}Wheat Field{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}Get 1 coin from the bank.\n(anyone's turn){reference['ansi_colours']['reset']}"

  def test_Ranch(self, capsys):
    # Arrange
    test_card = Ranch()
    test_card.activate = mock_activation

    # Act / Assert
    self.assess_blue_card(test_card)
    assess_card_triggers(test_card, "Ranch", [2], capsys)

    assert test_card.cost == 1
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Ranch"
    assert test_card.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}Ranch{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}Get 1 coin from the bank.\n(anyone's turn){reference['ansi_colours']['reset']}"

  def test_Forest(self, capsys):
    # Arrange
    test_card = Forest()
    test_card.activate = mock_activation

    # Act / Assert
    self.assess_blue_card(test_card)
    assess_card_triggers(test_card, "Forest", [5], capsys)

    assert test_card.cost == 3
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Forest"
    assert test_card.description == "Get 1 coin from the bank.\n(anyone's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}Forest{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}Get 1 coin from the bank.\n(anyone's turn){reference['ansi_colours']['reset']}"

  def test_Mine(self, capsys):
    # Arrange
    test_card = Mine()
    test_card.activate = mock_activation

    # Act / Assert
    self.assess_blue_card(test_card)
    assess_card_triggers(test_card, "Mine", [9], capsys)

    assert test_card.cost == 6
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Mine"
    assert test_card.description == "Get 5 coins from the bank.\n(anyone's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}Mine{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}Get 5 coins from the bank.\n(anyone's turn){reference['ansi_colours']['reset']}"

  def test_AppleOrchard(self, capsys):
    # Arrange
    test_card = AppleOrchard()
    test_card.activate = mock_activation

    # Act / Assert
    self.assess_blue_card(test_card)
    assess_card_triggers(test_card, "Apple Orchard", [10], capsys)

    assert test_card.cost == 3
    assert test_card.z_index == card_order.index(test_card.title)

    assert test_card.title == "Apple Orchard"
    assert test_card.description == "Get 3 coins from the bank.\n(anyone's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['blue']}Apple Orchard{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['blue']}Get 3 coins from the bank.\n(anyone's turn){reference['ansi_colours']['reset']}"

class TestGreenCards:
  def assessGreenCard(self, test: GreenCard):
    """
    Checks for the attributes and corresponding values that all Green cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "green"

    assert hasattr(test, 'colorize')
    assert test.colorize == reference['ansi_colours']["green"]

    assert hasattr(test, 'reset')
    assert test.reset == reference['ansi_colours']["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Green cards trigger for the current player only."

    assert hasattr(test, 'card_type')
    assert test.card_type == "Secondary"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_GreenTemplate(self, capsys):
    # Arrange
    test_card = GreenCard()

    # Act / Assert
    self.assessGreenCard(test_card)

    assert test_card.title == "A Green card"
    assert test_card.description == "A template for cards that are Secondary Industries"
    assert str(test_card) == f"{reference['ansi_colours']['green']}A Green card{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}A template for cards that are Secondary Industries{reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    test_card.trigger(mock_game, mock_player, 1)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    with pytest.raises(RuntimeError) as error:
      test_card.activate(mock_game, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      console_lines = captured.out.splitlines()
      assert len(console_lines) == 2
      assert console_lines[0] == f"This is {reference['ansi_colours']['green']}A Green card{reference['ansi_colours']['reset']}; {reference['ansi_colours']['green']}A template for cards that are Secondary Industries{reference['ansi_colours']['reset']}"
      assert console_lines[1] == "it has not been used to create an actual card yet."

  def test_Bakery(self, capsys):
    # Arrange
    test_card = Bakery()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessGreenCard(test_card)
    assess_card_triggers(test_card, "Bakery", [2, 3], capsys)

    assert test_card.cost == 1
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Bakery"
    assert test_card.description == "Get 1 coin from the bank.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['green']}Bakery{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}Get 1 coin from the bank.\n(your turn only){reference['ansi_colours']['reset']}"

  def test_ConvenienceStore(self, capsys):
    # Arrange
    test_card = ConvenienceStore()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessGreenCard(test_card)
    assess_card_triggers(test_card, "Convenience Store", [4], capsys)

    assert test_card.cost == 2
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Convenience Store"
    assert test_card.description == "Get 3 coins from the bank.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['green']}Convenience Store{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}Get 3 coins from the bank.\n(your turn only){reference['ansi_colours']['reset']}"
  
  def test_CheeseFactory(self, capsys):
    # Arrange
    test_card = CheeseFactory()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessGreenCard(test_card)
    assess_card_triggers(test_card, "Cheese Factory", [7], capsys)

    assert test_card.cost == 5
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Cheese Factory"
    assert test_card.description == "Get 3 coins from the bank per Ranch you own.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['green']}Cheese Factory{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}Get 3 coins from the bank per Ranch you own.\n(your turn only){reference['ansi_colours']['reset']}"

  def test_FurnitureFactory(self, capsys):
    # Arrange
    test_card = FurnitureFactory()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessGreenCard(test_card)
    assess_card_triggers(test_card, "Furniture Factory", [8], capsys)

    assert test_card.cost == 3
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Furniture Factory"
    assert test_card.description == "Get 3 coins from the bank per Forest/Mine you own.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['green']}Furniture Factory{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}Get 3 coins from the bank per Forest/Mine you own.\n(your turn only){reference['ansi_colours']['reset']}"

  def test_FarmersMarket(self, capsys):
    # Arrange
    test_card = FarmersMarket()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessGreenCard(test_card)
    assess_card_triggers(test_card, "Farmers Market", [11, 12], capsys)

    assert test_card.cost == 2
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Farmers Market"
    assert test_card.description == "Get 2 coins from the bank per Field/Orchard you own.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['green']}Farmers Market{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['green']}Get 2 coins from the bank per Field/Orchard you own.\n(your turn only){reference['ansi_colours']['reset']}"

class TestRedCards:
  def assessRedCard(self, test: RedCard):
    """
    Checks for the attributes and corresponding values that all Red cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "red"

    assert hasattr(test, 'colorize')
    assert test.colorize == reference['ansi_colours']["red"]

    assert hasattr(test, 'reset')
    assert test.reset == reference['ansi_colours']["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Red cards trigger for everyone except the current player."

    assert hasattr(test, 'card_type')
    assert test.card_type == "Restaurant"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_RedTemplate(self, capsys):
    # Arrange
    test_card = RedCard()

    # Act / Assert
    self.assessRedCard(test_card)

    assert test_card.title == "A Red card"
    assert test_card.description == "A template for cards that are Restaurants"
    assert str(test_card) == f"{reference['ansi_colours']['red']}A Red card{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['red']}A template for cards that are Restaurants{reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    test_card.trigger(mock_game, mock_player, 1)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    with pytest.raises(RuntimeError) as error:
      test_card.activate(mock_game, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      console_lines = captured.out.splitlines()
      assert len(console_lines) == 2
      assert console_lines[0] == f"This is {reference['ansi_colours']['red']}A Red card{reference['ansi_colours']['reset']}; {reference['ansi_colours']['red']}A template for cards that are Restaurants{reference['ansi_colours']['reset']}"
      assert console_lines[1] == "it has not been used to create an actual card yet."

  def test_Cafe(self, capsys):
    # Arrange
    test_card = Cafe()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessRedCard(test_card)
    assess_card_triggers(test_card, "Cafe", [3], capsys)

    assert test_card.cost == 2
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Cafe"
    assert test_card.description == "Take 1 coin from the active player.\n(opponent's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['red']}Cafe{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['red']}Take 1 coin from the active player.\n(opponent's turn){reference['ansi_colours']['reset']}"

  def test_FamilyRestaurant(self, capsys):
    # Arrange
    test_card = FamilyRestaurant()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessRedCard(test_card)
    assess_card_triggers(test_card, "Family Restaurant", [9, 10], capsys)

    assert test_card.cost == 3
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Family Restaurant"
    assert test_card.description == "Take 2 coins from the active player.\n(opponent's turn)"
    assert str(test_card) == f"{reference['ansi_colours']['red']}Family Restaurant{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['red']}Take 2 coins from the active player.\n(opponent's turn){reference['ansi_colours']['reset']}"

class TestPurpleCards:
  def assessPurpleCard(self, test: PurpleCard):
    """
    Checks for the attributes and corresponding values that all Purple cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "purple"

    assert hasattr(test, 'colorize')
    assert test.colorize == reference['ansi_colours']["purple"]

    assert hasattr(test, 'reset')
    assert test.reset == reference['ansi_colours']["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Purple cards trigger for the current player only."

    assert hasattr(test, 'card_type')
    assert test.card_type == "Major Establishment"

    assert hasattr(test, 'title')
    assert hasattr(test, 'description')
    assert hasattr(test, 'triggers')
    assert hasattr(test, 'trigger')
    assert hasattr(test, 'activate')

  def test_PurpleTemplate(self, capsys):
    # Arrange
    test_card = PurpleCard()

    # Act / Assert
    self.assessPurpleCard(test_card)

    assert test_card.title == "A Purple card"
    assert test_card.description == "A template for cards that are Major Establishments"
    assert str(test_card) == f"{reference['ansi_colours']['purple']}A Purple card{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['purple']}A template for cards that are Major Establishments{reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    test_card.trigger(mock_game, mock_player, 1)
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    with pytest.raises(RuntimeError) as error:
      test_card.activate(mock_game, 1)
      assert error.type is NotImplementedError
      captured = capsys.readouterr()
      console_lines = captured.out.splitlines()
      assert len(console_lines) == 2
      assert console_lines[0] == f"This is {reference['ansi_colours']['purple']}A Purple card{reference['ansi_colours']['reset']}; {reference['ansi_colours']['purple']}A template for cards that are Major Establishments{reference['ansi_colours']['reset']}"
      assert console_lines[1] == "it has not been used to create an actual card yet."

  def test_Stadium(self, capsys):
    # Arrange
    test_card = Stadium()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessPurpleCard(test_card)
    assess_card_triggers(test_card, "Stadium", [6], capsys)

    assert test_card.cost == 6
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Stadium"
    assert test_card.description == "Take 2 coins from each opponent.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['purple']}Stadium{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['purple']}Take 2 coins from each opponent.\n(your turn only){reference['ansi_colours']['reset']}"

  def test_TVStation(self, capsys):
    # Arrange
    test_card = TVStation()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessPurpleCard(test_card)
    assess_card_triggers(test_card, "TV Station", [6], capsys)

    assert test_card.cost == 7
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "TV Station"
    assert test_card.description == "Take 5 coins from an opponent.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['purple']}TV Station{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['purple']}Take 5 coins from an opponent.\n(your turn only){reference['ansi_colours']['reset']}"

  def test_BusinessCentre(self, capsys):
    # Arrange
    test_card = BusinessCentre()
    test_card.activate = mock_activation

    # Act / Assert
    self.assessPurpleCard(test_card)
    assess_card_triggers(test_card, "Business Centre", [6], capsys)

    assert test_card.cost == 8
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Business Centre"
    assert test_card.description == "Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only)"
    assert str(test_card) == f"{reference['ansi_colours']['purple']}Business Centre{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['purple']}Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only){reference['ansi_colours']['reset']}"

class TestLandmarks:
  def assessLandmarkCard(self, test: LandmarkCard):
    """
    Checks for the attributes and corresponding values that all Landmark cards should have
    """
    assert hasattr(test, 'colour')
    assert test.colour == "orange"

    assert hasattr(test, 'colorize')
    assert test.colorize == reference['ansi_colours']["orange"]

    assert hasattr(test, 'reset')
    assert test.reset == reference['ansi_colours']["reset"]

    assert hasattr(test, 'detail')
    assert test.detail == "Orange cards do not trigger, they grant special abilities.\nBuilding all 4 landmarks achieves victory."

    assert hasattr(test, 'card_type')
    assert test.card_type == "Landmark"

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
    test_card = LandmarkCard()

    # Act / Assert
    self.assessLandmarkCard(test_card)

    assert test_card.title == "An Orange card"
    assert test_card.description == "A template for cards that are Landmarks"

    assert str(test_card) == f"{reference['ansi_colours']['orange']}An Orange card (unbuilt) - building this will grant:{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}A template for cards that are Landmarks{reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    assert test_card.built == False

    ability = test_card.ability()
    assert ability == "This is An Orange card - it has not been used to create an actual card yet."
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    ability = test_card.build(mock_player)
    assert ability == "This is An Orange card - it has not been used to create an actual card yet."
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"PlayerNameHere has built their An Orange card"

    assert test_card.built == True
    assert str(test_card) == f"{reference['ansi_colours']['orange']}An Orange card{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}A template for cards that are Landmarks{reference['ansi_colours']['reset']}"

  def test_TrainStation(self, capsys):
    # Arrange
    test_card = TrainStation()

    # Act / Assert
    self.assessLandmarkCard(test_card)

    assert test_card.cost == 4
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Train Station"
    assert test_card.description == "You may roll 1 or 2 dice.\n(Ability)"
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Train Station (unbuilt) - building this will grant:{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}You may roll 1 or 2 dice.\n(Ability){reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    assert test_card.built == False

    ability = test_card.ability()
    assert ability == 'double_dice'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    ability = test_card.build(mock_player)
    assert ability == 'double_dice'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert console_lines[0] == f"PlayerNameHere has built their Train Station"

    assert test_card.built == True
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Train Station{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}You may roll 1 or 2 dice.\n(Ability){reference['ansi_colours']['reset']}"

  def test_ShoppingMall(self, capsys):
    # Arrange
    test_card = ShoppingMall()

    # Act / Assert
    self.assessLandmarkCard(test_card)

    assert test_card.cost == 10
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Shopping Mall"
    assert test_card.description == "Your store-front establishments earn +1 coin each when activated.\n(Ability)"
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Shopping Mall (unbuilt) - building this will grant:{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}Your store-front establishments earn +1 coin each when activated.\n(Ability){reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    assert test_card.built == False

    ability = test_card.ability()
    assert ability == 'plus_one'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    ability = test_card.build(mock_player)
    assert ability == 'plus_one'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert console_lines[0] == f"PlayerNameHere has built their Shopping Mall"

    assert test_card.built == True
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Shopping Mall{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}Your store-front establishments earn +1 coin each when activated.\n(Ability){reference['ansi_colours']['reset']}"

  def test_AmusementPark(self, capsys):
    # Arrange
    test_card = AmusementPark()

    # Act / Assert
    self.assessLandmarkCard(test_card)

    assert test_card.cost == 16
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Amusement Park"
    assert test_card.description == "If you roll a double, take another turn after this one.\n(Ability)"
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Amusement Park (unbuilt) - building this will grant:{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}If you roll a double, take another turn after this one.\n(Ability){reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    assert test_card.built == False

    ability = test_card.ability()
    assert ability == 'double_turn'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    ability = test_card.build(mock_player)
    assert ability == 'double_turn'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert console_lines[0] == f"PlayerNameHere has built their Amusement Park"

    assert test_card.built == True
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Amusement Park{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}If you roll a double, take another turn after this one.\n(Ability){reference['ansi_colours']['reset']}"

  def test_RadioTower(self, capsys):
    # Arrange
    test_card = RadioTower()

    # Act / Assert
    self.assessLandmarkCard(test_card)

    assert test_card.cost == 22
    assert test_card.z_index == card_order.index(test_card.title)
    assert test_card.title == "Radio Tower"
    assert test_card.description == "Once per turn, you may choose to reroll the dice.\n(Ability)"
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Radio Tower (unbuilt) - building this will grant:{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}Once per turn, you may choose to reroll the dice.\n(Ability){reference['ansi_colours']['reset']}"

    assert len(test_card.triggers) == 0
    assert test_card.built == False

    ability = test_card.ability()
    assert ability == 'reroll'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert len(console_lines) == 0

    ability = test_card.build(mock_player)
    assert ability == 'reroll'
    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    assert console_lines[0] == f"PlayerNameHere has built their Radio Tower"

    assert test_card.built == True
    assert str(test_card) == f"{reference['ansi_colours']['orange']}Radio Tower{reference['ansi_colours']['reset']}\n{reference['ansi_colours']['orange']}Once per turn, you may choose to reroll the dice.\n(Ability){reference['ansi_colours']['reset']}"

class TestDeck:
  blue_card_types = 4
  green_card_types = 4
  red_card_types = 4
  purple_card_types = 3

  def test_Deck_len(self):
    # Arrange
    player_count = 2
    test = Deck(player_count)

    # Act / Assert
    assert len(test) == (self.blue_card_types*6) + (self.green_card_types*6) + (self.red_card_types*6) + (self.purple_card_types*player_count)

  def test_Deck_contents_func(self):
    # Arrange
    player_count = 3
    test = Deck(player_count)

    # Act / Assert
    test_contents = test.contents()
    assert len(test_contents) == 15
    for i, card in enumerate(test_contents):
      assert isinstance(card, list)
      assert len(card) == 4
      assert card[3] == "Qty: 6" or f"Qty: {player_count}"
      if i < 6:
        # first 6 cards are blue/green/red
        assert card[3] == "Qty: 6"
      elif i < 9:
        # cards 7, 8 and 9 are purple
        assert card[3] == f"Qty: {player_count}"
      else:
        # remainder of cards are blue/green/red
        assert card[3] == "Qty: 6"

  def test_Deck_add_func(self, capsys):
    # Arrange
    player_count = 1
    test = Deck(player_count)

    # Act / Assert
    additions = [([Mine], [1]), ([ConvenienceStore], [2]), ([FamilyRestaurant], [3]), ([Stadium, TVStation, BusinessCentre], [1, 2, 1])]
    assert len(test.mines) == 6
    assert len(test.convenience_stores) == 6
    assert len(test.family_restaurants) == 6
    assert len(test.major_establishments) == self.purple_card_types*player_count
    for addition in additions:
      added_cards, qtys = addition
      for card, qty in zip(added_cards, qtys):
        for _ in range(qty):
          test.add(card())
    assert len(test.mines) == 7
    assert len(test.convenience_stores) == 8
    assert len(test.family_restaurants) == 9
    assert len(test.major_establishments) == (self.purple_card_types*player_count) + 4
    with pytest.raises(ValueError, match="Cannot add a Shopping Mall card to the Deck"):
      test.add(ShoppingMall()) #type: ignore

    captured = capsys.readouterr()
    console_lines = captured.out.splitlines()
    line = 0
    for addition in additions:
      purples = 0
      added_cards, qtys = addition
      for card, qty in zip(added_cards, qtys):
        for n in range(qty):
          statements = console_lines[line].split(" - ")
          if card in (Stadium, TVStation, BusinessCentre):
            assert statements[1] == f"there are now {(self.purple_card_types*player_count)+purples+1} cards in this pile"
            purples += 1
          else:
            assert statements[1] == f"there are now {6+n+1} cards in this pile"
          line += 1

    
  def test_Deck_remove_func(self):
    # Arrange
    player_count = 4
    test = Deck(player_count)

    # Act / Assert
    assert len(test.ranches) == 6
    assert len(test.bakeries) == 6
    assert len(test.cafes) == 6
    assert len(test.major_establishments) == self.purple_card_types*player_count
    removed_ranch1 = test.remove('Ranch')
    removed_ranch2 = test.remove('Ranch')
    removed_ranch3 = test.remove('Ranch')
    removed_bakery1 = test.remove('Bakery')
    removed_bakery2 = test.remove('Bakery')
    removed_cafe1 = test.remove('Cafe')
    removed_tv_station = test.remove('TV Station')
    removed_business_centre = test.remove('Business Centre')
    assert len(test.ranches) == 3
    assert len(test.bakeries) == 4
    assert len(test.cafes) == 5
    assert len(test.major_establishments) == (self.purple_card_types*player_count) - 2
    with pytest.raises(AttributeError, match="Cannot remove a Radio Tower card from the Deck - no pile exists for these cards."):
      test.remove('Radio Tower')

