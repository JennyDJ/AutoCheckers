from pymouse import PyMouseEvent
import tkinter as tk
import random

xcoor = None
ycoor = None

class GameBoard(tk.Frame,PyMouseEvent):
    def __init__(self, parent):  # CONSTRUCTOR
         # initialise constants and variables
        self.ROWS = 8
        self.COLUMNS = 8
        self.SQUARE_SIZE = 50
        self.COLOUR1 = "white"
        self.COLOUR2 = "black"
        self.Pieces = {}
        self.Circles={}
        self.Player1=None
        self.Player2=None
        self.WhichTurn=None
        self.button =None
        self.label = None
        self.dropDown = None
        self.popUpMenu =None
        self.player1Pieces = 12
        self.player2Pieces = 12
        self.AIPlayer1 = False
        self.AIPlayer2 =False

        # calculates the size that the canvas needs to be based on the size of the squares and the number of rows and columns
        canvas_width = self.COLUMNS * self.SQUARE_SIZE
        canvas_height = self.ROWS * self.SQUARE_SIZE

        PyMouseEvent.__init__(self) # initialises the pymouse event in the class

        tk.Frame.__init__(self, parent)
        # creates canvases in the given frame
        self.Canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,width=canvas_width, height=canvas_height)
        self.Canvas.grid(column = 1,row=1,rowspan =400,columnspan=400)

        self.buttonCanvas = tk.Canvas(self,borderwidth=0, highlightthickness=0,width=3, height=3)
        self.buttonCanvas.grid(column = 450,row=1,rowspan =10,columnspan=10,padx=10,pady=10)


    def new_board(self):  # draws the board using tkinter
        colour = self.COLOUR2
        for row in range(self.ROWS):
            colour = self.COLOUR1 if colour == self.COLOUR2 else self.COLOUR2
            for col in range(self.COLUMNS):
                x1 = (col * self.SQUARE_SIZE)
                y1 = (row * self.SQUARE_SIZE)
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                self.Canvas.create_rectangle(x1, y1, x2, y2, outline=colour, fill=colour, tags="square")
                self.Pieces[row,col]=[Piece(self.Circles),colour,colour,False]  # instantiates the pieces objects
                self.Pieces[row,col][0].create_new_piece(row,col,x1,x2,y1,y2,self.Canvas,colour)
                colour = self.COLOUR1 if colour == self.COLOUR2 else self.COLOUR2
        # creates the start button
        self.button = tk.Button(self.buttonCanvas,text="Press to start", command=lambda: self.set_players())
        self.button.grid(row =1, column = 1)

    def set_initial_pieces(self):  # sets circles and pieces in the start places
        turn = 1
        for i in range (0,3):
            if i ==1:
                for j in range(0,8,2):
                    self.Pieces[j, i][0].change_piece_colour(self.Canvas, turn, self.Circles, j, i,self.COLOUR2)
                    self.Pieces[j, i][1]= str(turn)
            else:
                for j in range(1,8,2):
                    self.Pieces[j, i][0].change_piece_colour(self.Canvas, turn, self.Circles, j, i,self.COLOUR2)
                    self.Pieces[j, i][1] = str(turn)

        turn = 2
        for i in range (5,8):
            if i ==6:
                for j in range(1,8,2):
                    self.Pieces[j, i][0].change_piece_colour(self.Canvas, turn, self.Circles, j, i,self.COLOUR2)
                    self.Pieces[j, i][1] = str(turn)
            else:
                for j in range(0,8,2):
                    self.Pieces[j, i][0].change_piece_colour(self.Canvas, turn, self.Circles, j, i,self.COLOUR2)
                    self.Pieces[j, i][1] = str(turn)

    def set_players(self):
        # creates drop down lists to select the type of player
        self.button.destroy()
        self.label = tk.Label(self.buttonCanvas, text="Select Player 1")
        self.label.grid(row=1, column=1)
        self.dropDown = tk.StringVar(self.buttonCanvas)
        popUpMenu = tk.OptionMenu(self.buttonCanvas,self.dropDown,"Human Player","AI Player")
        popUpMenu.grid(row=10, column=1)

        label2 = tk.Label(self.buttonCanvas,text = "Select Player 2")
        label2.grid(row=20,column=1)
        dropDown2 = tk.StringVar(self.buttonCanvas)
        popUpMenu2 = tk.OptionMenu(self.buttonCanvas, dropDown2, "Human Player", "AI Player")
        popUpMenu2.grid(row=40, column=1)
        self.button = tk.Button(self.buttonCanvas, text="ENTER", command=lambda: self.get_player_options(dropDown2,label2,popUpMenu,popUpMenu2))
        self.button.grid(row=60, column=1)

    def get_player_options(self,dropDown2,label2,popUpMenu,popUpMenu2):
        # instantiates the players based on the drop down option selected
        confirmation = True
        if self.dropDown.get() == "Human Player":
            self.Player1 = HumanPlayer(1)
        elif self.dropDown.get() == "AI Player":
            self.Player1 = ArtificailIntelligencePlayer(1,self.ROWS,self.COLUMNS)
            self.AIPlayer1 = True
        else:
            confirmation = False
        if dropDown2.get() == "Human Player":
            self.Player2 = HumanPlayer(2)
        elif dropDown2.get() == "AI Player":
            self.Player2 = ArtificailIntelligencePlayer(2,self.ROWS,self.COLUMNS)
            self.AIPlayer2 = True
        else:
            confirmation = False
        popUpMenu.destroy()
        popUpMenu2.destroy()
        self.label.destroy()
        label2.destroy()
        self.button.destroy()
        if confirmation == True:  # if the two players have been confirmed and instantiated start the game
            self.start_game()
        elif confirmation == False:
            self.set_players()

    def start_game(self):  # set up the first move
        self.WhichTurn = 1
        self.label = tk.Label(self.buttonCanvas,text ="Player 1 (gold) moves first")
        self.label.grid(row =1, column = 1)
        self.button = tk.Button(self.buttonCanvas, text="Press to select piece", command=lambda: self.select_piece_to_move(1))
        self.button.grid(row=10, column=1)

    def make_next_turn(self):  # based on whose turn it is the next move is set up
        if self.WhichTurn == 1:
            self.label.destroy()
            self.label = tk.Label(self.buttonCanvas, text="Player 2 (grey) moves")
            self.label.grid(row=1, column=1)
            self.button.destroy()
            self.button = tk.Button(self.buttonCanvas, text="Press to select piece", command=lambda: self.select_piece_to_move(2))
            self.button.grid(row=10, column=1)
            self.WhichTurn = 2
        else:
            self.label.destroy()
            self.label = tk.Label(self.buttonCanvas, text="Player 1 (gold) moves")
            self.label.grid(row=1, column=1)
            self.button.destroy()
            self.button = tk.Button(self.buttonCanvas, text="Press to select piece", command=lambda: self.select_piece_to_move(1))
            self.button.grid(row=10, column=1)
            self.WhichTurn = 1

    def select_piece_to_move(self,player):
        self.button.destroy()
        if player == 1:  # get the position of the piece the player will move
            condition, x, y = self.Player1.make_move(self.Pieces, self.Canvas, self.Circles, self.COLOUR1, self.COLOUR2,self.buttonCanvas)
        elif player == 2:
            condition, x, y = self.Player2.make_move(self.Pieces, self.Canvas, self.Circles, self.COLOUR1, self.COLOUR2,self.buttonCanvas)
        if condition == "ERROR":  # if the position is not valid, repeat and get another position
            self.label.destroy()
            self.label = tk.Label(self.buttonCanvas, text="ERROR wrong piece selected try again")
            self.label.grid(row=1, column=1)
            self.button = tk.Button(self.buttonCanvas, text="Press to select piece", command=lambda: self.select_piece_to_move(player))
            self.button.grid(row=10, column=1)
            self.label.destroy()
        else:  # if the position is valid update the pieces and set up the button that allows for a select move
            self.button.destroy()
            self.label.destroy()
            if x == None:
                isGameOver = self.check_win()  # check if the game is won
                if isGameOver == False:  # if it isn't make the next turn
                    self.make_next_turn()
                else:  # if the game is over dislay the end message
                    self.display_winner(isGameOver)
            else:
                self.button = tk.Button(self.buttonCanvas, text="Press to select new position",
                                        command=lambda: self.select_position_to_move_to(x,y,player,condition))
                self.button.grid(row=10, column=1)

    def select_position_to_move_to(self,x,y,player,condition):
        if player == 1:  # get the position that the player will move the selected piece to
            newCondition, takePiece= self.Player1.selecting_new_position(condition,self.Canvas,self.Circles,self.COLOUR2,self.buttonCanvas,x,y)
        elif player == 2:
            newCondition, takePiece = self.Player2.selecting_new_position(condition,self.Canvas,self.Circles,self.COLOUR2,self.buttonCanvas,x,y)
        if newCondition== "ERROR":  # if the selected position is invalid repeat and get a new move
            self.button.destroy()
            self.label.destroy()
            self.label = tk.Label(self.buttonCanvas, text="ERROR wrong position selected try again")
            self.label.grid(row=1, column=1)
            self.button = tk.Button(self.buttonCanvas, text="Press to select new position",
                                    command=lambda: self.select_position_to_move_to(x,y,player,condition))
            self.button.grid(row=10, column=1)
            self.label.destroy()
        else:  # if the position is valid the move is confirmed and saved then the next turn is set up
            self.button.destroy()
            self.label.destroy()
            self.Pieces=newCondition  # update the board
            if takePiece == True and player == 1:  # check if a piece has been taken and update piece totals
                self.player2Pieces-=1
            elif takePiece == True and player == 2:
                self.player1Pieces-=1

            isGameOver=self.check_win()  # check if the game is won
            if isGameOver == False:  # if it isn't make the next turn
                self.make_next_turn()
            elif isGameOver == 2 or isGameOver == 1:  # if the game is over dislay the end message
                self.display_winner(isGameOver)

    def check_win(self):
        if self.player1Pieces == 0:  # if there are no player 1 pieces return player 2 victory
            return 2
        elif self.player2Pieces == 0:  # if there are no player 2 pieces return player 1 victory
            return 1
        else:
            return False  # if there are pieces left for player 1 and 2 return false

    def display_winner(self,whoWon):
        self.label.destroy()
        self.button.destroy()
        if whoWon == 1:  # if player 1 wins display "player 1 wins" message
            self.label = tk.Label(self.buttonCanvas, text="Player 1 wins")
            self.label.grid(row=1, column=1)
        elif whoWon == 2:  # if player 2 wins display "player 2 wins" message
            self.label = tk.Label(self.buttonCanvas, text="Player 2 wins")
            self.label.grid(row=1, column=1)

class DetectMouseClick(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):  # uses a pymouse event to set up mouse click detection
        if button == 1:
            if press:
                if x not in range (0,410):
                    pass
                elif y not in range(20,430):
                    pass
                else:
                    global xcoor  # updates globals to the position of the mouse click
                    global ycoor
                    xcoor = x
                    ycoor = y
            self.stop()
        else:
            pass

class Piece:
    def __init__(self,Circles):
        self.PIECE_COLOUR1 = "darkgoldenrod1"
        self.PIECE_COLOUR2 = "grey45"
        self.HIGHLIGHT_COLOUR = "turquoise4"
        self.PIECE_SIZE = 50
        self.Circles=Circles

    def create_new_piece(self,row,col,x1,x2,y1,y2,Canvas,colour):  # creates a new piece
        self.Circles[row,col] =Canvas.create_oval(x1, y1, x2, y2, outline=colour, fill=colour)

    def change_piece_colour(self,Canvas,turn,Circles,row,col,Colour2): # changes the colour of a piece
        if turn == 1:
            colour = self.PIECE_COLOUR1
        else:
            colour = self.PIECE_COLOUR2
        Canvas.itemconfig(Circles[col,row],fill = colour)
        Canvas.itemconfig(Circles[col,row],outline = Colour2)

    def selected_highlight(self,Canvas,Circles,row,col):  # highlights a piece red when it has been selected to move
        Canvas.itemconfig(Circles[col, row], outline="red")

    def available_space_highlight(self, Canvas, Circles, row, col):  # highlights a possible position when it could be moved into
        Canvas.itemconfig(Circles[col, row], outline="blue")

    def remove_piece(self,Canvas,Circles,row,col,Colour2):  # removes a piece that exists in that position
        Canvas.itemconfig(Circles[col, row], fill=Colour2)
        Canvas.itemconfig(Circles[col, row], outline=Colour2)

    def remove_highlight(self,Canvas,Circles,row,col,Colour2):  # erases any highlights that a piece has
        Canvas.itemconfig(Circles[col, row], outline=Colour2)

class CrownedPiece(Piece):
    def __init__(self,Circles):
        self.PIECE_COLOUR1="darkorange3"
        self.PIECE_COLOUR2="purple2"
        self.Circles=Circles

    def create_crowned_piece(self,Canvas,turn,Circles,row,col,Colour2):  # creates a crowned piece
        if turn == 1:
            colour = self.PIECE_COLOUR1
        else:
            colour=self.PIECE_COLOUR2
        Canvas.itemconfig(Circles[col, row], fill=colour)
        Canvas.itemconfig(Circles[col,row],outline=Colour2)

class HumanPlayer():
    def __init__(self, turn):
        self.Turn = turn
        self.Pieces =None
        self.scoreCount=0
        self.blueCount = 0

    def make_move(self,Pieces,Canvas,Circles,Colour1,Colour2,buttonCanvas):
        self.blueCount =0
        self.Pieces=Pieces  # updates the players version of the board
        O = DetectMouseClick()  # uses the pymouse event to receive coordinates of the mouse click
        O.run()
        if xcoor == None or ycoor == None:  # if the coordinates are invalid (due to the event failing) return an error message
            return "ERROR", None, None
        else:
            newx= xcoor//50  # if the coordinates are successful correlate them to a position on the board
            newy=ycoor//50
            if newx not in range (0,8) or newy not in range (0,8):
                return "ERROR",None,None
            elif self.Pieces[newx,newy][1] == Colour1:
                # if the selected coordinates is a blank space return an error message
                return "ERROR", None,None
            elif self.Pieces[newx,newy][1] == str(self.Turn):
                 # if the selected position is one of the players pieces highlight it
                self.Pieces[newx, newy][0].selected_highlight(Canvas, Circles, newx, newy)
                self.Pieces[newx,newy][2] = "red"
                if self.Pieces[newx,newy][3] == True:  # if it is a crowned piece search above and below positions
                    self.searching_spaces_player1(newx,newy,True,Canvas,Circles,Colour2,buttonCanvas)
                    self.searching_spaces_player2(newx,newy,True,Canvas,Circles,Colour2,buttonCanvas)
                elif self.Turn ==1:  # if the piece is not crowned and a player 1 piece search below position
                    self.searching_spaces_player1(newx,newy,False,Canvas,Circles,Colour2,buttonCanvas)
                else:  # if the piece is not crowned and a player 2 piece search above position
                    self.searching_spaces_player2(newx,newy,False, Canvas, Circles, Colour2,buttonCanvas)
                if self.blueCount == 0:  # if there is no place to move to return an error message
                    self.removing_highlights(self.Pieces,Canvas,Circles,Colour2)
                    return "ERROR", None,None
                else:  # if there is spaces to move return the updated board veiw and the coordinates of the selected piece
                    return self.Pieces, newx,newy
            else:
                pass
                return "ERROR", None, None

    def searching_spaces_player1(self,row,col,turn,Canvas,Circles,Colour2,buttonCanvas):
        useTurn=None
        if turn==True:
            useTurn=str(self.Turn)
        else:
            useTurn="1"
        try:
             # if the square diagonally below the selected piece is blank highlight it
            if self.Pieces[row+1,col+1][1] == Colour2:
                self.Pieces[row+1,col+1][0].available_space_highlight(Canvas, Circles, row+1, col+1)
                self.Pieces[row+1,col+1][2]="blue"
                self.blueCount+=1
            elif self.Pieces[row+1,col+1][1] != useTurn:
                 # if the diagonal square contains a piece check if it is a take move
                self.search_diagonal_right_player1(row+1,col+1,Canvas,Circles,Colour2)
            else:
                pass
        except:
            pass

        try:  # repeat for the opposite diagonal
                if self.Pieces[row-1,col+1][1] == Colour2:
                    self.Pieces[row - 1, col + 1][0].available_space_highlight(Canvas, Circles, row - 1, col + 1)
                    self.Pieces[row - 1, col + 1][2] = "blue"
                    self.blueCount+=1

                elif self.Pieces[row-1,col+1][1]!= useTurn:
                    self.search_diagonal_left_player1(row-1,col+1,Canvas,Circles,Colour2)
                else:
                    pass
        except:
            pass

    def searching_spaces_player2(self,row,col,turn,Canvas,Circles,Colour2,buttonCanvas):
        useTurn=None
        if turn==True:
            useTurn=str(self.Turn)
        else:
            useTurn="2"
        try:  # if the square diagonally above the selected piece is blank highlight it
            if self.Pieces[row+1,col-1][1] == Colour2:
                self.Pieces[row+1,col-1][0].available_space_highlight(Canvas, Circles, row+1, col-1)
                self.Pieces[row+1,col-1][2] = "blue"
                self.blueCount+=1

            elif self.Pieces[row+1,col-1][1]!=useTurn:  # if the diagonal square contains a piece check if it is a take move
                self.search_diagonal_right_player2(row+1,col-1,Canvas,Circles,Colour2)

            else:
                pass
        except:
            pass

        try:  # repeat for the opposite diagonal
            if self.Pieces[row-1,col-1][1] == Colour2:
                self.Pieces[row-1,col-1][0].available_space_highlight(Canvas, Circles, row - 1, col-1)
                self.Pieces[row-1,col-1][2] = "blue"
                self.blueCount+=1

            elif self.Pieces[row-1,col-1][1]!=useTurn:
                self.search_diagonal_left_player2(row-1,col-1,Canvas,Circles,Colour2)

            else:
                pass
        except:
            pass

    def selecting_new_position(self,Pieces,Canvas,Circles,Colour2,buttonCanvas,row,col):
        O = DetectMouseClick()
        O.run()
        newx= xcoor//50  # get the coordinates of the mouse click
        newy=ycoor//50
        condition, takePiece = self.move_selected_piece(Canvas,Pieces,Circles,newx,newy,Colour2,row,col)  # check if the selected position is valid
        return condition, takePiece  # if the position is valid return the updated board

    def move_selected_piece(self,Canvas,Pieces,Circles,newx,newy,Colour2,row,col):
        takePiece = False
        if Pieces[newx, newy][2] == "blue":  # if the selected position is a highlighted and therefore available to move into
            if self.Turn==1 and newy == 7:  # if the piece is a crowned piece make sure the piece created in the new position is also crowned
                Pieces[newx,newy][0]=CrownedPiece(Circles)
                Pieces[newx,newy][0].create_crowned_piece(Canvas,self.Turn,Circles,newx,newy,Colour2)
                Pieces[newx,newy][1]= str(self.Turn)
                Pieces[newx,newy][3]=True
            elif self.Turn==2 and newy == 0:  # if the piece reaches the end of the board turn it into a crowned piece
                Pieces[newx,newy][0] = CrownedPiece(Circles)
                Pieces[newx,newy][0].create_crowned_piece(Canvas, self.Turn, Circles, newx, newy, Colour2)
                Pieces[newx,newy][3]= True
            else:
                if Pieces[row, col][3] == True:  # if the piece reaches the end of the board turn it into a crowned piece
                    Pieces[newx,newy][0] = CrownedPiece(Circles)
                    Pieces[newx,newy][0].create_crowned_piece(Canvas, self.Turn, Circles, newx, newy, Colour2)
                    Pieces[newx, newy][3] = True
                    Pieces[row,col][0] = Piece(Circles)
                else:
                    Pieces[newx, newy][0].change_piece_colour(Canvas, self.Turn, Circles, newx, newy, Colour2)
            # move the selected piece into the selected position
            Pieces[newx, newy][1] = str(self.Turn)
            Pieces[row,col][0].remove_piece(Canvas,Circles,row,col,Colour2)
            Pieces[row,col][1] =Colour2
            Pieces[row,col][2]=Colour2
            Pieces = self.removing_highlights(Pieces,Canvas,Circles,Colour2)
            return Pieces, takePiece  # return the updated board
        # if it is a take move that has been selected take the piece
        elif Pieces[newx, newy][2] == "blue take right 1" or Pieces[newx, newy][2] == "blue take left 1" \
                or Pieces[newx, newy][2] == "blue take right 2" or Pieces[newx, newy][2] == "blue take left 2":
            takePiece = True
            Pieces = self.take_piece(Canvas,Pieces,Circles,newx,newy,Colour2,row,col)
            return Pieces, takePiece

        else:  # if the position was not valid return an error message
            return "ERROR", "ERROR"

    def search_diagonal_right_player1(self,row,col,Canvas,Circles,Colour2):
        # if the following diagonal position is empty highlight and label with the correct move
        if self.Pieces[row+1,col+1][1] == Colour2:
            self.Pieces[row+1,col+1][0].available_space_highlight(Canvas, Circles, row+1, col+1)
            self.Pieces[row+1,col+1][2] = "blue take right 1"
            self.blueCount+=1
        else:
            pass

    def search_diagonal_left_player1(self,row,col,Canvas,Circles,Colour2):
        #  if the following diagonal position is empty highlight and label with the correct move
        if self.Pieces[row-1,col+1][1] == Colour2:
            self.Pieces[row-1,col+1][0].available_space_highlight(Canvas, Circles, row-1, col+1)
            self.Pieces[row-1,col+1][2] = "blue take left 1"
            self.blueCount+=1
        else:
            pass


    def search_diagonal_right_player2(self,row,col,Canvas,Circles,Colour2):
        #  if the following diagonal position is empty highlight and label with the correct move
        if self.Pieces[row+1,col-1][1] == Colour2:
            self.Pieces[row+1,col-1][0].available_space_highlight(Canvas, Circles, row+1, col-1)
            self.Pieces[row+1,col-1][2] = "blue take right 2"
            self.blueCount+=1
        else:
            pass

    def search_diagonal_left_player2(self,row,col,Canvas,Circles,Colour2):
        #  if the following diagonal position is empty highlight and label with the correct move
        if self.Pieces[row-1,col-1][1] == Colour2:
            self.Pieces[row-1,col-1][0].available_space_highlight(Canvas, Circles, row-1, col-1)
            self.Pieces[row-1,col-1][2] = "blue take left 2"
            self.blueCount+=1
        else:
            pass


    def take_piece(self,Canvas,Pieces,Circles,newx,newy,Colour2,row,col,):
        self.scoreCount+=1
        # use the label on the move to identify the type of move then remove the piece at the old position
        if Pieces[newx, newy][2]== "blue take right 1":
            Pieces[row+1,col+1][0].remove_piece(Canvas, Circles, row+1, col+1, Colour2)
            Pieces[row+1,col+1][1] = Colour2
            Pieces[row+1,col+1][2] = Colour2

        elif Pieces[newx, newy][2]== "blue take left 1":
            Pieces[row-1,col+1][0].remove_piece(Canvas, Circles, row-1, col+1, Colour2)
            Pieces[row-1,col+1][1] = Colour2
            Pieces[row-1,col+1][2] = Colour2

        elif Pieces[newx, newy][2] == "blue take right 2":
            Pieces[row+1,col-1][0].remove_piece(Canvas, Circles, row + 1, col - 1, Colour2)
            Pieces[row+1,col-1][1] = Colour2
            Pieces[row+1,col-1][2] = Colour2

        elif Pieces[newx, newy][2] == "blue take left 2":
            Pieces[row-1,col-1][0].remove_piece(Canvas, Circles, row - 1, col - 1, Colour2)
            Pieces[row-1,col-1][1] = Colour2
            Pieces[row-1,col-1][2] = Colour2
        else:
            pass

        if self.Turn==1 and newy == 7:  # if the piece reaches the end of the board turn it into a crowned piece
            Pieces[newx,newy][0]=CrownedPiece(Circles)
            Pieces[newx,newy][0].create_crowned_piece(Canvas,self.Turn,Circles,newx,newy,Colour2)
            Pieces[newx,newy][3]=True

        elif self.Turn==2 and newy == 0:  # if the piece reaches the end of the board turn it into a crowned piece
            Pieces[newx,newy][0]=CrownedPiece(Circles)
            Pieces[newx,newy][0].create_crowned_piece(Canvas,self.Turn,Circles,newx,newy,Colour2)
            Pieces[newx,newy][3]=True
        else:
            if Pieces[row,col][3]==True: # if the moved piece is a crowned piece make sure the new position piece is also crowned
                Pieces[newx, newy][0] = CrownedPiece(Circles)
                Pieces[newx, newy][0].create_crowned_piece(Canvas, self.Turn, Circles, newx, newy, Colour2)
                Pieces[newx,newy][3]=True
                Pieces[row,col][0]=Piece(Circles)
            else:
                Pieces[newx, newy][0].change_piece_colour(Canvas, self.Turn, Circles, newx, newy, Colour2)

        Pieces[newx, newy][1] = str(self.Turn)  # create the piece in the new position and destroy the taken piece and the old position piece
        Pieces[newx, newy][2] = Colour2
        Pieces[row, col][0].remove_piece(Canvas, Circles, row, col, Colour2)
        Pieces[row, col][1] = Colour2
        Pieces[row, col][2] = Colour2
        Pieces[row,col][3]=False
        Pieces = self.removing_highlights(Pieces, Canvas, Circles, Colour2)  # remlove highlights from the pieces
        return Pieces  # return the updated board


    def removing_highlights(self,Pieces,Canvas,Circles,Colour2):
        for i in range (0,8):  # search all positions and pieces and remove any highlighted ones
            for j in range(0,8):
                if Pieces[i,j][2]=="blue" or Pieces[i,j][2]=="blue take right 1" or Pieces[i,j][2]=="blue take left 1" \
                        or Pieces[i,j][2]=="blue take right 2" or Pieces[i,j][2]=="blue take left 2" or Pieces[i,j][2]=="red":
                    Pieces[i,j][0].remove_highlight(Canvas,Circles,i,j,Colour2)
                    Pieces[i,j][2] = Colour2

                if Pieces[i,j][1]== Colour2:
                    Pieces[i,j][3]=False
        return Pieces  # return the updated board

class ArtificailIntelligencePlayer(HumanPlayer):
    def __init__(self,turn,rows,columns):
        self.Turn = turn
        self.Pieces = {}
        self.ROWS  = rows
        self.COLUMNS = columns
        self.Moves={}
        self.scoreCount = 0

    def make_move(self, Pieces, Canvas, Circles, Colour1, Colour2, buttonCanvas):
        self.Pieces=Pieces  # update the players version of the board
        Graph =self.make_graph(Colour1, Colour2)  # create the graph of pieces
        i = 0
        start =list(Graph.keys())[i]  # get the start node of the graph
        while len(Graph[start])==0 and i<len(list(Graph.keys())):  # check if the start node is connected to any other nodes if it is not use the next node to start
            start=list(Graph.keys())[i]
            i+=1
        if len(Graph[start]) == 0:
            ownedPieces = self.search_for_pieces_without_traversal(Graph, Colour2) # if all the pieces are unconnected use a linear search each piece in turn
        else:
            ownedPieces = self.graph_traversal(start,Graph)  # otherwise get a list of owned pieces using the graph traversal
        for node in ownedPieces:
            values = []
            singleMoves = self.search_for_simple_moves(node,Colour2)  # get the list of single moves that can be made
            for i in singleMoves[0]:  # add each move to the moves list
                if self.Pieces[i][3] == False:
                    if self.Turn ==1 and i[1]== 7:
                         # if the move takes a piece to the vertical edge of the board increase the reward for the move
                        values.append((i,2))
                    elif self.Turn == 2 and i[1]==0:
                         #  if the move takes a piece to the vertical edge of the board increase the reward for the move
                        values.append((i,2))
                    elif i[0] == 0 or i[0] == 7 and self.Pieces[i][3]== False:
                         # if the move will result in the piece becoming crowned increase the reward
                        values.append((i, 2))
                    else:  # if the reward does not increase set it to 0
                        values.append((i,0))
                else:
                    values.append((i,0))
            try: # check if there the piece can make two moves and repeat the process
                if self.Pieces[i][3] == False:
                    for i in singleMoves[1]:
                        if self.Turn == 1 and i[1] == 7 and self.Pieces[i][3]==False:
                            values.append((i, 2))
                        elif self.Turn == 2 and i[1] == 0 and self.Pieces[i][3]==False:
                            values.append((i, 2))
                        elif i[0]==0 or i[0]==7:
                            values.append((i,2))
                        else:
                            values.append((i, 0))
                else:
                    values.append((i, 0))
            except:
                pass

            takeMoves = self.find_take_moves(node,Colour2)  # get the list of take moves
            for i in takeMoves[0]:
                if self.Pieces[i][3] == False:
                    #  if the take move creates a crowned piece or moves the piece to the vertical edge of the board increase the reward to 12
                    if self.Turn ==1 and i[1]== 7 and self.Pieces[i][3]==False or i[0]==0 or i[0]==7:
                        values.append((i,12))
                    elif self.Turn == 2 and i[1]==0 and self.Pieces[i][3]==False or i[0]==0 or i[0]==7:
                        values.append((i,12))
                    else:
                         # if not keep the reward as 10
                        values.append((i,10))
                else:
                    values.append((i, 10))

            try:  # repeat for second move if there is one
                if self.Pieces[i][3]==False:
                    for i in takeMoves[1]:
                        if self.Turn == 1 and i[1] == 7 and self.Pieces[i][3]==False or i[0]==0 or i[0]==7:
                            values.append((i, 12))
                        elif self.Turn == 2 and i[1] == 0 and self.Pieces[i][3]==False or i[0]==0 or i[0]==7:
                            values.append((i, 12))
                        else:
                            values.append((i, 10))
                else:
                    values.append((i, 10))
            except:
                pass

            # if there are moves that the piece can make add the piece coordinates, the move coordinates and the rewards to the moves dictionary
            if len(values)!=0:
                self.Moves[node]=values
        # choose the best move to make
        bestPieceToMove,bestMoveTo = self.choose_move_to_make()

        condition = self.validate_move_made(bestMoveTo,bestPieceToMove,Canvas,Pieces,Circles,Colour2)
        while condition == "ERROR":
            # if the validation on the move fails remove the move from the Move dictionary and get another move
            self.Moves[bestPieceToMove][self.Moves[bestPieceToMove].index(bestMoveTo)] = None
            bestPieceToMove, bestMoveTo = self.choose_move_to_make()
            condition = self.validate_move_made(bestMoveTo,bestPieceToMove,Canvas,Pieces,Circles,Colour2)

        self.removing_highlights(self.Pieces,Canvas,Circles,Colour2)
        self.Pieces = condition  # if the move is successful update the board and return it
        return self.Pieces, None, None

    def make_graph(self, Colour1, Colour2):
        Graph ={}
        identity= []
        for x in range (self.ROWS):
            for y in range (self.COLUMNS):
                 # for every square on the board if there is a piece in it turn the coordinates of the piece into a node
                if self.Pieces[x, y][1] == Colour1 or self.Pieces[x, y][1] == Colour2:
                    pass
                else:
                    for i in (-1, 1):
                        for j in (-1, 1):
                            if x+i<0 or y+j<0 or x+i>7 or y+j>7:
                                pass
                            else:
                                if self.Pieces[x+i,y+j][1] == Colour2 or self.Pieces[x, y][1] == Colour1:
                                    pass # add any connecting nodes the the identity list
                                else:
                                    identity.append((x+i,y+j))
                    Graph.update({(x,y):identity}) # update the graph with the new nodes and the list of connecting nodes
        return Graph  # return the graph

    def search_for_pieces_without_traversal(self,Graph, listToSearch):
        ownedPieces = []
        nodeList = list(Graph.keys())
        for i in nodeList:
            if self.Pieces[i][1]==str(self.Turn):
                ownedPieces.append(i)
        return ownedPieces

    def graph_traversal(self,start,Graph):
        ownPieces=[]
        keyList = list(Graph.keys())
        visited=[]
        queue =[(start)]  # queue up the starting vertex
        while len(queue)!=0:
            vertex = queue.pop()  # pop the first vertex in the queue
            if self.binary_search(visited,vertex) == False: # search the visited list for the vertex
                visited.append(vertex) # if the vertex has not been visited add it to the visited list
                try:
                    keyList.remove(vertex)
                except:
                    pass
                if self.Pieces[vertex][1]==str(self.Turn):  # if it is a piece that the player owns add it to the ownedPieces list
                    ownPieces.append(vertex)
            for adjacent in Graph[vertex]:  # if the adjacent verticies is not in the visited list add it to the list
                if self.binary_search(visited,adjacent)==False:
                    queue.append(adjacent)

        for node in keyList:  # to ensure any unconnected nodes are traversed
            if node not in visited:  # do a binary search for any unvisited nodes in the graph
                if self.Pieces[node][1] == str(self.Turn):
                    ownPieces.append(node)  # if the piece is the players piece add it to the ownPieces list
        return ownPieces

    def binary_search(self,searchList,item):
        for i in range(len(searchList) - 1):  # use a simple bubble sort on the searchList
            for j in range(i):
                if searchList[i] > searchList[i + 1]:
                    temp = searchList[i]
                    searchList[i] = searchList[i + 1]
                    searchList[i + 1] = temp

        if len(searchList) == 0:  # if the searchList is empty return false
            return False
        else:
            midpoint = len(searchList) // 2  # find the middle of the list
            if searchList[midpoint] == item:  # if the middle of the list is the item return true
                return True
            else:
                if item < searchList[midpoint]:  # if the middle of the list is larger than the item repeat with the lower half of the list
                    return self.binary_search(searchList[:midpoint], item)
                else: # if the middle of the list is smaller than the item repeat with the upper half of the list
                    return self.binary_search(searchList[midpoint + 1:], item)

    def search_for_simple_moves(self,node,Colour2):
        singleMoves = []
        if self.Pieces[node][3]==True:  # if the piece is a crowned piece search the positions above and below
            singleMoves.append(self.check_simple_move_available_player1(node[0],node[1],Colour2))
            singleMoves.append(self.check_simple_move_available_player2(node[0],node[1],Colour2))
        elif self.Turn == 1:  # if the player is player 1 search the positions below
            singleMoves.append(self.check_simple_move_available_player1(node[0],node[1], Colour2))
        elif self.Turn ==2:  # if the player is player 2 search the positions above
            singleMoves.append(self.check_simple_move_available_player2(node[0],node[1], Colour2))
        return singleMoves

    def check_simple_move_available_player1(self,x,y,Colour2):
        singleMoves=[]
        try:
            if self.Pieces[x+1,y+1][1]==Colour2:
                # if there is a space in the position diagonally below add it to the single moves list
                singleMoves.append((x+1,y+1))
        except:
            pass
        try:
            # repeat with the other diagonal
            if self.Pieces[x-1,y+1][1] == Colour2:
                singleMoves.append((x-1,y+1))
        except:
            pass
        return singleMoves

    def check_simple_move_available_player2(self,x,y,Colour2):
        singleMoves=[]
        try:
            if self.Pieces[x+1,y-1][1]==Colour2:
                # if there is a space in the position diagonally above add it to the single moves list
                singleMoves.append((x+1,y-1))
        except:
            pass
        try:
            if self.Pieces[x-1,y-1][1] == Colour2:
                # repeat with the other diagonal
                singleMoves.append((x-1,y-1))
        except:
            pass
        return singleMoves

    def find_take_moves(self,node, Colour2):
        takeMoves = []
        if self.Pieces[node][3]==True: # if the piece is a crowned piece search the positions above and below
            takeMoves.append(self.searching_take_moves_player1(node[0],node[1],Colour2))
            takeMoves.append(self.searching_take_moves_player2(node[0],node[1],Colour2))
        elif self.Turn == 1:  # if the player is player 1 search the positions below
            takeMoves.append(self.searching_take_moves_player1(node[0],node[1], Colour2))
        elif self.Turn ==2:  # if the player is player 2 search the positions above
            takeMoves.append(self.searching_take_moves_player2(node[0],node[1], Colour2))
        return takeMoves

    def searching_take_moves_player1(self,x,y,Colour2):
        takeMoves=[]
        try:
            if self.Pieces[x+1,y+1][1]==str(self.Turn):
                pass
            elif self.Pieces[x+1,y+1][1]!= Colour2:  # if there is an opposing piece in the below diagonal position
                if self.Pieces[x+2,y+2][1]==Colour2:
                    # if the following diagonal position is empty add it to the take moves list
                    takeMoves.append((x+2,y+2))
        except:
            pass
        try:  # repeat with the opposite diagonal
            if self.Pieces[x-1,y+1][1]==str(self.Turn):
                pass
            elif self.Pieces[x-1,y+1][1]!= Colour2:
                if self.Pieces[x-2,y+2][1]==Colour2:
                    takeMoves.append((x-2,y+2))
        except:
            pass
        return takeMoves

    def searching_take_moves_player2(self,x,y,Colour2):
        takeMoves=[]
        try:  # if there is an opposing piece in the above diagonal position
            if self.Pieces[x+1,y-1][1]==str(self.Turn):
                pass
            elif self.Pieces[x+1,y-1][1]!= Colour2:
                # if the following diagonal position is empty add it to the take moves list
                if self.Pieces[x+2,y-2][1]==Colour2:
                    takeMoves.append((x+2,y-2))
        except:
            pass
        try:  # repeat with opposite diagonal
            if self.Pieces[x-1,y-1][1] == str(self.Turn):
                pass
            elif self.Pieces[x-1,y-1][1]!= Colour2:
                if self.Pieces[x-2,y-2][1]==Colour2:
                    takeMoves.append((x-2,y-2))
        except:
            pass
        return takeMoves

    def choose_move_to_make(self):
        sortList = []
        for i in self.Moves:
            for j in (self.Moves[i]):
                try:
                    sortList.append((i,j[0],j[1]))  # set up the dictionary to a list to be used in the merge sort
                except:
                    pass

        sortList = self.merge_sort(sortList)  # merge sort the list
        if len(sortList)!=0:
            possibleMove = sortList.pop()  # take out the highest reward in the sorted list
            if possibleMove[2]==0:  # if the reward is 0 make a random move
                bestPieceToMove, bestMoveTo = self.choose_random_move()
            else:
                bestPieceToMove= possibleMove[0]  # assign the coordinates of the move to variables
                bestMoveTo = possibleMove[1],possibleMove[2]
        else:  # if there is an error with the move choose a random move
            bestPieceToMove,bestMoveTo = self.choose_random_move()
        return bestPieceToMove, bestMoveTo

    def merge_sort(self,sortList):
        if len(sortList)>1:
            mid = len(sortList)//2 # calculate the midpoint of the list
            leftHalf = sortList[:mid]  # seperate the list into two halves around the midpoint
            rightHalf = sortList[mid:]
            leftHalf = self.merge_sort(leftHalf)  # merge sort each of the half lists
            rightHalf = self.merge_sort(rightHalf)

            i,j,k = 0,0,0
            while i<len(leftHalf) and j<len(rightHalf):  # compare the start value of each half
                if leftHalf[i][2] < rightHalf[j][2]:  # add the lowest value to the sort list
                    sortList[k]=leftHalf[i]
                    i+=1
                else:
                    sortList[k]=rightHalf[j]
                    j+=1
                k+=1

            while i < len(leftHalf):  # move each item in the list along
                sortList[k]=leftHalf[i]
                i+=1
                k+=1

            while j < len(rightHalf):  # repeat for both lists
                sortList[k]=rightHalf[j]
                j+=1
                k+=1
        return sortList

    def choose_random_move(self):
        bestPieceToMove = random.choice(self.Moves.keys())  # select a random key a.k.a piece to move
        i = random.choice(self.Moves[bestPieceToMove])  # randomly select a value from the key a.k.a position to move to
        while i == None:  # if there is an error repeat the process
            bestPieceToMove = random.choice(self.Moves.keys())
            i = random.choice(self.Moves[bestPieceToMove])
        bestMoveTo = i  # assign the position coordinates to the variable
        return bestPieceToMove,bestMoveTo

    def validate_move_made(self,bestMoveTo,bestPieceToMove,Canvas, Pieces, Circles,Colour2):
        if self.Pieces[bestPieceToMove[0],bestPieceToMove[1]][1]!=str(self.Turn):
        # if the selected piece to move is not a valid piece return an error
            condition = "ERROR"
        elif self.Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][1]!=Colour2:
        # if the position being moved to is not valid return an error
            condition = "ERROR"
        elif bestMoveTo[1]==10 or bestMoveTo[1]==12:  # if the move will reult in a take piece set up a take move
            condition =self.change_take_piece(Canvas, Pieces, Circles, bestMoveTo,bestPieceToMove,Colour2)
        else:  # otherwise set up an ordinary simple move
            self.Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][2]="blue"
            condition = self.move_selected_piece(Canvas, Pieces, Circles, bestMoveTo[0][0], bestMoveTo[0][1], Colour2,
                                            bestPieceToMove[0], bestPieceToMove[1])
        return condition

    def change_take_piece(self,Canvas, Pieces, Circles, bestMoveTo,bestPieceToMove,Colour2):
        # calculate the difference in the coordinates of the moved piece and the position to calculate the piece that is taken
        diffx = (bestMoveTo[0][0] - bestPieceToMove[0])/2
        diffy = (bestMoveTo[0][1] - bestPieceToMove[1])/2

        if diffx == 0 or diffy ==0: # if there is no difference return an error as it is not a take move
            return "ERROR"
        else:
            if self.Turn == 1 and bestMoveTo[0][1] == 7:  # if the move results in a crowned piece set up a new crowned piece
                Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][0] = CrownedPiece(Circles)
                Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][0].create_crowned_piece(Canvas,self.Turn,Circles,bestMoveTo[0][0],bestMoveTo[0][1],Colour2)
                Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][1] = str(self.Turn)
                Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][3] = True
            elif self.Turn == 2 and bestMoveTo[0][1] == 0:
                Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][0] = CrownedPiece(Circles)
                Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][0].create_crowned_piece(Canvas,self.Turn,Circles,bestMoveTo[0][0],bestMoveTo[0][1],Colour2)
                Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][3]= True
            else:  # otherwise move the piece to the new position
                if Pieces[bestPieceToMove[0],bestPieceToMove[1]][3] == True:
                    Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][0]=CrownedPiece(Circles)
                    Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][0].create_crowned_piece(Canvas,self.Turn,Circles,bestMoveTo[0][0],bestMoveTo[0][1],Colour2)
                    Pieces[bestMoveTo[0][0], bestMoveTo[0][1]][3] = True
                    Pieces[bestPieceToMove[0],bestPieceToMove[1]][0] = Piece(Circles)
                else:
                    Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][0].change_piece_colour(Canvas,self.Turn,Circles,bestMoveTo[0][0],bestMoveTo[0][1],Colour2)

            # use the differences calculated to find the piece that is taken and remove it
            Pieces[bestMoveTo[0][0],bestMoveTo[0][1]][1] = str(self.Turn)
            Pieces[bestPieceToMove[0]+diffx,bestPieceToMove[1]+diffy][0].remove_piece(Canvas,Circles,bestPieceToMove[0]+diffx,bestPieceToMove[1]+diffy,Colour2)
            Pieces[bestPieceToMove[0]+diffx,bestPieceToMove[1]+diffy][1]=Colour2
            Pieces[bestPieceToMove[0]+diffx,bestPieceToMove[1]+diffy][2]=Colour2
            Pieces[bestPieceToMove[0],bestPieceToMove[1]][0].remove_piece(Canvas,Circles,bestPieceToMove[0],bestPieceToMove[1],Colour2)
            Pieces[bestPieceToMove[0],bestPieceToMove[1]][1]=Colour2
            Pieces[bestPieceToMove[0],bestPieceToMove[1]][2]=Colour2
            return Pieces

root = tk.Tk()
board = GameBoard(root)
board.pack(side="top", fill="both", expand="true")

board.new_board()
board.set_initial_pieces()
root.mainloop()