from inquirer.themes import Default, term

rgb_colours = {
  'red': [208,0,0],
  'green': [0,208,0],
  'blue': [0,0,208]
}

rgb_colours['cyan'] = [b+g for b, g in zip(rgb_colours['blue'], rgb_colours['green'])]
rgb_colours['yellow'] = [r+g for r, g in zip(rgb_colours['red'], rgb_colours['green'])]
rgb_colours['magenta'] = [r+b for r, b in zip(rgb_colours['red'], rgb_colours['blue'])]

rgb_colours['crashmat_blue'] = [b+int(g/2) for b, g in zip(rgb_colours['blue'], rgb_colours['green'])]
rgb_colours['orange'] = [r+int(g/2) for r, g in zip(rgb_colours['red'], rgb_colours['green'])]
rgb_colours['pink'] = [r+int(b/2) for r, b in zip(rgb_colours['red'], rgb_colours['blue'])]

rgb_colours['teal'] = [g+int(b/2) for g, b in zip(rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['lime'] = [g+int(r/2) for g, r in zip(rgb_colours['green'], rgb_colours['red'])]
rgb_colours['purple'] = [b+int(r/2) for b, r in zip(rgb_colours['blue'], rgb_colours['red'])]

rgb_colours['crashmat_blue_faded'] = [b+int(g/2.5)+int(r/3) for b, g, r in zip(rgb_colours['blue'], rgb_colours['green'], rgb_colours['red'])]
rgb_colours['orange_faded'] = [r+int(g/2.5)+int(b/3) for r, g, b in zip(rgb_colours['red'], rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['pink_faded'] = [r+int(b/2.5)+int(g/3) for r, b, g in zip(rgb_colours['red'], rgb_colours['blue'], rgb_colours['green'])]

rgb_colours['teal_faded'] = [int(g/2)+int(b/2) for g, b in zip(rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['lime_faded'] = [int(g/2)+int(r/2) for g, r in zip(rgb_colours['green'], rgb_colours['red'])]
rgb_colours['purple_faded'] = [int(b/2)+int(r/2) for b, r in zip(rgb_colours['blue'], rgb_colours['red'])]

ansi_colours = {colour: f"\033[38;2;{';'.join(str(x) for x in rgb_colours[colour])};74m" for colour in rgb_colours}
ansi_colours['reset'] = f"\033[39m"

hex_colours = {colour: '#%02x%02x%02x' % (*rgb_colours[colour],) for colour in rgb_colours}

shortcuts = {
  'notification_start': f"{ansi_colours['yellow']}==> ",
  'notification_end': f"{ansi_colours['reset']}\n",
  'unaffordable': "\x1b[9;2m",
  'affordable': "\x1b[3;32m",
  'reset': "\x1b[0m",
  'blink_start': "\033[5m",
  'blink_end': "\033[0m"
}

reference = {"rgb_colours": rgb_colours, "ansi_colours": ansi_colours, "hex_colours": hex_colours, "shortcuts": shortcuts}

class MyTheme(Default):
  def __init__(self, player):
    super().__init__()
    self.Question.mark_color = term.color_rgb(*rgb_colours[player.colour]) # type: ignore
    self.Question.brackets_color = term.color_rgb(*rgb_colours[player.colour]) # type: ignore
    self.Question.default_color = term.on_color_rgb(*rgb_colours[player.colour]) # type: ignore
    self.List.selection_color = term.on_color_rgb(*rgb_colours[player.colour]) # type: ignore
    self.List.selection_cursor = f"{player.name} =>" # type: ignore