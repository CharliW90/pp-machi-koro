import pytest
from game import Game
from player import reset as reset_player_names

onePlayer = ['A']
twoPlayer = [*onePlayer, 'B']
threePlayer = [*twoPlayer, 'C']
fourPlayer = [*threePlayer, 'D']
fivePlayer = [*fourPlayer, 'E']
bankTemplate = [42, 24, 12]
cashTemplate = [42, 120, 120]
coloursTemplate = ['red','green','blue','purple', 'orange', 'yellow', 'cyan']

def assess_game_class(game):
  assert hasattr(game, 'name')
  assert game.name == "Machi Koro"
  assert hasattr(game, 'player_count')
  assert hasattr(game, 'players')
  assert hasattr(game, 'bank')
  assert game.bank.total == 282
  for i, stack in enumerate(game.bank.coins):
    assert len(stack) == bankTemplate[i]
    assert sum(coin.value for coin in stack) == cashTemplate[i]
  assert hasattr(game, 'deck')
  assert hasattr(game, 'round')
  assert hasattr(game, 'notify')
  assert hasattr(game, 'list_affordable_cards')
  assert hasattr(game, 'display_cards_to_player')
  assert hasattr(game, 'take_card_from_stack')
  assert hasattr(game, 'current_player')
  assert hasattr(game, 'start')
  assert hasattr(game, 'play')
  assert hasattr(game, 'end_game')

class TestGameClass:
  def test_one_player(self):
    reset_player_names()
    # Arrange
    players = onePlayer

    # Act / Assert
    with pytest.raises(ValueError):
      Game(players)

  def test_two_players(self):
    reset_player_names()
    # Arrange
    players = twoPlayer

    # Act
    test = Game(players)

    # Assert
    assess_game_class(test)
    assert test.player_count == 2

    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]

  def test_three_players(self):
    reset_player_names()
    # Arrange
    players = threePlayer

    # Act
    test = Game(players)

    # Assert
    assess_game_class(test)
    assert test.player_count == 3

    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]
  
  def test_four_players(self):
    reset_player_names()
    # Arrange
    players = fourPlayer

    # Act
    test = Game(players)

    # Assert
    assess_game_class(test)
    assert test.player_count == 4

    assert hasattr(test, 'players')
    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]

  def test_five_players(self):
    reset_player_names()
    # Arrange
    players = fivePlayer

    # Act / Assert
    with pytest.raises(ValueError):
      Game(players)