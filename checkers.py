from tkinter import *
from copy import copy, deepcopy
from time import sleep


colors = ["red", "black"]

"""
Tablero:
0 -> colors[0] (red)
1 -> colors[1] (black) (user)
2 -> empty
"""

def utility_func(tablero):
    machine = 0
    user = 0
    for fila in tablero:
        for columna in fila:
            if columna == 0:
                machine += 1
            elif columna == 1:
                user += 1

    return machine-user

def get_possible_moves(tablero, turn):
    #turn = 0: AI 
    #turn = 1: user
    #just like their numbers

    moves = []

    for row in range(len(tablero)):
        for col in range(len(tablero[0])):
            if tablero[row][col] != turn:
                continue

            #possible moves:
            #[row+1][col+1]
            #[row+1][col-1]
            #[row-1][col+1]
            #[row-1][col-1]

            add = False
            
            if (row+1) <= 7 and (col+1) <= 7:
                if tablero[row+1][col+1] != turn:
                    cur_move = deepcopy(tablero)
                    if (cur_move[row+1][col+1] != 2): #eating
                        if (row+2 <= 7 and col+2 <= 7):
                            if (cur_move[row+2][col+2] == 2):
                                #position after eating: it's free
                                cur_move[row+2][col+2] = turn
                                cur_move[row+1][col+1] = 2
                                add = True
                    else:
                        cur_move[row+1][col+1] = turn
                        add = True
                    cur_move[row][col] = 2
                    if add:
                        moves.append(cur_move)

            add = False
            
            if (row+1) <= 7 and (col-1) >= 0:
                if tablero[row+1][col-1] != turn:
                    cur_move = deepcopy(tablero)
                    if (cur_move[row+1][col-1] != turn and cur_move[row+1][col-1] != 2): #eating
                        if (row+2 <= 7 and col-2 >= 0):
                            if (cur_move[row+2][col-2] == 2):
                                cur_move[row+2][col-2] = turn
                                cur_move[row+1][col-1] = 2
                                add = True
                    else:
                        cur_move[row+1][col-1] = turn
                        add = True
        
                    cur_move[row][col] = 2
                    if add:
                        moves.append(cur_move)

            add = False
                    
            if (row-1) >= 0 and (col+1) <= 7:
                if tablero[row-1][col+1] != turn:
                    cur_move = deepcopy(tablero)
                    if (cur_move[row-1][col+1] != turn and cur_move[row-1][col+1] != 2):
                        if (row-2 >= 0 and col+2 <= 7):
                            if cur_move[row-2][col+2] == 2:
                                cur_move[row-2][col+2] = turn
                                cur_move[row-1][col+1] = 2
                                add = True
                    else:
                        cur_move[row-1][col+1] = turn
                        add = True
                    cur_move[row][col] = 2
                    if add:
                        moves.append(cur_move)

            add = False
            
            if (row-1) >= 0 and (col-1) >= 0:
                if tablero[row-1][col-1] != turn:
                    cur_move = deepcopy(tablero)
                    if (cur_move[row-1][col-1] != turn and cur_move[row-1][col-1] != 2):
                        if (row-2 >= 7 and col-2 >= 0):
                            if cur_move[row-2][col+2] == 2:
                                cur_move[row-2][col-2] = turn
                                cur_move[row-1][col-1] = 2
                                add = True
                    else:
                        cur_move[row-1][col-1] = turn
                        add = True
                    cur_move[row][col] = 2
                    if add:
                        moves.append(cur_move)
            
    return moves

class Node():

    def __init__(self, data):
        self.data = data
        self.child = []
        self.utility = 0


def build_tree(cur_tablero, turn, cur_node, cur_level, max_level):
    if (cur_level >= max_level):
        return

    #getting childs
    cur_level_moves = get_possible_moves(cur_tablero, turn)
    
    for cur_move in cur_level_moves:
        cur_child = Node(cur_move)
        cur_child.utility = utility_func(cur_child.data)
        cur_node.child.append(cur_child) #storing childs

        if turn == 0:
            turn = 1
        else:
            turn = 0

    for child in cur_node.child: #recursively creating other childs
        cur_node = child
        build_tree(child.data, turn, cur_node, cur_level+1, max_level)
        


class Tree():

    def __init__(self):
        self.root = None

    def build(self, tablero, levels):

        turn = 0
        self.root = Node(tablero)
        cur_node = self.root
        cur_tablero = tablero
        cur_node.utility = utility_func(cur_node.data)

        build_tree(cur_tablero, turn, cur_node, 0, levels)
            

def get_min_or_max(cur_father, mm): #mm = 0, min; 1, max
    values = []
    for child in cur_father.child:
        values.append(utility_func(child.data))

    if (mm == 0):
        mini = min(values)
        return (mini, values.index(mini))
    else:
        maxi = max(values)
        return (maxi, values.index(maxi))

    

def min_max(node, level, mm):
    
    if (level == 0) or len(node.child) == 0:
        return node.utility

    values = []
    for child in node.child:
        values.append(child.utility)

    if mm == 0:

        value = -9999
        
        for i in range(len(node.child)): #for all childs
            
            value = max(value, min_max(node.child[i], level-1, 1))

        return value
    
    else:

        value = 9999

        for i in range(len(node.child)):
            value = min(value, min_max(node.child[i], level-1, 0))

        return value

        
class Ficha():
    def __init__(self, color):
        self.color = colors[color]

    def draw(self, x,y):
        fcha = Canvas(bg = self.color, height = 15, width = 15)
        fcha.grid(row = x, column = y)


class Tablero():
    def __init__(self):
        self.tablero = [ [2 for i in range(8)] for j in range(8) ]

        for i in range(0,8,2):
            #red thingies
            self.tablero[0][i+1] = 0
            self.tablero[1][i] = 0
            self.tablero[2][i+1] = 0
            
            #black thingies
            self.tablero[5][i] = 1
            self.tablero[6][i+1] = 1
            self.tablero[7][i] = 1

        self.cur_play = False
        self.click_positions = [ 0,0 ] #pos_1, pos_2

    def play(self, row, col, difficulty):
        if not self.cur_play:
            if (self.tablero[row][col] != 1):
                print(str(row) + " row, col: " + str(col))
                print(str(self.tablero[row][col]))
                print("Not your piece!")
                return

            self.click_positions[0] = row
            self.click_positions[1] = col
            self.cur_play = True
        else:
            if (self.tablero[row][col] == 1):
                print("Not a valid position, try again!")
                self.click_positions = [ 0,0 ] #pos_1, pos_2
                self.cur_play = False
                return
            
            row_1 = self.click_positions[0]
            col_1 = self.click_positions[1]

            st_1 = row_1 == row+1 and col_1 == col+1
            st_2 = row_1 == row-1 and col_1 == col+1
            st_3 = row_1 == row-1 and col_1 == col-1
            st_4 = row_1 == row+1 and col_1 == col-1

            final_st = st_1 or st_2 or st_3 or st_4

            if not final_st:
                print("Not a valid move. Try again.")
                self.click_positions = [ 0,0 ] #pos_1, pos_2
                self.cur_play = False
                return
            st_5 = True

            if st_1:
                print("Statement1")
            
            if st_2:
                print("Statement2")
            
            if (st_3):
                print("Statement3")

            if st_4:
                print("Statement4")
            
            if self.tablero[row][col] == 0: #enemy
                print("col: " + str(col_1) + ", row: " + str(row_1))
                if st_3 and row_1+2 <= 7 and col_1+2 <= 7:
                    print("Condition1")
                    if self.tablero[row_1+2][col_1+2] == 2:
                        self.tablero[row_1][col_1] = 2
                        self.tablero[row][col] = 2
                        self.tablero[row+1][col+1] = 1
                        st_5 = False
                elif st_4 and row_1-2 >= 0 and col_1+2 <= 7:
                    print("Condition2")
                    if self.tablero[row_1-2][col_1+2] == 2:
                        self.tablero[row_1][col_1] = 2
                        self.tablero[row][col] = 2
                        self.tablero[row-1][col+1] = 1
                        st_5 = False
                elif st_1 and row_1-2 >= 0 and col_1-2 >= 0:
                    print("Condition3")
                    if self.tablero[row_1-2][col_1-2] == 2:
                        self.tablero[row_1][col_1] = 2
                        self.tablero[row][col] = 2
                        self.tablero[row-1][col-1] = 1
                        st_5 = False
                elif st_2 and row_1+2 <= 7 and col_1-2 >= 0:
                    print("Condition4")
                    if self.tablero[row_1+2][col_1-2] == 2:
                        self.tablero[row_1][col_1] = 2
                        self.tablero[row][col] = 2
                        self.tablero[row+1][col-1] = 1
                        st_5 = False
                elif st_5:
                    print("Not a valid move. Try again.")
                    self.click_positions = [ 0,0 ] #pos_1, pos_2
                    self.cur_play = False
                    return

            else:
                self.tablero[row_1][col_1] = 2
                self.tablero[row][col] = 1

            self.click_positions = [ 0,0 ] #pos_1, pos_2
            self.cur_play = False
            print("Piece moved.")

            #self.draw()
            
            print(utility_func(self.tablero))
            print("Cur difficulty: " + str(difficulty))

            #sleep(5)

            ###minmax calculations

            cur_tree = Tree()
            cur_tree.build(self.tablero, difficulty)
            
            cur_value = min_max(cur_tree.root, difficulty, 0)

            for child in cur_tree.root.child:
                if child.utility == cur_value:
                    self.tablero = child.data
                    break
                        
            self.draw()

    def draw_fichas(self):
        for fila in range(8):
            for columna in range(8):
                if (self.tablero[fila][columna] != 2):
                    temp_ficha = Ficha(self.tablero[fila][columna])
                    temp_ficha.draw(fila, columna)

    def draw(self):
        #difficulty = Scale(from_=1, to=10,orient=HORIZONTAL)
        #difficulty.set(1)
        #difficulty.grid(row=9,column=0,columnspan=8)
        
        for fila in range(8):
            for columna in range(8):
                bt = Button()
                if fila % 2 == 0:
                    if columna % 2 == 0:
                        bt = Button(bg = "white")
                    else:
                        bt = Button(bg = "brown")
                else:   
                    if columna % 2 == 0:
                        bt = Button(bg = "brown")
                    else:
                        bt = Button(bg = "white")
                bt.configure(activebackground = "gray", height = 3,
                     width = 3, command = lambda x = fila, y = columna:
                             self.play(x, y, difficulty.get()))
                bt.grid(row = fila, column = columna)

        print("Buttons drawed")

        self.draw_fichas()

root = Tk()

tablero = Tablero()
tablero.draw()

difficulty = Scale(from_=1, to=10,orient=HORIZONTAL)
#difficulty.set(1)
difficulty.grid(row=9,column=0,columnspan=8)


root.mainloop()
