import string as st
import itertools as it 
import networkx as nx
import matplotlib.pyplot as plt


EDCN = 3

ADJACENCY_LIST = [["b"],["a","c"],["b","d"],["c","e"],["d"]]
possible_boards_list = []

legal_boards = []
legal_boards_list = []

playable_boards = []
unplayable_boards = []

playable_boards_list = []
unplayable_boards_list = []

COLORS = []
MOVES = []
COLORS.append(-1)

#  Adding all the colors based off of the EDCN starting at 1
for i in range(1,EDCN+1):
    COLORS.append(i)
    MOVES.append(i)


#  Makes the blank boards    
def possible_boards(board): 
    inter_board = {}
    vertices = []
    
    for i, j in zip(board, st.ascii_letters):
        inter_board[j] = [0, i]
        vertices.append(j)
    
    return inter_board  


#  Generate the possible colorings for every board 
def make_boards(adj_list, colors):               
    global possible_boards_list

    #  Create all of the permutations of the board colorings
    for possible_coloring in it.product(colors, repeat=len(adj_list)):
        board = possible_boards(ADJACENCY_LIST)
        for index, vertex in enumerate(board):
            board[vertex][0] = possible_coloring[index]
    
        possible_boards_list.append(board)
    
    return 


#  Remove all boards with illegal edge colorings
def no_repeat_edges(edges):           
    no_repeats = True
    
    for side in edges:  
        #  Allow for the empty board
        if side == [-1,-1] and (edges.count(side) == len(edges)):
            return True 

        #  Edges only appearing once are legal 
        elif edges.count(side) == 1:
            continue

        elif edges.count(side) > 1:
            #  Allow for repeated colorings if one of the vertices is uncolored
            if -1 in side: 
                continue  

            #  Allow for a double edge if it is a color next to itself
            elif side[0] == side[-1]: 
                if edges.count(side) <= 2:
                    continue
                else:               
                    return False 

            #  Return False for any other case
            else:
                return False  

    # Returns True for all boards without a repeated edge
    if no_repeats == True:   
        return True


#  Determine if a board is legal with the repeat edges function 
def is_safe(board): 
    edges = []
    vertices = []

    #  Create the edge list by iterating through the vertices and pairing the vertex color with the color of the adjacent vertices
    for vertex in board:
        vertices.append(board[vertex][0])
        for i in range(len(board[vertex][1])):
            edges.append([board[vertex][0], board[board[vertex][1][i]][0]])
            
    #  Will return true if the board is legal
    if no_repeat_edges(edges):
        return True 

    return False


#  Return True for all boards which are PLAYABLE
def terminating_board(board, color_list):        
    value = board.values()
    board_color = []
    
    for entry in value:
        board_color.append(entry[0])

    #  All fully colored boards are terminating
    if -1 not in board_color:
        return False

    #  If a board is not fully colored, check the uncolored vertices to see if they are markable
    for vertex in board:  
        if board[vertex][0] != -1:
            continue
        else:
            for color in color_list:   
                board[vertex][0] = color 
                if is_safe(board):
                    board[vertex][0] = -1 
                    return True   
                else:
                    board[vertex][0] = -1
                    continue

    #  Return False for all terminating boards
    return False


#  Will "play" the whole game and make the game states
def play_game(adj_list, colors):                 
    global possible_boards_list
    global vertex_list
    global legal_boards
    global unplayable_boards
    global playable_boards
    global legal_boards_list
    global playable_boards_list 
    global unplayable_boards_list
    global MOVES
    
    make_boards(adj_list, colors)  
    
    for board in possible_boards_list:
        if is_safe(board):  
            legal_boards.append(board)
            
    for board in legal_boards:    
        if terminating_board(board, MOVES):
            playable_boards.append(board)
        else:
            unplayable_boards.append(board)

    #  Changing all the dictionaries into lists of vertex colors 
    for board in playable_boards: 
        temp_board = []
        for vertex in board:
            temp_board.append(board[vertex][0])
            
        playable_boards_list.append(temp_board)
    
    for board in unplayable_boards:
        temp_board = []
        for vertex in board:
            temp_board.append(board[vertex][0])
        
        unplayable_boards_list.append(temp_board)
        
    legal_boards_list.extend(playable_boards_list)
    legal_boards_list.extend(unplayable_boards_list)
    
    return

#  Call the function 
play_game(ADJACENCY_LIST, COLORS)


empty_board = []
for i in range(len(legal_boards_list[0])):
    empty_board.append(-1)

#  Initialize the DiGraph
digraph = nx.DiGraph()
board_moves = [[]] 

for i in range(len(ADJACENCY_LIST)):
    board_moves.append([])

#  Sort the board by how many vertices have been colored i.e. moves
for board in legal_boards_list:  
    vertex_colors = 0
    for vertex in board:
        if vertex != -1:
            vertex_colors += 1 
    
    board_moves[vertex_colors].append(board)
    
    #  Add boards to digraph and indicate whether they are in an end position "p"
    if board in playable_boards_list:
        digraph.add_node(tuple(board), position = "", layer = vertex_colors)
    else: 
        digraph.add_node(tuple(board), position = "p", layer = vertex_colors)


for i in range(len(legal_boards_list[0])):
    for board in board_moves[i]:
    
        #  Make edges in the digraph based on the next move 
        if digraph.nodes[tuple(board)]["position"] == "":

            #  Check possible moves from a board to another in the next layer
            for i in range(len(board)):
                if board[i] == -1:
                    game_state = list(board)

                    for move in MOVES:
                        game_state[i] = move
                        
                        #  Make all of the edges in the DiGraph
                        if tuple(game_state) in digraph.nodes:
                            digraph.add_edge(tuple(board), tuple(game_state))


#  Label nodes in the digraph as n and p positions starting at the end of the game
for i in range(len(legal_boards_list[0])+1):
    for board in board_moves[len(board_moves)-i-1]:
        if (digraph.in_degree(tuple(board)) == 0) and (i != len(board_moves)-1):
            turns = 0 
            for entry in board:
                if entry != 0:
                    turns += 1
            digraph.remove_node(tuple(board))
        
        #  A P-position if in an end state
        elif len(digraph.edges(tuple(board))) == 0:
            digraph.nodes[tuple(board)]["position"] = "p"
        
        else:
            for edge in digraph.edges(tuple(board)):
                if digraph.nodes[edge[1]]["position"] == "p":
                    digraph.nodes[tuple(board)]["position"] = "n"

            #P-position if only directed to N-positions
            if digraph.nodes[tuple(board)]["position"] == "":
                digraph.nodes[tuple(board)]["position"] = "p" 



#  Determine which player has a winning strategy
if digraph.nodes[tuple(empty_board)]["position"] == "n":
    print("Player 1 has a winning strategy")
else:
    print("Player 2 has a winning strategy")


#  Print possible moves based on board
for edge in digraph.edges(tuple(empty_board)):
    print(edge, "\t", digraph.nodes[edge[1]]["position"])


#Uncomment the following code to download an image of directed graph
#drawing = nx.multipartite_layout(digraph, subset_key="layer")
#color_map = [(255/255, 184/255, 28/255) if digraph.nodes[node]["position"] == "p" else (65/255, 65/255, 65/255) for node in digraph] 
#nx.draw_networkx(digraph, pos=drawing, node_size = 50, with_labels=False, node_color= color_map)

#plt.savefig("P_5digraph.png")
