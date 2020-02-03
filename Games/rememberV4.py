# Remember The Word Version 4
# This program does the following:
# creates a window
# displays icon
# display instructions
# prompts player to press enter
# displays words
# gets guess
# displays results - outputs congrats or condolences
# end game
# replace duplicate line groups with repititon control structure
# limit the occurrence of literals

# Main Algorithm
import time
from uagame import Window

def main():
    
    # create window
    title = 'Remember the Word'
    width = 500
    height = 400
    window = Window(title,width,height)
    
    # display icon
    display_icon(window)
    
    # display instructions
    text_size = 24
    text_color = 'white'    
    window.set_font_size(text_size)    
    font_height = window.get_font_height()
    display_instrcutions(window,text_size,text_color,font_height)
    
    # clear window
    window.clear()
    # display the icon
    display_icon(window)   
    
    # display words   
    word_list = ['orange','chair','mouse','sandwich']
    correct_answer = word_list[3]
    start_letter = correct_answer[0]
    # FUNCTION CALL TO DISPLAY WORDS
    display_words(window,text_size,text_color,word_list)
 
    # get guess -  FUNCTION CALL
    guess = get_guess(window,text_size,text_color,start_letter)
    # clear window
    window.clear()
    # display the icon
    display_icon(window)    
    # display results
    display_results(window,text_size,text_color,guess,correct_answer)
    # end game
    end_game(window)
    
#USER DEFIND FUNCTIONS
def end_game(window):
    font_height = window.get_font_height
    x = 0
    y = window.get_height() - window.get_font_height() 
    prompt2 = 'Press enter to end the game.'
    window.input_string(prompt2,x,y)
    window.close()    
    
def display_results(window,text_size,text_color,guess,correct_answer):
    x = 0
    y = 0
    window.set_font_size(text_size)
    window.set_font_color(text_color)    
    font_height = window.get_font_height()
    win_message = 'Congratulations, you are correct.'
    lose_message = 'Sorry you entered ' + guess
    if guess == correct_answer:
        window.draw_string(win_message,x,y)  
    else:
        window.draw_string(lose_message + '.',x,y)
    y = y + font_height        
    correct_message = 'The correct answer is ' + correct_answer
    window.draw_string(correct_message,x,y)
    
def get_guess(window,text_size,text_color,start_letter):
    x = 0
    y = 0
    window.set_font_size(text_size)
    window.set_font_color(text_color)     
    prompt_for_word = 'What word starts with the letter '
    guess = window.input_string(prompt_for_word + start_letter + '?',x,y)
    return guess
    
def display_words(window,text_size,text_color,word_list):
    pause_time = 2
    x = 0
    y = 0
    for word in word_list:
	    window.set_font_size(text_size)
	    window.set_font_color(text_color)		
	    window.draw_string(word,x,y)
	    time.sleep(pause_time)
	    # CLEAR WINDOW
	    window.clear()
	    # DISPLAY ICON
	    display_icon(window)   
	    
def display_icon(window):
    # displays the icon
    # - window is a uagame.Window object on which the icon appears
    icon_color = 'green'
    icon_size = 100
    icon_string = 'UA'
    window.set_font_color(icon_color)
    window.set_font_size(icon_size)
    window_width = window.get_width()
    icon_width = window.get_string_width(icon_string)
    x_icon = window_width - icon_width
    y_icon = 0
    window.draw_string(icon_string,x_icon,y_icon)

def display_instrcutions(window,text_size,text_color,font_height):
    # display instuctions
    # - window

    window.set_font_size(text_size)
    window.set_font_color(text_color)
    x = 0
    y = 0
    instruction_list = ['A sequence of words will be displayed','You will be asked which words starts with','a particular letter.','You win if you enter the right word.']
    for instruction in instruction_list:
	    window.draw_string(instruction,x,y)
	    y = y + font_height 
    # prompt player to press enter
    prompt1 = 'Press the enter key to display the words.'
    window.input_string(prompt1,x,y)    
    
        
main()
