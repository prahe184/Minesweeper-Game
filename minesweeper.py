import random
import re

class Board: 
     def __init__(self, dim_size, num_bombs):
          self.dim_size = dim_size
          self.num_bombs = num_bombs
          #Let's create a board
          #helper_function!
          self.board = self.make_new_board() #plant the bombs
          self.assign_values_to_board()

          #Let's keep track of which locations we've uncovered through initialising a set
          #we save in a row,col tuples into this set
          self.dug = set() #if we dig at 0,0, then self.dug={(0,0)}
     def make_new_board(self):
          #construct a new board based on the dim_size and num_bombs
          #we should consider a list of lists here(or whatever representation you prefer)
          #but since we have a 2D board, list of lists is natural

          #generates a new board
          board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
          #this creates an array like this:
          #[[None, None,..., None],
          #[None, None,..., None],
          #[None, None,..., None]]
          #we can see how this represents a board!
          #plant the bombs
          bombs_planted  = 0
          bomb_locations = {set}
          while bombs_planted < self.num_bombs:
               loc = random.randint(0, self.dim_size**2-1) #return a random integer N such that a <= N <= b
               row = loc // self.dim_size #we want the number of times dim_size goes into loc to tell us
               col = loc % self.dim_size #we want the remainder to tell us what index in that row to loc
               
               if (row, col) in bomb_locations:
                     continue  # Bomb already here, retry

               bomb_locations.add((row, col))  # Store bomb location
               board[row][col] = '*'  # Plant the bomb
               bombs_planted += 1

          return board
               
     def assign_values_to_board(self):
          #now that we have bombs planted, let's assign a number 0-8 for all empty spaces,which
          #represemts how many neighbouring bombs there are. We can precompute these and it'll save us some 
          #effort checking what's around the board later on:
          for r in range(self.dim_size):
                for c in range(self.dim_size):
                    if self.board[r][c] == '*':
                         #if its already a bomb, we don't want to calculate anything
                          continue
                    self.board[r][c] = self.get_num_neighbouring_bombs(r,c)
     def get_num_neighbouring_bombs(self, row, col):
          #Let's iterate through each of the neighbouring positions and sum number of bombs
          #top left: (row-1, col-1)
          # top middle: (row-1, col)
          # top right: (row-1, col+1)
          #left : (row, col-1)
          #right: (row, col+1)
          #bottom left: (row+1, col-1)
          #bottom middle: (row+1, col)
          #bottom right: (row+1, col+1)
          num_neighbouring_bombs = 0
          for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
               for c in range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                    if r == row and c == col:
                         #our original location, don't check
                          continue
                    if self.board[r][c] == '*':
                          num_neighbouring_bombs +=1
          return num_neighbouring_bombs 
     def dig(self, row, col):
           #dig at that location
           #return true if successful dig, Flase if bomb dug

           #a few scenarios:
           #hit a bomb -> game over
           #dig at location with neighbouring bombs -> finish dig
           #dig at location with no neighbouring bombs -> recursively dig neighbours!
           if(row,col) in self.dug:
                 return True
           self.dug.add((row,col)) #keep track that we dug here
           if self.board[row][col] == '*':
                return False
           elif self.board[row][col]>0:
                return True
           
           #self.baord[row][col] 
           for r in range(max(0,row-1),min(self.dim_size-1, row+2)):
                for c in range(max(0,col-1),min(self.dim_size-1, col+2)):
                    if (r,c) in self.dug:
                         continue #don't dig where you alraedy dug
                    self.dig(r,c)
           return True

     def __str__(self):
          #this is a magic function where if you print on this object,
          #it'll print out wheat this function returns
          #return a string that shows a board to the player

          #first let's create a new array that represents what the user would see
          visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
          for row in range(self.dim_size):
               for col in range(self.dim_size):
                    if (row,col) in self.dug:
                          visible_board[row][col] = str(self.board[row][col])
                    else:
                          visible_board[row][col] = ' '
          # Build a string representation of the visible board.
          string_rep = "   " + "  ".join(str(i) for i in range(self.dim_size)) + "\n"  # Column headers
          string_rep += "   " + "---" * self.dim_size + "\n"  # Separator line

          for i in range(len(visible_board)):
                row = visible_board[i]
                string_rep += f"{i} | " + " | ".join(row) + " |\n"  # Format rows neatly

          return string_rep

#play the game
def play(dim_size=10, num_bombs=10):
     #1: Create the board and plant the bombs
     game_board = Board(dim_size, num_bombs)


     #2: Show the board to the user and ask for where they want to dig?
     #3a:If the location is a bomb then show game over message
     #3b:If the location is not a bomb, dig recursively until each square is atleast next to a bomb
     #4:repeat steps2 and 3ab until there are no more places to dig-->Victory!

     safe = True
     while len(game_board.dug)<game_board.dim_size ** 2-num_bombs:
          
          user_input = re.split(',(\\s)*',input("Where would you like to dig? Input as row, col: "))
          try:
               row, col = int(user_input[0]), int (user_input[-1])
          except:
            print("Invalid input. Try again.")
            continue

          if row<0 or row>=game_board.dim_size or col<0 or col>=game_board.dim_size:
                print("Invalid loaction.Try again.")
                continue
          safe = game_board.dig(row,col)
          print(game_board)

          if not safe:
                break

     if safe:
           print("Congratulations, You're victorious!")
     else:
           print("Sorry, Game Over")
           game_board.dug = {(r,c) for r in range(game_board.dim_size) for c in range(game_board.dim_size)}
           print(game_board)

     
if __name__ == "__main__":
       play()