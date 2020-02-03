# Pong V3
# This game shows a ball going across the screen.
# There are 2 paddles that have frontal collision.
# The left paddle moves up and down when 'q' and 'a' are pressed.
# The right paddle moves up and down when 'p' and 'l' are pressed.
# The game closes when the 'x' is clicked.
# When the ball hits the left and right most "walls" a point will be scored.
# The game ends when either score reaches 11.

from uagame import Window
import pygame, time
from pygame.locals import *

def main():
   # create window
   window = Window('Pong V3', 500, 400)
   
   # play game
   window.set_auto_update(False)
   game = Game(window)
   game.play()
   window.close()

# User-defined classes

class Ball:
   # An object in this class represents a white ball.

   def __init__(self, center, radius, color, surface, velocity):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - center is a list containing the x and y int
      # coords of the center of the Circle
      # - radius is the int pixel radius of the Circle
      # - color is the pygame.Color of the Circle
      # - surface is the uagame window object
      # - velocity is the speed of the Ball in the x/y plane

      self.center = center
      self.radius = radius
      self.color = color
      self.surface = surface
      self.velocity = velocity
   
   def draw(self):
      # Draw the Ball.
      # - self is the Ball to draw
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   
   def move(self,right_paddle,left_paddle):
      # Move the Ball.
      # self is the Ball to move
      # import the parameters of the paddles
      get_right_rect = right_paddle.rect
      get_left_rect = left_paddle.rect
      
      # make sure the ball bounces off the bounds of the screen
      window_size = (self.surface.get_width(), self.surface.get_height())
      for index in range(len(window_size)):
         self.center[index] = self.center[index] + self.velocity[index]         
         if self.center[index] - self.radius < 0 or self.center[index] + self.radius > window_size[index]:
            # bounce the ball
            self.velocity[index] = -1* self.velocity[index] 
            # change direction
         elif self.velocity[0] > 0 and get_right_rect.collidepoint(self.center):
            # bounce off the right paddle from the front
            self.velocity[0] = -1* self.velocity[index]
         elif self.velocity[0] < 0 and get_left_rect.collidepoint(self.center):
            # bounce off the left paddle from the front
            self.velocity[0] = -1* self.velocity[index]   

            
      
   
class Paddle:
   # An object in this class represents a white paddle.

   def __init__(self, surface, color, rect, width, velocity):
      # - self is the Paddle to initialize
            # - surface is the uagame window object  
            # - color is the pygame.Color of the Paddle
            # - rect is the coords and size of the Paddle
            # - width is the thickness of the Paddle
                
      self.surface = surface
      self.color = color
      self.rect = rect
      self.width = width
      self.velocity = velocity
      
   def draw(self):
      # draw the paddle
      pygame.draw.rect(self.surface, self.color, self.rect, self.width)
      
   def move_up(self):
      # handle 'q' and 'p' inputs
      if self.rect.top > 0:
         self.rect.top = self.rect.top - self.velocity
   
   def move_down(self):
      # handle 'a' and 'l' inputs
      if self.rect.top < self.surface.get_height() - self.rect.height:
         self.rect.top = self.rect.top + self.velocity

class Game:
   # An object in this class represents a complete game.

   def __init__(self, window):
      # Initialize a Game.
      # - self is the Game to initialize
      # - window is the uagame window object
      self.window = window
      surface = window.get_surface()
      self.surface = surface
      color = pygame.Color('white')
      self.pause_time = 0.01
      self.close_clicked = False
      self.continue_game = True
      # pygame.key.set_repeat(20, 20)
      # parameters for the ball
      center = [250,200]
      radius = 5
      velocity = [6,2]
      self.ball = Ball(center, radius, color, surface, velocity)
      # parameters for the first paddle
      rect1 = Rect(75, 175, 10, 50)
      width = 0
      paddle_velocity = 4
      self.left_paddle = Paddle(surface, color, rect1, width, paddle_velocity)
      # parameters for the second paddle
      rect2 = Rect(425, 175, 10, 50)
      self.right_paddle = Paddle(surface, color, rect2, width, paddle_velocity)
      # parameters for the scoreboard
      self.left_score = 0
      self.right_score = 0
      self.score_size = 72
      
      
      
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

   def handle_keys(self):
      # determine which keys are being pressed
      keys_pressed = pygame.key.get_pressed()
      if keys_pressed[K_q]:
         self.left_paddle.move_up()
      if keys_pressed[K_a]:
         self.left_paddle.move_down()
      if keys_pressed[K_p]:
         self.right_paddle.move_up()
      if keys_pressed[K_l]:
         self.right_paddle.move_down()      
   def handle_event(self):
      # Handle each user event by changing the game state
      # appropriately.
      # - self is the Game whose events will be handled

      event = pygame.event.poll()
      if event.type == QUIT:
         self.close_clicked = True
      # if event.type == KEYDOWN:
      if self.continue_game:
         #allow no inputs when the game is over
         self.handle_keys()
         
   def draw_score(self):
      # set font size for the scoreboard and 
      # display the score
      right_score_x = 500 - self.window.get_string_width(str(self.right_score))
      left_score_x = 0
      score_y = 0
      self.window.set_font_size(self.score_size)
      # draw each score
      self.window.draw_string(str(self.left_score), left_score_x,score_y)
      self.window.draw_string(str(self.right_score), right_score_x,score_y)
   
   def update_score(self):
      # decide if a point is scored for the left or right side
      window_size = (self.surface.get_width(), self.surface.get_height())
      left_bound = 0
      right_bound = 500
      # when ball hits the left side
      if self.ball.center[0] - self.ball.radius < left_bound:
         self.right_score = self.right_score + 1
      # when ball hits the right side
      elif self.ball.center[0] + self.ball.radius > right_bound:
         self.left_score = self.left_score + 1
      
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.window.clear()
      self.ball.draw()
      self.left_paddle.draw()
      self.right_paddle.draw()
      self.draw_score()
      if not self.continue_game:
         # Perform appropriate game over actions
         # there are no game over actions
         pass
      self.window.update()

   def update(self):
      # Update the game objects.
      # - self is the Game to update
      self.update_score()
      self.ball.move(self.right_paddle, self.left_paddle)
      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      max_score = 11
      # if either score reaches 11 stop the game immediately
      if self.left_score == max_score or self.right_score == max_score:
         self.continue_game = False


main()












