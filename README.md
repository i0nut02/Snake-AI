# Snake AI

Snake AI is a snake game solver, it works following a Hamiltonian Path and uses a heuristic function that allows the snake to take some shortcuts and guaranty to find a solution.

# How do I find a Hamiltonian Path in O(N) instead of O(N!)?
  I just found a pattern and defined an algorithm that works with grid graphs, you can also find a different solution in this [paper](https://www.researchgate.net/publication/220616693_Hamilton_Paths_in_Grid_Graphs)

  So let's show how a Hamiltonian Cycle with a grid 4x5

  |   | 1 | 2 | 3 | 4 |
  |:-:|:-:|:-:|:-:|:-:|
  | 1 | → | → | → | ↓ |
  | 2 | ↑ | ↓ | ← | ← |
  | 3 | ↑ | → | → | ↓ |
  | 4 | ↑ | ↓ | ← | ↓ |
  | 5 | ↑ | ← | ↑ | ← |

  Now with a grid 4x4

  |   | 1 | 2 | 3 | 4 |
  |:-:|:-:|:-:|:-:|:-:|
  | 1 | → | → | → | ↓ |
  | 2 | ↑ | ↓ | ← | ← |
  | 3 | ↑ | → | → | ↓ |
  | 4 | ↑ | ← | ← | ← |

  
  and with a grid 5x5? It doesn't exist, and probably doesn't exist for any grid with odd height and width

  So as you can see there is a pattern between the two Hamiltonian Cycles, the only difference is made by the height of the grid, which will change just the last two rows

# How does the heuristic function work?
