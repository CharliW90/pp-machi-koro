import pytest
import re
import random
from unittest.mock import patch, Mock, create_autospec, call
from reference import reference

from player import Player, reset as reset_player_names

def assess_attributes(*testPlayers: Player) -> None:
  playerColours = ['red','green','blue','purple']
  
  for testPlayer in testPlayers:
    assert hasattr(testPlayer, 'name')
    assert testPlayer.name.isalnum
    assert hasattr(testPlayer, 'colour')
    assert testPlayer.colour in playerColours
    assert hasattr(testPlayer, 'colorize')
    assert testPlayer.colorize in reference['ansi_colours'].values()
    assert hasattr(testPlayer, 'reset')
    assert testPlayer.reset == reference['ansi_colours']['reset']
    assert hasattr(testPlayer, 'turn_order')
    assert 0 <= testPlayer.turn_order <= 3
    assert hasattr(testPlayer, 'current')
    assert hasattr(testPlayer, 'build_action_taken')
    assert hasattr(testPlayer, 'coins')
    assert hasattr(testPlayer, 'cards')
    assert hasattr(testPlayer, 'abilities')
    assert hasattr(testPlayer, 'initialised')

def idFn(arg) -> str:
  """Takes an arg of Any type and describes it in such a way that it usefully identifies the test being run."""
  if isinstance(arg, str):
    if '\\' in repr(arg):
      cleaned = "".join(char if char.isalnum() else "_" for char in arg)
      return f"escape chars {cleaned}"
    length = len(arg)
    if length:
      chars = len(arg.strip())
      if chars:
        return f"{chars} len str: {str(arg)}"
      else:
        return "whitespace"
    else:
      return "empty str"
  elif isinstance(arg, int) and not isinstance(arg, bool):
    if arg < 0:
      return f"int < 0: {arg}"
    if arg > 4:
      return f"big int: {arg}"
    if arg == 4:
      return f"off by one: {arg}"
    else:
      return f"int: {arg}"
  elif isnumeric(arg):
    return f"{type(arg).__name__}: {arg}"
  else:
    return f"{type(arg).__name__}"
  
def isnumeric(var) -> bool:
  """Returns True for any numeric value such as int, float, complex etc. and False for anything else."""
  try:
    int(var)
    return not isinstance(var, bool)
  except ValueError:
    return False
  except TypeError:
    return False

def text_as_colour(text: str, colour: str) -> str:
  """Formats a given string to be in one of the colours red, green, blue or purple"""
  staticColours = {
    'red': "\033[38;2;208;0;0;74m",
    'green': "\033[38;2;0;208;0;74m",
    'blue': "\033[38;2;0;0;208;74m",
    'purple': "\033[38;2;104;0;208;74m",
    'clear': "\033[39m"
  }
  return f"{staticColours[colour]}{text}{staticColours['clear']}"

class TestPlayer:
  @pytest.mark.parametrize(
    "valid_name,pos",
    argvalues=[('string', 0),('aMuchMuchLengthierNameThatsAlmostAbsurdButIsOkay', 1),('a', 2),('First Middle and Last Names', 3)],
    ids=['string', 'long_string', 'single_char', 'string with whitespace']
    )
  def test_inputs_acceptable_names(self, valid_name, pos):
    reset_player_names()
    # Arrange/Act
    test = Player(valid_name, pos)
    # Assert
    assess_attributes(test)
    assert test.name == str(valid_name)

  @pytest.mark.parametrize(
    "invalid_name",
    argvalues=[False, 123, Player('your_name', 0), "", "  ", "new\nline", "return\rcarriage", "tabbed\tname", "deleted_c\bh\ba\br\bs\b", "ThisNameIsInvalidAsItIsGreaterThanFortyEightCharacters", float(0.420), ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_inputs_unacceptable_names(self, invalid_name):
    reset_player_names()
    if not isinstance(invalid_name, str):
      expected_message = re.escape(rf"Provided names must be plain strings - {invalid_name} is a {type(invalid_name).__name__}.")
    else:
      if len(invalid_name) > 48:
        expected_message = "Name too long - max length 48 characters!"
      else:
        if '\\' in repr(invalid_name):
          expected_message = "Name cannot contain escape characters!"
        else:
          expected_message = "Name cannot be blank!"
    with pytest.raises(ValueError, match=expected_message):
      reset_player_names()
      Player(invalid_name, 0)

  def test_inputs_acceptable_int(self):
    reset_player_names()
    # Arrange / Act
    test_red = Player('name1', 0)
    test_green = Player('name2', 1)
    test_blue = Player('name3', 2)
    test_purple = Player('name4', 3)

    # Assert
    assess_attributes(test_red, test_green, test_blue, test_purple)

  @pytest.mark.parametrize(
    "invalid_i",
    argvalues=[False, 'string', Player('player_name', 0), float(0.420), float(1.0), float(4.99999), 4, 123, -2, ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_inputs_unacceptable_ints(self, invalid_i):
    reset_player_names()
    if isinstance(invalid_i, int) and not isinstance(invalid_i, bool):
      expected_message = f"Attempting to set colour based on int {invalid_i} is not possible - int must be between 0 and 3"
    else:
      expected_message = "Provided number must be integer"
    with pytest.raises(ValueError, match=expected_message):
      reset_player_names()
      Player('name_okay', invalid_i)

  def test_player_auto_colorize(self, capsys):
    reset_player_names()
    # Arrange
    players = [
      Player('should be red', 0),
      Player('should be green', 1),
      Player('should be blue', 2),
      Player('should be purple', 3)
    ]
    red, green, blue, purple = players
    # Act / Assert
    assess_attributes(*players)
    assert red.colour == 'red'
    assert red.colorize == reference['ansi_colours']['red']
    assert green.colour == 'green'
    assert green.colorize == reference['ansi_colours']['green']
    assert blue.colour == 'blue'
    assert blue.colorize == reference['ansi_colours']['blue']
    assert purple.colour == 'purple'
    assert purple.colorize == reference['ansi_colours']['purple']
    
    for player in players:
      print(f"{player.colorize}this output {player.name}{player.reset}")
    
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == len(players)
    assert console_lines[0] == text_as_colour('this output should be red', 'red')
    assert console_lines[1] == text_as_colour('this output should be green', 'green')
    assert console_lines[2] == text_as_colour('this output should be blue', 'blue')
    assert console_lines[3] == text_as_colour('this output should be purple', 'purple')

  @pytest.mark.parametrize(
    "invalid_colour",
    argvalues=[False, 123, Player('yourNameHere', 0), "", "  ", "not_a_valid_colour", float(0.420), ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_player_invalid_colorize(self, invalid_colour):
    reset_player_names()
    # Arrange
    test = Player('name', 0)

    # Act / Assert
    assert test.colour == 'red'
    assert test.colorize == "\033[38;2;208;0;0;74m"

    if not isinstance(invalid_colour, str):
      expected_message = re.escape(rf"Provided colour must be plain string - {invalid_colour} is a {type(invalid_colour).__name__}.")
    else:
      expected_message = "Somehow the colour for colorize is not one of the valid player colours"
    with pytest.raises(ValueError, match=expected_message):
      test.colorize = invalid_colour
    
    assert test.colour == 'red'
    assert test.colorize == "\033[38;2;208;0;0;74m"

  def test_player_correct_turn_orders(self, capsys):
    reset_player_names()
    # Arrange
    players = [
      Player('One', 0),
      Player('Two', 1),
      Player('Three', 2),
      Player('Four', 3)
    ]
    playerOne, playerTwo, playerThree, playerFour = players

    # Act
    playerOne.turn_order = 3
    playerTwo.turn_order = 2
    playerThree.turn_order = 0
    playerFour.turn_order = 1

    # Assert
    assess_attributes(*players)
    assert playerThree > playerFour
    assert playerFour > playerTwo
    assert playerTwo > playerOne

    assert players[0].name == 'One'
    assert players[1].name == 'Two'
    assert players[2].name == 'Three'
    assert players[3].name == 'Four'
    # sort players in descending order (from first player to last)
    players.sort(reverse=True)
    assert players[0].name == 'Three'
    assert players[1].name == 'Four'
    assert players[2].name == 'Two'
    assert players[3].name == 'One'

    for player in players:
      print(player)
    
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == len(players)
    assert console_lines[0] == "Player 1: Three"
    assert console_lines[1] == "Player 2: Four"
    assert console_lines[2] == "Player 3: Two"
    assert console_lines[3] == "Player 4: One"

  @pytest.mark.parametrize(
    "invalid_i",
    argvalues=[False, 'string', Player('new player', 0), float(0.420), float(1.0), float(4.99999), 4, 123, -2, ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_player_incorrect_turn_orders(self, invalid_i):
    reset_player_names()
    # Arrange
    test = Player('One', 0)
    Player('Two', 1)
    Player('Three', 2)
    Player('Four', 3)

    if isinstance(invalid_i, int) and not isinstance(invalid_i, bool):
      expected_message = f"Cannot assign {invalid_i} as a turn order - in a game of 4 players possible turn orders are 0 / 1 / 2 / 3."
    else:
      expected_message = "Provided number must be integer"
    with pytest.raises(ValueError, match=expected_message):
      test.turn_order = invalid_i

  def test_player_initialisation_locks_edits(self):
    reset_player_names()
    # Arrange
    test = Player('red', 0)
    Player('anyone', 1)
    Player('someone', 2)
    Player('noone', 3)

    # Act
    ## can edit these values
    test.turn_order = 1
    test.colorize = 'green'
    test.colour = 2
    test.name = 'purple'

    ## initialised should now lock these values
    test.initialised = True

    # Assert
    assert test.initialised == True
    with pytest.raises(Exception, match="Player already initialised - cannot initialise again."):
      test.initialised = False
    assert test.initialised == True

    assert test.name == 'purple'
    with pytest.raises(Exception, match="Sorry, but you can't edit players"):
      test.name = "actualName"
    assert test.name == 'purple'

    assert test.colour == 'blue'
    with pytest.raises(Exception, match="Sorry, but you can't edit players"):
      test.colour = 3
    assert test.colour == 'blue'

    assert test.colorize == "\033[38;2;0;208;0;74m"
    with pytest.raises(Exception, match="Sorry, but you can't edit players"):
      test.colorize = 'purple'
    assert test.colorize == "\033[38;2;0;208;0;74m"

    assert test.turn_order == 1
    with pytest.raises(Exception, match="Sorry, but you can't edit players"):
      test.turn_order = 3
    assert test.turn_order == 1

  def test_player_string(self):
    reset_player_names()
    # Arrange
    name = 'test name'
    test = Player(name, 0)
    Player('anyone', 1)
    Player('someone', 2)
    Player('noone', 3)

    # Act
    test.turn_order = 2

    # Assert
    assert str(test) == f"Player 3: test name"

  def test_player_repr(self):
    reset_player_names()
    # Arrange
    name = 'another name'
    test = Player(name, 0)
    Player('anyone', 1)
    Player('someone', 2)
    Player('noone', 3)

    # Act
    test.turn_order = 2

    # Assert
    assert repr(test) == f"Player([2] 'another name': is not the current player; is the red player; has 0 cash; has built 0 landmarks)"

  def test_player_comparison_operators(self):
    reset_player_names()
    # Arrange
    name = 'duplicate name'
    test_one = Player(name, 0)
    reset_player_names()  # allows us to have two players with the same name
    test_two = Player("another_name", 1)
    test_three = Player(name, 2)
    test_four = Player("one more name", 3)
    Player("padding", 0)  # need to create an extra player to pad the 'player names' list back to length 4, otherwise we cannot set turn_order = 3

    # Act
    test_one.turn_order = 3
    test_two.turn_order = 2
    test_three.turn_order = 1
    test_four.turn_order = 0

    # Assert
    assert not test_one == test_two
    assert test_one == test_three   # equal compares names, these have the same name
    assert not test_one == test_four
    assert not test_two == test_three
    assert not test_two == test_four
    assert not test_three == test_four

    assert test_one != test_two
    assert not test_one != test_three   # notequal compares names, these have the same name
    assert test_one != test_four
    assert test_two != test_three
    assert test_two != test_four
    assert test_three != test_four

    assert test_one < test_two < test_three < test_four     # test_one is the last player in turn order, and therefore deemed lowest
    assert test_four > test_three > test_two > test_one     # test_four is the first player in turn order, and therefore deemed highest
    assert test_one <= test_two <= test_three <= test_four  # test_two is after test_one in turn order
    assert test_four >= test_three >= test_two >= test_one  # test_three is after test_two in turn order

    class NotPlayer:
      def __init__(self) -> None:
        self.name = 'duplicate name'
        self.turn_order = 2
    
    test_not_player = NotPlayer()
    assert test_one.name == test_not_player.name
    assert test_one.turn_order > test_not_player.turn_order
    assert not test_one.turn_order < test_not_player.turn_order

    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert test_one == test_not_player
    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert test_one != test_not_player
    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert test_one > test_not_player       # type: ignore
    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert not test_one < test_not_player   # type: ignore
    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert test_one >= test_not_player      # type: ignore
    with pytest.raises(TypeError, match="Cannot compare Player with NotPlayer.  Player class objects may only be compared with other Player class objects."):
      assert not test_one <= test_not_player  # type: ignore

  def test_player_declare_action(self, capsys):
    reset_player_names()
    # Arrange
    test_red = Player('one', 0)
    test_green = Player('two', 1)
    test_blue = Player('three', 2)
    test_purple = Player('four', 3)

    # Act
    test_red.declare_action("Hello Red World!")
    test_green.declare_action("Hello Green World!")
    test_blue.declare_action("Hello Blue World!")
    test_purple.declare_action("Hello Purple World!")

    # Assert
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 4
    assert console_lines[0] == text_as_colour("Hello Red World!", "red")
    assert console_lines[1] == text_as_colour("Hello Green World!", "green")
    assert console_lines[2] == text_as_colour("Hello Blue World!", "blue")
    assert console_lines[3] == text_as_colour("Hello Purple World!", "purple")

  def test_player_begin_turn(self, capsys):
    reset_player_names()
    # Arrange
    test = Player('test_player', 0)

    # Act
    test.begin_turn()

    # Assert
    assert test.current == True
    assert test.build_action_taken == False
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == text_as_colour("It is test_player's turn!", "red")
  
  def test_player_end_turn(self):
    reset_player_names()
    # Arrange
    test = Player('test_player', 0)
    test.begin_turn()

    # Act
    test.end_turn()

    # Assert
    assert test.current == False
    assert test.build_action_taken == False
  
  def test_player_view_hand(self, capsys):
    reset_player_names()
    # Arrange
    test = Player('test_player', 0)

    # Act
    test.view_hand()

    # Assert
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 14
    assert re.search(r"^\s*Name\s*Action\s*Owned\s*$", console_lines[0])
    assert re.search(r"^\s*-*\s*-*\s*-*$", console_lines[1])
    assert re.search(r"^\S*Wheat Field\S*\s*\S*Get 1 coin from the bank.\S*\s*\S*Qty: 1\S*", console_lines[2])
    assert re.search(r"^\S*> \(1\) <\S*\s*\S*\(anyone's turn\)\S*", console_lines[3])
    assert re.search(r"^\S*Bakery\S*\s*\S*Get 1 coin from the bank.\S*\s*\S*Qty: 1\S*", console_lines[4])
    assert re.search(r"^\S*> \(2-3\) <\S*\s*\S*\(your turn only\)\S*", console_lines[5])
    assert re.search(r"^\S*Train Station\S*\s*\S*You may roll 1 or 2 dice.\S*\s*\S*Not yet built...\S*", console_lines[6])
    assert re.search(r"^\S*> Unbuilt Landmark <\S*\s*\S*\(Ability\)\S*", console_lines[7])
    assert re.search(r"^\S*Shopping Mall\S*\s*\S*Your store-front establishments earn \+1 coin each when activated.\S*\s*\S*Not yet built...\S*", console_lines[8])
    assert re.search(r"^\S*> Unbuilt Landmark <\S*\s*\S*\(Ability\)\S*", console_lines[9])
    assert re.search(r"^\S*Amusement Park\S*\s*\S*If you roll a double, take another turn after this one.\S*\s*\S*Not yet built...\S*", console_lines[10])
    assert re.search(r"^\S*> Unbuilt Landmark <\S*\s*\S*\(Ability\)\S*", console_lines[11])
    assert re.search(r"^\S*Radio Tower\S*\s*\S*Once per turn, you may choose to reroll the dice.\S*\s*\S*Not yet built...\S*", console_lines[12])
    assert re.search(r"^\S*> Unbuilt Landmark <\S*\s*\S*\(Ability\)\S*", console_lines[13])

  def test_player_get_balance(self):
    reset_player_names()
    # Arrange
    test = Player('test_player', 0)
    class MockCoin:
      value = 3
    
    mock_coin = MockCoin()

    # Act
    init_balance = test.get_balance()
    test.coins.coppers.append(mock_coin)  #type: ignore
    balance_three = test.get_balance()
    test.coins.silvers.append(mock_coin)  #type: ignore
    balance_six = test.get_balance()
    test.coins.golds.append(mock_coin)  #type: ignore
    balance_nine = test.get_balance()

    # Assert
    assert init_balance == 0
    assert balance_three == 3
    assert balance_six == 6
    assert balance_nine == 9

  @patch('cards.card_types.BlueCard.trigger')
  @patch('cards.card_types.GreenCard.trigger')
  def test_player_activate(self, mocked_Green_trigger, mocked_Blue_trigger):
    reset_player_names()
    # Arrange
    test = Player('test_player', 0)
    mock_game = 'this'

    # Act
    test.activate(mock_game, 'blue', 1)   #type: ignore
    test.activate(mock_game, 'green', 2)  #type: ignore

    # Assert
    mocked_Blue_trigger.assert_called_once_with(mock_game, test, 1)
    mocked_Green_trigger.assert_called_once_with(mock_game, test, 2)

