import pytest
from game import Game

onePlayer = ['A']
twoPlayer = [*onePlayer, 'B']
threePlayer = [*twoPlayer, 'C']
fourPlayer = [*threePlayer, 'D']
fivePlayer = [*fourPlayer, 'E']
bankTemplate = [42, 24, 12]
cashTemplate = [42, 120, 120]
coloursTemplate = ['red','green','blue','purple', 'orange', 'yellow', 'cyan']

class TestGameClass:
  def test_one_player(self):
    # Arrange
    players = onePlayer

    # Act / Assert
    with pytest.raises(ValueError):
      Game(players)

  def test_two_players(self):
    # Arrange
    players = twoPlayer

    # Act
    test = Game(players)

    # Assert
    assert hasattr(test, 'name')
    assert test.name == "Machi Koro"

    assert hasattr(test, 'playerCount')
    assert test.player_count == 2

    assert hasattr(test, 'players')
    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]
    
    assert hasattr(test, 'bank')
    assert test.bank.total == 282
    for i, stack in enumerate(test.bank.coins):
      assert len(stack) == bankTemplate[i]
      assert sum(coin.value for coin in stack) == cashTemplate[i]
    
    assert hasattr(test, 'deck')

    assert hasattr(test, 'round')

    assert hasattr(test, 'limitRounds')

    assert hasattr(test, 'notify')

    assert hasattr(test, 'listAffordableCards')

    assert hasattr(test, 'displayCardsToPlayer')

    assert hasattr(test, 'takeCardFromStack')

    assert hasattr(test, 'start')

    assert hasattr(test, 'play')
    
    assert hasattr(test, 'endGame')
    test.end_game()

  def test_three_players(self):
    # Arrange
    players = threePlayer

    # Act
    test = Game(players)

    # Assert
    assert hasattr(test, 'name')
    assert test.name == "Machi Koro"

    assert hasattr(test, 'playerCount')
    assert test.player_count == 3

    assert hasattr(test, 'players')
    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]
    
    assert hasattr(test, 'bank')
    assert test.bank.total == 282
    for i, stack in enumerate(test.bank.coins):
      assert len(stack) == bankTemplate[i]
      assert sum(coin.value for coin in stack) == cashTemplate[i]
    
    assert hasattr(test, 'deck')

    assert hasattr(test, 'round')

    assert hasattr(test, 'limitRounds')

    assert hasattr(test, 'notify')

    assert hasattr(test, 'listAffordableCards')

    assert hasattr(test, 'displayCardsToPlayer')

    assert hasattr(test, 'takeCardFromStack')

    assert hasattr(test, 'start')

    assert hasattr(test, 'play')

    assert hasattr(test, 'endGame')
    test.end_game()
  
  def test_four_players(self):
    # Arrange
    players = fourPlayer

    # Act
    test = Game(players)

    # Assert
    assert hasattr(test, 'name')
    assert test.name == "Machi Koro"

    assert hasattr(test, 'playerCount')
    assert test.player_count == 4

    assert hasattr(test, 'players')
    for i, player in enumerate(test.players):
      assert player.name == players[i]
      assert player.colour == coloursTemplate[i]
    
    assert hasattr(test, 'bank')
    assert test.bank.total == 282
    for i, stack in enumerate(test.bank.coins):
      assert len(stack) == bankTemplate[i]
      assert sum(coin.value for coin in stack) == cashTemplate[i]
    
    assert hasattr(test, 'deck')

    assert hasattr(test, 'round')

    assert hasattr(test, 'limitRounds')

    assert hasattr(test, 'notify')

    assert hasattr(test, 'listAffordableCards')

    assert hasattr(test, 'displayCardsToPlayer')

    assert hasattr(test, 'takeCardFromStack')

    assert hasattr(test, 'start')

    assert hasattr(test, 'play')

    assert hasattr(test, 'endGame')
    test.end_game()

  def test_five_players(self):
    # Arrange
    players = fivePlayer

    # Act / Assert
    with pytest.raises(ValueError):
      Game(players)