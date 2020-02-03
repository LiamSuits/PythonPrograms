# Memory V3
# In this game the player tries
# to solve a memory puzzle as fast as possible.
# There is 4x4 grid of tiles and 2 of each image.
# The timer stops when all tiles are flipped

from uagame import Window
from random import shuffle
import pygame, time
from pygame.locals import *

# User-defined functions
def main():
   window = Window('Memory', 500, 400)
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
      self.pause_time = 0.001 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      Tile.set_window(window)
      self.image_list = []
      self.index = 0
      self.can_click = True
      self.last_time = 0
      self.board_size = 4
      self.selected = []
      self.create_images()
      self.board = []
      self.create_board()
      self.timer = 0
      self.timer_size = 100
      self.matches = 0
      self.start_time = pygame.time.get_ticks()

   def create_images(self):
      # loads images from a folder into a list
      for num in range(1,9):
         image_file = 'image' + str(num) + '.bmp'
         picture = pygame.image.load(image_file)
         self.image_list.append(picture)
      self.image_list = self.image_list + self.image_list
      shuffle(self.image_list)  
      
   def create_board(self):
      # create the 4x4 game board
      # -self is the Game object
      for row_index in range(0,self.board_size):
         # create row
         row = self.create_row(row_index)
         # Add row to board
         self.board.append(row)
         
   def create_row(self,row_index):
      # creates one row of 4 row objects and returns it
      # -self is the Game object
      # -row_index is the row number to be created
      row = []
      black_space = self.window.get_width()//5
      width = (self.window.get_width() - black_space)//self.board_size
      height = self.window.get_height()//self.board_size
      Tile.set_dimensions(width,height)
      for col_index in range(0,self.board_size):
         x = width * col_index
         y = height * row_index
         # Create Tile object
         tile = Tile(x,y,self.image_list[self.index])
         self.index = self.index + 1
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
      if event.type == MOUSEBUTTONUP and self.continue_game and self.can_click:
         self.handle_mouse_up(event)
   
   def handle_mouse_up(self,event):
      # handles mouse up event
      # - event is pygame.event.Event object
      for row in self.board:
         for tile in row:
            if tile.select(event.pos):
               tile.flip_tile()
               self.selected.append(tile)
   
   def check_tiles(self):
      # check if the 2 clicked tiles match 
      self.can_click = False
      if self.last_time == 0:
         self.last_time = pygame.time.get_ticks()
      time_elapsed = (pygame.time.get_ticks()) - self.last_time
      
      if self.selected[0] == self.selected[1]:
         self.matches = self.matches + 1
         self.selected = []
         self.last_time = 0
         self.can_click = True         
      elif  time_elapsed > 1000:
         self.selected[0].flip_back()
         self.selected[1].flip_back()
         self.selected = []
         self.last_time = 0
         self.can_click = True
      
   def draw(self):
      # Draw all game objects.
      # Check if all tiles are clicked
      self.window.clear()
      surface = self.window.get_surface()
      for row in self.board:
         for tile in row:
            tile.draw()
      self.draw_timer()
      self.window.update()
      
   def draw_timer(self):
      # draw the timer
      self.window.set_font_size(self.timer_size)
      timer_x = self.window.get_width() - self.window.get_string_width(str(self.timer))
      timer_y = 0
      self.window.draw_string(str(self.timer), timer_x,timer_y)
      
   def update(self):
      # update the timer when the game isn't won
      if self.continue_game:
         self.update_timer()
         if len(self.selected) > 1:
            self.check_tiles()
 
   def update_timer(self):
      # update the timer according to time spent in game
      self.timer = int(((pygame.time.get_ticks() - self.start_time)//1000))
      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.matches >= 8:
         self.continue_game = False
class Tile:
   # An object of this class represents a Tile
   # Class Attributes
   window = None
   border_size = 3
   border_color = pygame.Color('black')
   hidden_image = pygame.image.load('image0.bmp')
   # Class Method
   @classmethod
   def set_window(cls,window):
      cls.window = window
   @classmethod
   def set_dimensions(cls,width,height):
      cls.width = width
      cls.height = height
   #Instance Methods
   def __init__(self,x,y,image):
      # initializes the Tile object
      # - self is the Tile
      self.rect = pygame.Rect(x,y,Tile.width,Tile.height)
      self.image = image
      self.clicked = False
      self.flipped = False
   def draw(self):
      # draws the Tile
      # - self is the Tile object to draw
      surface = Tile.window.get_surface()
      if self.flipped:
         surface.blit(self.image,self.rect)
      else:
         surface.blit(Tile.hidden_image,self.rect)
      pygame.draw.rect(surface,Tile.border_color,self.rect,Tile.border_size)
   
   def select(self,position):
      # detects mouse click inside Tile 
      # - self is the Tile object
      # - position is the (x,y) location of the mouse click
      return self.rect.collidepoint(position) and not self.flipped
   
   def flip_tile(self):
      # called when a tile is clicked
      self.flipped = True
   
   def flip_back(self):
      # called when the two flipped tiles do not match
      self.flipped = False   
   
   def __eq__(self,other_tile):
      if self.image == other_tile.image:
         return True
      else:
         return False
   

main()






