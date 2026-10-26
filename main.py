from game import Game
from scenes import MainMenuScene

if __name__ == "__main__":
    game: Game = Game()

    game.SetScene( MainMenuScene() )

    while ( not game.ShouldExit() ):
        game.Update()
