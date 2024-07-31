import pytest
import re
from unittest.mock import patch, Mock, create_autospec, call
from reference import reference

from player import Player, reset as resetPlayerNames

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
    # Arrange/Act
    test = Player(valid_name, pos)
    # Assert
    assess_attributes(test)
    assert test.name == str(valid_name)
  
  resetPlayerNames()

  @pytest.mark.parametrize(
    "invalid_name",
    argvalues=[False, 123, Player('yourNameHere', 0), "", "  ", "new\nline", "return\rcarriage", "tabbed\tname", "deleted_c\bh\ba\br\bs\b", "ThisNameIsInvalidAsItIsGreaterThanFortyEightCharacters", float(0.420), ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_inputs_unacceptable_names(self, invalid_name):
    if not isinstance(invalid_name, str):
      expected_message = re.escape(rf"Provided names must be plain strings - {invalid_name} is a {type(invalid_name).__name__}.")
    else:
      if len(invalid_name) > 48:
        expected_message = "Name too long - max length 48 characters!"
      else:
        print(repr(invalid_name), "<< encoded name")
        if '\\' in repr(invalid_name):
          expected_message = "Name cannot contain escape characters!"
        else:
          expected_message = "Name cannot be blank!"
    with pytest.raises(ValueError, match=expected_message):
      resetPlayerNames()
      Player(invalid_name, 0)
  
  resetPlayerNames()

  def test_inputs_acceptable_int(self):
    # Arrange / Act
    test_red = Player('name1', 0)
    test_green = Player('name2', 1)
    test_blue = Player('name3', 2)
    test_purple = Player('name4', 3)

    # Assert
    assess_attributes(test_red, test_green, test_blue, test_purple)

  resetPlayerNames()

  @pytest.mark.parametrize(
    "invalid_i",
    argvalues=[False, 'string', Player('yourNameHere', 0), float(0.420), float(1.0), float(4.99999), 4, 123, -2, ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_inputs_unacceptable_ints(self, invalid_i):
    if isinstance(invalid_i, int) and not isinstance(invalid_i, bool):
      expected_message = f"Attempting to set colour based on int {invalid_i} is not possible - int must be between 0 and 3"
    else:
      expected_message = "Provided number must be integer"
    with pytest.raises(ValueError, match=expected_message):
      resetPlayerNames()
      Player('name_okay', invalid_i)
  
  resetPlayerNames()

  def test_player_auto_colorize(self, capsys):
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
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == len(players)
    assert consoleLines[0] == text_as_colour('this output should be red', 'red')
    assert consoleLines[1] == text_as_colour('this output should be green', 'green')
    assert consoleLines[2] == text_as_colour('this output should be blue', 'blue')
    assert consoleLines[3] == text_as_colour('this output should be purple', 'purple')

  resetPlayerNames()

  @pytest.mark.parametrize(
    "invalid_colour",
    argvalues=[False, 123, Player('yourNameHere', 0), "", "  ", "not_a_valid_colour", float(0.420), ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_player_invalid_colorize(self, invalid_colour):
    # Arrange
    resetPlayerNames()
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

  resetPlayerNames()

  def test_player_correct_turn_orders(self, capsys):
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
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == len(players)
    assert consoleLines[0] == "Player 1: Three"
    assert consoleLines[1] == "Player 2: Four"
    assert consoleLines[2] == "Player 3: Two"
    assert consoleLines[3] == "Player 4: One"

  resetPlayerNames()

  @pytest.mark.parametrize(
    "invalid_i",
    argvalues=[False, 'string', Player('yourNameHere', 0), float(0.420), float(1.0), float(4.99999), 4, 123, -2, ["string", 123, True], ('this', 'that'), {1, 2, 3}, {'1': 'one', '2': 'two',  '3': 'three'}, b'hello world', None],
    ids=idFn
    )
  def test_player_incorrect_turn_orders(self, invalid_i):
    # Arrange
    resetPlayerNames()
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

  def test_initialised_locks_player_edits(self):
    # Arrange
    test = Player('red', 0)

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


