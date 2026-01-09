import Game
import minimax
import State
import games

g = Game.Game()
g.step([3,2])
g.step([2,2])
g.step([1,2])
g.step([4,2])
g.step([5,4])
g.step([3,1])

#State.display(g.state)
#print("===================================")

#g.step(minimax.minimax(g, 1))

#State.display(g.state)

#g.displayAllActions()

#games.H()
games.methodical()
