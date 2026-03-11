# Graph Operator
A graph theory visualisation tool where users can construct graphs to represent real-world road networks
or to improve their understanding of this area of discrete mathematics.

The user can implement Dijkstra's algorithm and the nearest neighbour algorithm on their constructed graph,
used to respectively find the shortest path from one node to another and to find the shortest path to traverse
all nodes.

## Features
### Graph Construction
- Vertices
  - Allows for custom naming
  - Prevents duplicate vertex names
- Arcs
  - Accepts positive numeric inputs for arc weight (incl. decimals)
  - Supports simultaneous directed & undirected arcs
  - Can add two arcs between two vertices heading opposite directions
  - Prevents the adding of multiple arcs between two vertices

### Dijkstra's Algorithm & the Nearest Neighbour Algorithm
Computational methods derived from manual mathematical methods
- Now accounts for multiple optimal paths that share identical total weights
  - Such paths are now replayable and selectable from a list
- Can handle graphs with directed arcs
- Detects unreachable paths
- Handles multiple edge-cases

## Technologies
- Python
- PyQt6 (the user interface)

## Status
- Development: started 2025 (age 17); in progress
  - Dijkstra's algorithm - completed, tested and verified; now fully adapted for UI interaction
  - Nearest neighbour algorithm - completed, tested and verified; now fully adapted for UI interaction
  - User interface - main function complete (future features to come)
