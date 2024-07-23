import pytest
from unittest.mock import patch, Mock, create_autospec, call
import inquirer.questions
from game import Game, resetPlayers
from reference import MyTheme
from cards import WheatField

from actions.build import buildAction, handleBuilding
from actions.dice import rollDice, roll, handleDiceResult, diceFace

affordableCards = [(f"Card Title Here: Purchase Price: 2 - BUY?", "cardTitleHere"),
  (f"Another Card Title Here: Purchase Price: 6 - BUY?", "anotherCardTitleHere")]

def prepGameAndPlayer():
  resetPlayers()
  mockGame = Game(['PlayerOne', 'PlayerTwo'])

  mockGame.listAffordableCards = lambda player: affordableCards.copy()
  mockGame.notify = lambda message: print(message)

  mockPlayer = mockGame.players[0]

  mockPlayer.declareAction = lambda action: print(action)
  mockPlayer.getBalance = lambda : 3

  return mockGame, mockPlayer


class TestBuildActions:
  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handleBuilding")
  def test_buildAction_Basic(self, mocked_handleBuilding, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_handleBuilding.return_value = False
    mocked_time.sleep = lambda x: None
    mockTheme = MyTheme(mockPlayer)
    mocked_theme.return_value = mockTheme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mockPlayer.colorize}Build an establishment?{mockPlayer.reset}"
    expected_choices = [
      (f"[?] {mockPlayer.colorize}Look at your cards{mockPlayer.reset}", "look"),
      (f"[?] {mockPlayer.colorize}Look at available cards{mockPlayer.reset}", "display"),
      (f"[X] {mockPlayer.colorize}Build Nothing{mockPlayer.reset}", "nothing"),
      (affordableCards[0]),
      (affordableCards[1])
    ]

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}
    
    # Act
    output = buildAction(mockGame, mockPlayer, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluatePrompt(mocked_prompt)
    assert name == expected_name
    assert message == expected_message
    assert type(choices) == list
    assert len(choices) == 5
    for i, choice in enumerate(choices):
      assert type(choice) == inquirer.questions.TaggedValue
      assert str(choice) == expected_choices[i][0]
      assert repr(choice) == f"'{expected_choices[i][1]}'"

    assert output == False

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"Time to build an establishment, {mockPlayer.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handleBuilding")
  def test_buildAction_Basic_NoHand(self, mocked_handleBuilding, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_handleBuilding.return_value = False
    mocked_time.sleep = lambda x: None
    mockTheme = MyTheme(mockPlayer)
    mocked_theme.return_value = mockTheme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mockPlayer.colorize}Build an establishment?{mockPlayer.reset}"
    expected_choices = [
      (f"[?] {mockPlayer.colorize}Look at available cards{mockPlayer.reset}", "display"),
      (f"[X] {mockPlayer.colorize}Build Nothing{mockPlayer.reset}", "nothing"),
      (affordableCards[0]),
      (affordableCards[1])
    ]

    settings = {'offerToShowHand': False, 'offerToShowDeck': True}
    
    # Act
    output = buildAction(mockGame, mockPlayer, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluatePrompt(mocked_prompt)
    assert name == expected_name
    assert message == expected_message
    assert type(choices) == list
    assert len(choices) == 4
    for i, choice in enumerate(choices):
      assert type(choice) == inquirer.questions.TaggedValue
      assert str(choice) == expected_choices[i][0]
      assert repr(choice) == f"'{expected_choices[i][1]}'"

    assert output == False

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"Time to make a decision, {mockPlayer.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handleBuilding")
  def test_buildAction_Basic_NoDeck(self, mocked_handleBuilding, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_handleBuilding.return_value = False
    mocked_time.sleep = lambda x: None
    mockTheme = MyTheme(mockPlayer)
    mocked_theme.return_value = mockTheme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mockPlayer.colorize}Build an establishment?{mockPlayer.reset}"
    expected_choices = [
      (f"[?] {mockPlayer.colorize}Look at your cards{mockPlayer.reset}", "look"),
      (f"[X] {mockPlayer.colorize}Build Nothing{mockPlayer.reset}", "nothing"),
      (affordableCards[0]),
      (affordableCards[1])
    ]

    settings = {'offerToShowHand': True, 'offerToShowDeck': False}
    
    # Act
    output = buildAction(mockGame, mockPlayer, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluatePrompt(mocked_prompt)
    assert name == expected_name
    assert message == expected_message
    assert type(choices) == list
    assert len(choices) == 4
    for i, choice in enumerate(choices):
      assert type(choice) == inquirer.questions.TaggedValue
      assert str(choice) == expected_choices[i][0]
      assert repr(choice) == f"'{expected_choices[i][1]}'"

    assert output == False

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"Time to make a decision, {mockPlayer.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handleBuilding")
  def test_buildAction_Basic_NoHandOrDeck(self, mocked_handleBuilding, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_handleBuilding.return_value = False
    mocked_time.sleep = lambda x: None
    mockTheme = MyTheme(mockPlayer)
    mocked_theme.return_value = mockTheme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mockPlayer.colorize}Build an establishment?{mockPlayer.reset}"
    expected_choices = [
      (f"[X] {mockPlayer.colorize}Build Nothing{mockPlayer.reset}", "nothing"),
      (affordableCards[0]),
      (affordableCards[1])
    ]

    settings = {'offerToShowHand': False, 'offerToShowDeck': False}
    
    # Act
    output = buildAction(mockGame, mockPlayer, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluatePrompt(mocked_prompt)
    assert name == expected_name
    assert message == expected_message
    assert type(choices) == list
    assert len(choices) == 3
    for i, choice in enumerate(choices):
      assert type(choice) == inquirer.questions.TaggedValue
      assert str(choice) == expected_choices[i][0]
      assert repr(choice) == f"'{expected_choices[i][1]}'"

    assert output == False

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"Time to make a decision, {mockPlayer.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handleBuilding")
  def test_buildAction_TriggersBuild(self, mocked_handleBuilding, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_handleBuilding.return_value = False
    mocked_time.sleep = lambda x: None
    mockTheme = MyTheme(mockPlayer)
    mocked_theme.return_value = mockTheme
    mocked_prompt.return_value = {'build': "cardTitleHere"}

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}
    
    # Act
    output = buildAction(mockGame, mockPlayer, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    mocked_handleBuilding.assert_called_once_with(mockGame, mockPlayer, "cardTitleHere", settings)

    assert output == False

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"Time to build an establishment, {mockPlayer.name}!  You have 3 coins"

  @patch("actions.build.time")
  @patch("actions.build.buildAction")
  def test_handleBuilding_handlesNothing(self, mocked_buildAction, mocked_time, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_time.sleep = lambda x: None
    mocked_buildAction.return_value = True

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}

    # Act
    output = handleBuilding(mockGame, mockPlayer, 'nothing', settings)

    # Assert
    assert output == False
    assert not mocked_buildAction.called

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"{mockPlayer.name} built nothing this round - holding onto their 3 coins!"

  @patch("actions.build.time")
  @patch("actions.build.buildAction")
  def test_handleBuilding_handlesShowHand(self, mocked_buildAction, mocked_time, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_time.sleep = lambda x: None
    mocked_buildAction.return_value = True
    mockPlayer.viewHand = lambda: print("This would be many lines\nrepresenting many cards\nin the player's hand")

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}

    # Act
    output = handleBuilding(mockGame, mockPlayer, 'look', settings)

    # Assert
    assert output == True
    settings["offerToShowHand"] = False
    mocked_buildAction.assert_called_once_with(mockGame, mockPlayer, settings)

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 3
    assert consoleLines[0] == "This would be many lines"
    assert consoleLines[1] == "representing many cards"
    assert consoleLines[2] == "in the player's hand"

  @patch("actions.build.time")
  @patch("actions.build.buildAction")
  def test_handleBuilding_handlesShowDeck(self, mocked_buildAction, mocked_time, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_time.sleep = lambda x: None
    mocked_buildAction.return_value = True
    mockGame.displayCardsToPlayer = lambda player: print("This would be many lines\nrepresenting many cards\nin the game's deck")

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}

    # Act
    output = handleBuilding(mockGame, mockPlayer, 'display', settings)

    # Assert
    assert output == True
    settings["offerToShowDeck"] = False
    mocked_buildAction.assert_called_once_with(mockGame, mockPlayer, settings)

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 3
    assert consoleLines[0] == "This would be many lines"
    assert consoleLines[1] == "representing many cards"
    assert consoleLines[2] == "in the game's deck"

  @patch("actions.build.time")
  @patch("actions.build.buildAction")
  def test_handleBuilding_handlesCardBuilding(self, mocked_buildAction, mocked_time, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_time.sleep = lambda x: None
    mocked_buildAction.return_value = True
    mockBuild = create_autospec(mockPlayer.build, return_value=True)
    mockPlayer.build = mockBuild
    mockCard = WheatField()
    mockTakeCard = create_autospec(mockGame.takeCardFromStack, return_value=mockCard)
    mockGame.takeCardFromStack = mockTakeCard

    settings = {'offerToShowHand': True, 'offerToShowDeck': True}

    # Act
    output = handleBuilding(mockGame, mockPlayer, "a card title", settings)

    # Assert
    assert output == True
    assert not mocked_buildAction.called

    # assert mockGame.takeCardFromStack.assert_called_once_with("a card title")
    mockTakeCard.assert_called_once_with("a card title")
    mockBuild.assert_called_once_with(mockCard, mockGame.bank)

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 0

def evaluatePrompt(mockPrompt: Mock) -> tuple[str, str, list]:
  called_with = mockPrompt.call_args[0]
  assert type(called_with) == tuple
  assert len(called_with) == 1

  prompt = called_with[0]
  assert type(prompt) == list
  assert len(prompt) == 1

  question = prompt[0]
  assert isinstance(question, inquirer.questions.List)

  assert hasattr(question, "name")
  assert hasattr(question, "message")
  assert hasattr(question, "choices")
  name = question.name
  message = question.message
  choices = question.choices
  return (name, message, choices)

class TestDiceActions:
  def test_roll_x100(self):
    for _ in range(100):
      output = roll()
      assert 1 <= output <= 6
  
  def test_diceFace(self):
    assert diceFace(1) == diceFaces[0]
    assert diceFace(2) == diceFaces[1]
    assert diceFace(3) == diceFaces[2]
    assert diceFace(4) == diceFaces[3]
    assert diceFace(5) == diceFaces[4]
    assert diceFace(6) == diceFaces[5]
  
  def test_handleDiceResult(self):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mockActivateOne = create_autospec(mockPlayer.activate)
    mockGame.players[0].activate = mockActivateOne
    mockActivateTwo = create_autospec(mockPlayer.activate)
    mockGame.players[1].activate = mockActivateTwo

    mockGame.players[0].current = True
    mockGame.players[1].current = False

    # Act/Assert
    for n in range(5):
      handleDiceResult(mockGame, n+1)
      mockActivateOne.assert_has_calls([call(mockGame, "blue", n+1), call(mockGame, "green", n+1), call(mockGame, "purple", n+1)])
      mockActivateTwo.assert_has_calls([call(mockGame, "red", n+1), call(mockGame, "blue", n+1)])

  @patch("actions.dice.handleDiceResult")
  @patch("actions.dice.inquirer.prompt")
  def test_rollDice_x100_oneDice(self, mocked_prompt, mocked_handleDiceResult, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_prompt.return_value = {'dice': 1}
    mocked_handleDiceResult.return_value = None
    mockPlayer.current = True

    for _ in range(100):
      # Act
      rollDice(mockGame, mockPlayer)

      # Assert
      console = capsys.readouterr()
      consoleLines = console.out.splitlines()
      assert len(consoleLines) == 8
      assert consoleLines[0] == f"Time to roll the dice, {mockPlayer.name}!"
      assert consoleLines[1] == f"{mockPlayer.name} rolled 1 dice"

      resultString = consoleLines[7].split(' ')
      assert len(resultString) == 3
      assert resultString[0] == ">"
      assert resultString[2] == "<"
      result = int(resultString[1])
      assert 1 <= result <= 6

      diceFaceString = "\n".join(consoleLines[2:7])
      assert diceFaceString == diceFaces[result-1]

      mocked_handleDiceResult.assert_called_once_with(mockGame, result)
      mocked_handleDiceResult.reset_mock()

  @patch("actions.dice.handleDiceResult")
  @patch("actions.dice.inquirer.prompt")
  def test_rollDice_x100_twoDice(self, mocked_prompt, mocked_handleDiceResult, capsys):
    # Arrange
    mockGame, mockPlayer = prepGameAndPlayer()
    mocked_prompt.return_value = {'dice': 2}
    mocked_handleDiceResult.return_value = None
    mockPlayer.current = True

    for _ in range(100):
      # Act
      rollDice(mockGame, mockPlayer)

      # Assert
      console = capsys.readouterr()
      consoleLines = console.out.splitlines()
      assert len(consoleLines) == 8
      assert consoleLines[0] == f"Time to roll the dice, {mockPlayer.name}!"
      assert consoleLines[1] == f"{mockPlayer.name} rolled 2 dice"

      resultString = consoleLines[7].split(' ')
      assert len(resultString) == 3
      assert resultString[0] == ">"
      assert resultString[2] == "<"
      result = int(resultString[1])
      assert 2 <= result <= 12

      splitDiceStrings = [line.split("  ::  ") for line in consoleLines[2:7]]
      diceStringOne = "\n".join([string[0] for string in splitDiceStrings])
      diceStringTwo = "\n".join([string[1] for string in splitDiceStrings])

      assert diceStringOne in diceFaces
      assert diceStringTwo in diceFaces

      mocked_handleDiceResult.assert_called_once_with(mockGame, result)
      mocked_handleDiceResult.reset_mock()


diceFaces = [
# 1
"-----\n\
|   |\n\
| o |\n\
|   |\n\
-----",
# 2
"-----\n\
|o  |\n\
|   |\n\
|  o|\n\
-----",
# 3
"-----\n\
|o  |\n\
| o |\n\
|  o|\n\
-----",
# 4
"-----\n\
|o o|\n\
|   |\n\
|o o|\n\
-----",
# 5
"-----\n\
|o o|\n\
| o |\n\
|o o|\n\
-----",
# 6
"-----\n\
|o o|\n\
|o o|\n\
|o o|\n\
-----"
]