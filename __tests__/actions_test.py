import pytest
from unittest.mock import patch, Mock, create_autospec, call
import inquirer.questions
from game import Game, reset_players
from reference import MyTheme
from cards import WheatField

from actions.build import build_action, handle_building
from actions.dice import roll_dice, roll, handle_dice_result, dice_face

affordable_cards = [
  (f"Card Title Here: Purchase Price: 2 - BUY?", "cardTitleHere"),
  (f"Another Card Title Here: Purchase Price: 6 - BUY?", "anotherCardTitleHere")
]

def prep_game_and_player():
  reset_players()
  mock_game = Game(['PlayerOne', 'PlayerTwo'])

  mock_game.list_affordable_cards = lambda player: affordable_cards.copy()
  mock_game.notify = lambda message: print(message)

  mock_player = mock_game.players[0]

  mock_player.declare_action = lambda action: print(action)
  mock_player.get_balance = lambda : 3

  return mock_game, mock_player

class TestBuildActions:
  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handle_building")
  def test_build_action_Basic(self, mocked_handle_building, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_handle_building.return_value = False
    mocked_time.sleep = lambda x: None
    mock_theme = MyTheme(mock_player)
    mocked_theme.return_value = mock_theme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mock_player.colorize}Build an establishment?{mock_player.reset}"
    expected_choices = [
      (f"[?] {mock_player.colorize}Look at your cards{mock_player.reset}", "look"),
      (f"[?] {mock_player.colorize}Look at available cards{mock_player.reset}", "display"),
      (f"[X] {mock_player.colorize}Build Nothing{mock_player.reset}", "nothing"),
      (affordable_cards[0]),
      (affordable_cards[1])
    ]

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}
    
    # Act
    output = build_action(mock_game, mock_player, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluate_prompt(mocked_prompt)
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
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"Time to build an establishment, {mock_player.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handle_building")
  def test_build_action_Basic_No_Hand(self, mocked_handle_building, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_handle_building.return_value = False
    mocked_time.sleep = lambda x: None
    mock_theme = MyTheme(mock_player)
    mocked_theme.return_value = mock_theme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mock_player.colorize}Build an establishment?{mock_player.reset}"
    expected_choices = [
      (f"[?] {mock_player.colorize}Look at available cards{mock_player.reset}", "display"),
      (f"[X] {mock_player.colorize}Build Nothing{mock_player.reset}", "nothing"),
      (affordable_cards[0]),
      (affordable_cards[1])
    ]

    settings = {'offer_to_show_hand': False, 'offer_to_show_deck': True}
    
    # Act
    output = build_action(mock_game, mock_player, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluate_prompt(mocked_prompt)
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
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"Time to make a decision, {mock_player.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handle_building")
  def test_build_action_Basic_No_Deck(self, mocked_handle_building, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_handle_building.return_value = False
    mocked_time.sleep = lambda x: None
    mock_theme = MyTheme(mock_player)
    mocked_theme.return_value = mock_theme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mock_player.colorize}Build an establishment?{mock_player.reset}"
    expected_choices = [
      (f"[?] {mock_player.colorize}Look at your cards{mock_player.reset}", "look"),
      (f"[X] {mock_player.colorize}Build Nothing{mock_player.reset}", "nothing"),
      (affordable_cards[0]),
      (affordable_cards[1])
    ]

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': False}
    
    # Act
    output = build_action(mock_game, mock_player, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluate_prompt(mocked_prompt)
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
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"Time to make a decision, {mock_player.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handle_building")
  def test_build_action_Basic_No_Hand_or_Deck(self, mocked_handle_building, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_handle_building.return_value = False
    mocked_time.sleep = lambda x: None
    mock_theme = MyTheme(mock_player)
    mocked_theme.return_value = mock_theme
    mocked_prompt.return_value = {'build': "nothing"}

    expected_name = "build"
    expected_message = f"{mock_player.colorize}Build an establishment?{mock_player.reset}"
    expected_choices = [
      (f"[X] {mock_player.colorize}Build Nothing{mock_player.reset}", "nothing"),
      (affordable_cards[0]),
      (affordable_cards[1])
    ]

    settings = {'offer_to_show_hand': False, 'offer_to_show_deck': False}
    
    # Act
    output = build_action(mock_game, mock_player, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    name, message, choices = evaluate_prompt(mocked_prompt)
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
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"Time to make a decision, {mock_player.name}!  You have 3 coins"

  @patch("actions.build.inquirer.prompt")
  @patch("actions.build.MyTheme")
  @patch("actions.build.time")
  @patch("actions.build.handle_building")
  def test_build_action_Triggers_Build(self, mocked_handle_building, mocked_time, mocked_theme, mocked_prompt, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_handle_building.return_value = False
    mocked_time.sleep = lambda x: None
    mock_theme = MyTheme(mock_player)
    mocked_theme.return_value = mock_theme
    mocked_prompt.return_value = {'build': "cardTitleHere"}

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}
    
    # Act
    output = build_action(mock_game, mock_player, settings)
    
    # Assert
    mocked_prompt.assert_called_once
    mocked_handle_building.assert_called_once_with(mock_game, mock_player, "cardTitleHere", settings)

    assert output == False

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"Time to build an establishment, {mock_player.name}!  You have 3 coins"

  @patch("actions.build.time")
  @patch("actions.build.build_action")
  def test_handle_building_Handles_Nothing(self, mocked_build_action, mocked_time, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_time.sleep = lambda x: None
    mocked_build_action.return_value = True

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}

    # Act
    output = handle_building(mock_game, mock_player, 'nothing', settings)

    # Assert
    assert output == False
    assert not mocked_build_action.called

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"{mock_player.name} built nothing this round - holding onto their 3 coins!"

  @patch("actions.build.time")
  @patch("actions.build.build_action")
  def test_handle_building_handlesShowHand(self, mocked_build_action, mocked_time, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_time.sleep = lambda x: None
    mocked_build_action.return_value = True
    mock_player.view_hand = lambda: print("This would be many lines\nrepresenting many cards\nin the player's hand")

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}

    # Act
    output = handle_building(mock_game, mock_player, 'look', settings)

    # Assert
    assert output == True
    settings["offer_to_show_hand"] = False
    mocked_build_action.assert_called_once_with(mock_game, mock_player, settings)

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 3
    assert console_lines[0] == "This would be many lines"
    assert console_lines[1] == "representing many cards"
    assert console_lines[2] == "in the player's hand"

  @patch("actions.build.time")
  @patch("actions.build.build_action")
  def test_handle_building_Handles_Show_Deck(self, mocked_build_action, mocked_time, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_time.sleep = lambda x: None
    mocked_build_action.return_value = True
    mock_game.display_cards_to_player = lambda player: print("This would be many lines\nrepresenting many cards\nin the game's deck")

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}

    # Act
    output = handle_building(mock_game, mock_player, 'display', settings)

    # Assert
    assert output == True
    settings["offer_to_show_deck"] = False
    mocked_build_action.assert_called_once_with(mock_game, mock_player, settings)

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 3
    assert console_lines[0] == "This would be many lines"
    assert console_lines[1] == "representing many cards"
    assert console_lines[2] == "in the game's deck"

  @patch("actions.build.time")
  @patch("actions.build.build_action")
  def test_handle_building_Handles_Card_Building(self, mocked_build_action, mocked_time, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_time.sleep = lambda x: None
    mocked_build_action.return_value = True
    mock_build = create_autospec(mock_player.build, return_value=True)
    mock_player.build = mock_build
    mock_card = WheatField()
    mock_take_card = create_autospec(mock_game.take_card_from_stack, return_value=mock_card)
    mock_game.take_card_from_stack = mock_take_card

    settings = {'offer_to_show_hand': True, 'offer_to_show_deck': True}

    # Act
    output = handle_building(mock_game, mock_player, "a card title", settings)

    # Assert
    assert output == True
    assert not mocked_build_action.called

    # assert mock_game.takeCardFromStack.assert_called_once_with("a card title")
    mock_take_card.assert_called_once_with("a card title")
    mock_build.assert_called_once_with(mock_card, mock_game.bank)

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 0

def evaluate_prompt(mock_prompt: Mock) -> tuple[str, str, list]:
  called_with = mock_prompt.call_args[0]
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
  
  def test_dice_face(self):
    assert dice_face(1) == dice_faces[0]
    assert dice_face(2) == dice_faces[1]
    assert dice_face(3) == dice_faces[2]
    assert dice_face(4) == dice_faces[3]
    assert dice_face(5) == dice_faces[4]
    assert dice_face(6) == dice_faces[5]
  
  def test_handle_dice_result(self):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mock_activate_one = create_autospec(mock_player.activate)
    mock_game.players[0].activate = mock_activate_one
    mock_activate_two = create_autospec(mock_player.activate)
    mock_game.players[1].activate = mock_activate_two

    mock_game.players[0].current = True
    mock_game.players[1].current = False

    # Act/Assert
    for n in range(5):
      handle_dice_result(mock_game, n+1)
      mock_activate_one.assert_has_calls([call(mock_game, "blue", n+1), call(mock_game, "green", n+1), call(mock_game, "purple", n+1)])
      mock_activate_two.assert_has_calls([call(mock_game, "red", n+1), call(mock_game, "blue", n+1)])

  @patch("actions.dice.handle_dice_result")
  @patch("actions.dice.inquirer.prompt")
  def test_roll_dice_x100_one_dice(self, mocked_prompt, mocked_handle_dice_result, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_prompt.return_value = {'dice': 1}
    mocked_handle_dice_result.return_value = None
    mock_player.current = True

    for _ in range(100):
      # Act
      roll_dice(mock_game, mock_player)

      # Assert
      console = capsys.readouterr()
      console_lines = console.out.splitlines()
      assert len(console_lines) == 8
      assert console_lines[0] == f"Time to roll the dice, {mock_player.name}!"
      assert console_lines[1] == f"{mock_player.name} rolled 1 dice"

      result_string = console_lines[7].split(' ')
      assert len(result_string) == 3
      assert result_string[0] == ">"
      assert result_string[2] == "<"
      result = int(result_string[1])
      assert 1 <= result <= 6

      dice_face_string = "\n".join(console_lines[2:7])
      assert dice_face_string == dice_faces[result-1]

      mocked_handle_dice_result.assert_called_once_with(mock_game, result)
      mocked_handle_dice_result.reset_mock()

  @patch("actions.dice.handle_dice_result")
  @patch("actions.dice.inquirer.prompt")
  def test_rollDice_x100_twoDice(self, mocked_prompt, mocked_handle_dice_result, capsys):
    # Arrange
    mock_game, mock_player = prep_game_and_player()
    mocked_prompt.return_value = {'dice': 2}
    mocked_handle_dice_result.return_value = None
    mock_player.current = True

    for _ in range(100):
      # Act
      roll_dice(mock_game, mock_player)

      # Assert
      console = capsys.readouterr()
      console_lines = console.out.splitlines()
      assert len(console_lines) == 8
      assert console_lines[0] == f"Time to roll the dice, {mock_player.name}!"
      assert console_lines[1] == f"{mock_player.name} rolled 2 dice"

      resultString = console_lines[7].split(' ')
      assert len(resultString) == 3
      assert resultString[0] == ">"
      assert resultString[2] == "<"
      result = int(resultString[1])
      assert 2 <= result <= 12

      split_dice_strings = [line.split("  ::  ") for line in console_lines[2:7]]
      dice_string_one = "\n".join([string[0] for string in split_dice_strings])
      dice_string_two = "\n".join([string[1] for string in split_dice_strings])

      assert dice_string_one in dice_faces
      assert dice_string_two in dice_faces

      mocked_handle_dice_result.assert_called_once_with(mock_game, result)
      mocked_handle_dice_result.reset_mock()


dice_faces = [
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