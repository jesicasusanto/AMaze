# AMaze
A maze solver using Djikstra's algorithm and generator using recursive backtracking.

The AMaze is generated with recursive backtracking. Using the Stack abstract data structure, the Maze Generator chooses randomly the node's top, bottom, left, or right neighbor to be appended to the Stack.

Using the Djikstra's algorithm, AMaze finds the shortest path between two nodes by calculating the minimum cost to travel to all possible direction. The Queue abstract data structure kepps track of the shortest path and trace the path backwards after reaching the final destination.

