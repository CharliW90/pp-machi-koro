import inquirer
from reference import MyTheme, welcome, help_text
from game import Game

def run_game(player_names: list[str]) -> None:
  game = Game(player_names)
  game.start()

def query_players() -> int:
  player_options = [inquirer.List('players', message=f"How many players?", choices=[("One vs PC", 1), ("Two", 2), ("Three", 3), ("Four", 4), ("Game Help", 'help'), ("Exit", 'exit')])]
  player_count = inquirer.prompt(player_options, theme=MyTheme('cyan', '?'))
  if player_count['players'] == 'exit': # type: ignore
    exit()
  if player_count['players'] == 'help': # type: ignore
    for text in help_text:
      print(text)
    return query_players()
  else:
    return int(player_count['players']) # type: ignore

def get_player_name(i: int) -> str:
  questions = [inquirer.Text('name', message=f"Player {i+1}, What's your name?")]
  answers = inquirer.prompt(questions)
  return answers['name'] # type: ignore

if __name__ == "__main__":
  print(welcome)
  players = query_players()
  if players == 1:
    raise NotImplementedError("Not yet implemented Bot logic to play against PC")
  names = [get_player_name(n) for n in range(players)]
  if len(names) == players:
    run_game(names)