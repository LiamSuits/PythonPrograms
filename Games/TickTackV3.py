# Tic Tac Toe Version 3 - custom cursors
# This program allows two players to play Tic Tac Toe.
# The X and Y player's take turns selecting empty tiles
# to fill on a 3x3 board. If a player selects three tiles
# in a row, a column or a diagonal, that player wins.
# If all the tiles are filled without a win, the game is
# a draw.


from uagame import Window
import pygame, time,random
from pygame.locals import *

# User-defined functions

def main():

   window = Window('Tic Tac Toe', 500, 400)
   window.set_auto_update(False)
   game = Game(window)
   game.play()
   window.close()

# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, window):
      # Initialize a Game.
      # - self is the Game to initialize
      # - window is the uagame window object
      
      self.window = window
      self.pause_time = 0.00001 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      # This is how we call a class method
      Tile.set_window(window)
      self.board = []
      self.player_x = 'X'
      self.player_o = 'O'
      self.cursor_x = Cursor('cursorx.txt')
      self.cursor_o = Cursor('cursoro.txt')
      self.cursor_x.activate()
      self.turn = self.player_x
      self.filled = []
      self.flashers = []
      self.create_board()
   def create_board(self):
      # create a TTT board by creating and adding one row at a time
      # -self is the Game object
      for row_index in range(0,3):
         # create row
         row = self.create_row(row_index)
         # Add row to board
         self.board.append(row)
   def create_row(self,row_index):
      # creates one row of 3 Tile objects and returns it
      # -self is the Game object
      # -row_index is the row number to be created
      row = []
      width = self.window.get_width()//3
      height = self.window.get_height()//3
      for col_index in range(0,3):
         x = width * col_index
         y = height * row_index
         # Create Tile object
         tile = Tile(x,y,width,height)
         # Add tile to row
         row.append(tile)
      return row

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
          # play frame
         self.handle_event()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         time.sleep(self.pause_time) # set game velocity by pausing

   def handle_event(self):
      # Handle each user event by changing the game state
      # appropriately.
      # - self is the Game whose events will be handled

      event = pygame.event.poll()
      if event.type == QUIT:
         self.close_clicked = True
      if event.type == MOUSEBUTTONUP and self.continue_game:
         self.handle_mouse_up(event)
   def handle_mouse_up(self,event):
      # handles mouse up event
      # - event is pygame.event.Event object
      for row in self.board:
         for tile in row:
            if tile.select(event.pos,self.turn) == True:
               self.filled.append(tile)
               self.change_turn()
   def change_turn(self):
      if self.turn == self.player_x:
         self.turn = self.player_o
         self.cursor_o.activate()
      else:
         self.turn = self.player_x
         self.cursor_x.activate()
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.window.clear()
      self.choose_flashing_tile()
      for row in self.board:
         for tile in row:
            tile.draw()
      self.window.update()
   def choose_flashing_tile(self):
      if len(self.flashers) != 0:
         tile = random.choice(self.flashers)
         # I am calling the flash method in the Tile class to set the flashing attributes
         # Writing tile.flash is NOT right
         tile.flash()
         
      
      
   def update(self):
      # Update the game objects.
      # - self is the Game to update
      pass
   def is_list_win(self,alist):
      # - alist is a list of 3 Tile objects
      list_win = False
      if alist[0] == alist[1] == alist[2]:
         # == operator is calling the __eq__ method inside the Tile class
         self.flashers = alist
         list_win = True
      return list_win
   def is_row_win(self):
      row_win = False
      for row in self.board:
         # What is a row
         # A row is a list of 3 Tile objects
         if self.is_list_win(row) == True:
            row_win = True
         # return row_win this will be a PROBLEM
      return row_win
   def is_diagonal_win(self):
      diagonal_win = False
      diagonal1 = [self.board[0][0],self.board[1][1],self.board[2][2]]
      diagonal2 = [self.board[2][0],self.board[1][1],self.board[0][2]]
      if self.is_list_win(diagonal1) or self.is_list_win(diagonal2):
         diagonal_win = True
      return diagonal_win
   def is_column_win(self):
      column_win = False
      for col_index in range(0,3):
         column = []
         for row_index in range(0,3):
            tile = self.board[row_index][col_index]
            column.append(tile)
         # column is a list of 3 Tile objects
         if self.is_list_win(column):
            column_win = True
         # return column_win PROBLEM
      return column_win
   def is_tie(self):
      tie = False
      if len(self.filled) == 9:
         self.flashers = self.filled
         tie = True
      return tie
   def is_win(self):
      win= False
      if self.is_row_win() or self.is_column_win() or self.is_diagonal_win():
         win = True
      return win
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.is_win() or self.is_tie():
         self.continue_game = False
class Tile:
   # An object of this class represents a Tile
   # Class Attributes
   window = None
   font_size = 133
   border_size = 3
   border_color = 'white'
   # Class Method
   @classmethod
   def set_window(cls,window):
      cls.window = window
   #Instance Methods
   def __init__(self,x,y,width,height):
      # initializes the Tile object
      # - self is the Tile
      # - x,y are top left corner int coordinates of Tile object
      # - width, height are int dimensions of Tile object
      self.flashing = False
      self.content = ''
      self.rect = pygame.Rect(x,y,width,height)
   def draw(self):
      # draws the Tile based on its flashing attributes
      # - self is the Tile object to draw
      surface=Tile.window.get_surface()
      if self.flashing:
         # draw a white rectangle
         pygame.draw.rect(surface,pygame.Color(Tile.border_color),self.rect,0)
         self.flashing = False
      else:
         # draw a black rectangle with white border
         self.draw_content()
         pygame.draw.rect(surface,pygame.Color(Tile.border_color),self.rect,Tile.border_size)
   def draw_content(self):
      # draws the content of the Tile object
      # - self is the Tile object
      # set the Size and color
      Tile.window.set_font_size(Tile.font_size)
      Tile.window.set_font_color(Tile.border_color)
      # find the location 
      string_width = Tile.window.get_string_width(self.content)
      left_over_x = self.rect.width - string_width
      x = self.rect.x + left_over_x//2
      string_height = Tile.window.get_font_height()
      left_over_y = self.rect.height - string_height
      y = self.rect.y + left_over_y//2
      Tile.window.draw_string(self.content,x,y)
   def select(self,position,player):
      # detects mouse click inside Tile 
      # changes content if content is blank
      # else sets flashing attribute to True 
      # - self is the Tile object
      # - position is the (x,y) location of the mouse click
      # - player is either 'X' or 'O'
      valid_click = False
      if self.rect.collidepoint(position):
         if self.content == '':
            self.content = player
            valid_click = True
         else:
            self.flashing = True
      return valid_click
   def flash(self):
      self.flashing = True
   def __eq__(self,other_tile):
      if self.content != '' and self.content == other_tile.content:
         return True
      else:
         return False
class Cursor:
   def __init__(self,filename):
      # step 1 - OPEN a file in read mode
      # returns an object of type TextIOWrapper
      infile = open(filename,'r')
      # step 2 - read the file using the read method in TextIOWrapper class
      # returns the entire file as a string
      content = infile.read()
      # step 3 - split lines into a list
      list_of_strings = content.splitlines()
      # step 4 - use pygame function to generate the data and the mask
      compiled = pygame.cursors.compile(list_of_strings,black = '#', white='*')
      self.data = compiled[0]
      self.mask =compiled[1]
      width = len(list_of_strings[0])
      height = len(list_of_strings)
      self.size = (width,height)
      self.hotspot = (width//2,height//2)
   def activate(self):
      pygame.mouse.set_cursor(self.size,self.hotspot,self.data,self.mask)
main()




