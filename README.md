# Algorithmic Solution for EDGe
The program included in the repository is the primary companion code of that included in _The Edge-Distinguishing Game_. Given an adjacency list, the program will determine which player will win the game EDGe if they play perfectly. Using an interface which allows for cells, it can be used to play the game and determine the exact moves needed to win the game. 

Here we provide a description of the inputs needed for the program as well as the interpretation of the output. 

Note: Two version of the code are included in this repository. We suggest using the Jupyter Notebook, or something similar, for interactive play with the game; however, in general, the kernal will die if a graph has more than 9 vertices. In that case we suggest running the python file through the desired IDE.

Labeling and Entering the Graph:
-------------------------------
Before entering the graph, draw a picture of the figure and label as follows:
1. For the desired graph, begin at either the uppermost, leftmost, or upper leftmost vertex and label that vertex with "a"
2. Continue _clockwise_ around the figure labeling the vertices in ascending alphabetical order from the outermost vertices to the inside vertices

Once the graph is labeled, create the adjacency list as follows:
1. Create a list with as many entries as there are vertices, with each entry being a list (each list within the larger list represents a vertex).
2. Within each list, list the "names" of the adjacent vertices. For example, if I have a graph with three vertices "a", "b", and "c" in a line, the corresponding adjacency list would be [["b"], ["a","c"],["b"]]. Both of the ends have only one entry ("b") beccause they are only connected to the middle vertex.

Entering the EDCN:
-----------------
The program requires the edge-distinguishing chromatic number (EDCN) of the graph to be entered as a constant. If the value of the EDCN for a graph is known, it can be entered. If it is not known, refer to the other program mentioned in the references of _The Edge-Distinguishing Game_ to determine the EDCN, then enter it. 

Output:
------
The first thing that will be printed is a statement of which player has the winning strategy. The next will be every possible move Player 1 can make from the empty board. The tuple on the left is the current state of the board while the right tuple is the move a player can make. The entries in the tuple are ordered the same way as they are in the adjacency list, so the first entry should be vertex "a" and so on till the end is reached. The object of both players is to make a move that is labeled with a "p". Whichever player does this first ensures they will win the game regardless of the move made by the oppposing player. Every subsequent move by the winning player should be on a board labeled "p".  

If desired, the program can be used to show the exact series of moves needed to win. To do this, the value _tuple(empty_board)_ in se second to last cell should be replaced with the desired board. The board will be the second tuple in the printed list. 

The final cell of the program will generate an image of the directed graph used to determine the winning strategy. 

Versions:
--------
python - 3.12.1

networkx - 3.3

matplotlib - 3.8.3
