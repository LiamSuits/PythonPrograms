# Poke The Dots Version 1
# In this game the user tries to prevent two moving
# dots from colliding by pressing and releasing the mouse
# button to teleport the dots to a random location.
# The score is the number of seconds from the start of the
# game until the dots collide.
#
# V1 uses "Template - Events Algorithm" and implements 
# moving dots that start at fixed locations (instead of 
# random) and "wrap around" the edges (instead of bouncing)
# - no scoreboard, 
# - no dot collisions
# - no handling of player actions
# - game runs until player closes window (part of the template)
import pygame,time,math,random
from uagame import Window
from pygame.locals import *

# Main Algorithm
def main():
    # create the window
    title = 'Poke THe Dots'
    width = 500
    height = 400
    window = Window(title,width,height)
    window.set_auto_update(False)
    # create the Game object
    game = Game(window)
    # play the game
    game.play()
    # close the window
    window.close()
# USER DEFINED CLASS
class Game:
    # An object in this class represents a complete game.

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        
        self.window = window
        self.close_clicked = False
        self.continue_game = True
        self.pause_time = 0.01 # smaller is faster game
        # Create red dot
        color1 = pygame.Color('red')
        center1 = [50,75]
        radius1 = 30
        velocity1 = [1,2]
        surface = window.get_surface()
        self.small_dot=Dot(surface,color1,center1,radius1,velocity1)
        # Create blue Dot
        color2 = pygame.Color('blue')
        center2 = [250,200]
        radius2 = 40
        velocity2 = [2,1]
        self.big_dot = Dot(surface,color2,center2,radius2,velocity2)
        self.small_dot.randomize()
        self.big_dot.randomize()        
        self.score = 0
        
    
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:
            # play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue() # should game continue?
            time.sleep(self.pause_time) # set game velocity by pausing
            
    def handle_event(self):
        # Handle one user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled.

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up()
    def handle_mouse_up(self):
        self.small_dot.randomize()
        self.big_dot.randomize()
                        
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self.window.clear()
        self.small_dot.draw()
        self.big_dot.draw()
        self.draw_score()
        if  not self.continue_game:
            self.draw_game_over()
        self.window.update()        
    def draw_score(self):
        score_string = 'Score' + str(self.score)
        fg_color = 'white'
        font_size = 70
        self.window.set_font_size(font_size)
        self.window.set_font_color(fg_color)
        x = 0
        y = 0
        self.window.draw_string(score_string,x,y)
    def draw_game_over(self):
        font_size = 100
        fg_color = 'red'
        bg_color = 'blue'
        game_over_str = 'Game Over'
        self.window.set_font_size(font_size)
        self.window.set_font_color(fg_color)
        self.window.set_bg_color(bg_color)
        x = 0
        y = self.window.get_height() - self.window.get_font_height()
        self.window.draw_string(game_over_str,x,y)
        default_bg_color = 'black'        
        self.window.set_bg_color(default_bg_color)
    def update(self):
        # Update all game objects with state changes
        # that are not due to user events
        # - self is the Game to update
        self.small_dot.move()
        self.big_dot.move()
        self.score = pygame.time.get_ticks()//1000

    def decide_continue(self):
        # Determine if the game should continue
        # - self is the Game to update
        if self.small_dot.crash(self.big_dot):
            self.continue_game = False
class Dot:
    def __init__(self,surface,color,center,radius,velocity):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object        
        self.surface = surface
        self.color = color
        self.center = center
        self.radius = radius
        self.velocity = velocity
    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot
        
        pygame.draw.circle(self.surface,self.color,self.center,self.radius)
    def move(self):
        # Change the location and the velocity of the Dot so it
        # remains on the surface by bouncing from its edges.
        # - self is the Dot
        
        #self.center[0] = (self.center[0] + self.velocity[0])%500
        #self.center[1] = (self.center[1] + self.velocity[1]) % 400
        size = self.surface.get_size()
        # size is a tuple holding (width, height)
        for coord in range(len(size)):
            self.center[coord] = (self.center[coord]+self.velocity[coord])%size[coord]
            if self.center[coord] < self.radius:
                self.velocity[coord] = -self.velocity[coord]
            if self.center[coord] + self.radius > size[coord]:
                self.velocity[coord] = -self.velocity[coord]
                
    def crash(self,other_dot):
        distance_x = self.center[0] - other_dot.center[0]
        distance_y = self.center[1] - other_dot.center[1]
        distance = math.sqrt(distance_x**2 + distance_y**2)
        return distance < self.radius + other_dot.radius
    
    def randomize(self):
        atuple = self.surface.get_size()
        for index in range(0,2):
            self.center[index] = random.randint(self.radius,atuple[index] - self.radius)
            
                
main()


