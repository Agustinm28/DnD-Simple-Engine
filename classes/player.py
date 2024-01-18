class Player:

    def __init__(self, name, player, race, subrace, background, player_class, level, description):
        self.name = name
        self.player = player
        self.race = race
        self.subrace = subrace
        self.background = background
        self.player_class = player_class
        self.level = level
        self.description = description

    def __str__(self):
        return f"Player {self.player} who's character is {self.name} is a {self.race}, {self.subrace}, {self.background}, {self.player_class}, Level {self.level}, {self.description}"