# Snake AI

Snake AI is a snake game solver, it works following a Hamiltonian Path and uses a heuristic function that allows the snake to take some shortcuts and guaranty to find a solution.

## How do I find a Hamiltonian Path in O(N) instead of O(N!)?
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

  
  and with a grid 5x5? It doesn't exist, and doesn't exist for any grid with odd height and width.

  So as you can see there is a pattern between the two Hamiltonian Cycles, the only difference is made by the height of the grid, which will change just the last two rows.

  ### Algorithm
  Every cell in the grid has an id, for example, the cell (i, j) with 0 < i <= h and 0 < j <= w has an id = i * w + j
  1. `path = [1 * w + 1]` insert the first element
  2. For each row starting from the first to the third last, insert the elements of the row (reverse the row if row_index % 2 == 1 in Python indexes starts from 0)
  3. If h % 2 == 0 then insert the penultimate row and then the reversed  last row
  4. else reverse and zip the two last rows and, then insert the elements of each tuple of the zip
  5. Insert the first column upside down excluding the first element

## How does the heuristic function work?
  Problems to solve:
  1. The snake can go in two directions.
  2. When the snake is eating food, he has to entirely be on the Hamiltonian path, in this way, we will solve the problem 100%.
  3. The snake has to take some shortcuts that don't let him die.
  4. The snake has to make as few movements as possible to eat the food

### Solutions
* If the Hamiltonian distance from the head to the food is lower or equal to the length of the snake, then we have to follow the Hamiltonian path (reversed or not).
* For each possible move we have to ensure that following the Hamiltonian path the snake will not die.
* We have to consider each direction for each possible move, which means that we can reverse the Hamiltonian path that you have seen before.
* The snake can move the head in 4 directions (up, down, right, left) and for each, we will take the shortest one to the food

## Visual Solution
https://github.com/i0nut02/Snake-AI/assets/99051485/3d13aa30-1e72-4706-a2c2-7b62e5238805



