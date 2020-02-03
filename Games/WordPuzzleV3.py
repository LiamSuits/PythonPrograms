# Word Puzzle Version 3

# This program is a game where the player is prompted to guess all letter
# of a hidden word.

# create window
# display instructions as list
# display puzzle so far
# get guess
# wait for input
# get puzzle so far
# display puzzle so far
# display results
# end game

import uagame

def main():

    # create window
    window = create_window()
    string_coords = [0,0]
    guesses = 4
    correct_word = 'banana'
    puzzle = ['_','_','_','_','_','_']      
    puzzle_str = ' '.join(puzzle)
    instruction_list = ['I\'m thinking of a secret word.','Try and guess the word. You can guess one letter','at a time. Each time you guess I will show you','which letters have been correctly guessed and which','letters are still missing. You will have '+str(guesses)+' guesses to','guess all of the letters. Good luck!','The answer so far is:'+puzzle_str]    
    # display instructions
    display_instructions(window, instruction_list, string_coords)
    # play game
    is_win = play_game(window, puzzle, correct_word, guesses, string_coords)
    # display result
    output_result(window, is_win, correct_word, string_coords)
    # end game
    end_game(window, string_coords)
    
def create_window():
    # Create a window
    # return: a new uagame.Window object    
    screen_width = 500
    screen_height = 400
    window = uagame.Window("Word Puzzle 3", screen_width, screen_height)
    text_size = 20
    text_color = 'white'
    window.set_font_size(text_size)
    window.set_font_color(text_color)    
    return window

def draw_line(window, string, string_coords):
    # Display the string at the position string_coords and update the
    # y coordinate in string_coords to be one 'line' lower
    # - window is the uagame.Window object to draw to
    # - string is the string to display
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed    
    window.draw_string(string,string_coords[0],string_coords[1])
    string_coords[1] = string_coords[1] + window.get_font_height()

def display_instructions(window, instructions, string_coords):
    # Display the instructions for the game
    # - window is the uagame.Window object to draw to
    # - instructions is a list of strings containing the game's instructions
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed    
    font_height = window.get_font_height()
    for instruction in instructions:
        draw_line(window, instruction, string_coords)
        
def display_puzzle_string(window, puzzle, string_coords):
    # Display the current state of the puzzle to the screen.
    # Letters which have been guessed will be revealed. 
    # Non-guessed letters will be replaced with underscore 
    # characters.
    # - window is the uagame.Window object to draw to
    # - puzzle is a list representing the puzzles current state, 
    # each element is either a letter if that letter has been
    # guessed, or an underscore if it has not. 
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed    
    puzzle_str = ' '.join(puzzle)
    tell_puzzle = "The answer so far: "+puzzle_str
    draw_line(window,tell_puzzle,string_coords)    
                
def get_guess(window, num_guesses, string_coords):
    # Prompt the user for a password and indicate the number of
    # guesses remaining
    # - window is the uagame.Window object to draw to
    # - num_guesses is the int number of guesses remaining
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed
    # return: a string with the player's guess    
    guess_text = 'Guess a letter ('+str(num_guesses)+' Guesses Remaining):'
    guess = window.input_string(guess_text,string_coords[0],string_coords[1])
    string_coords[1] = string_coords[1] + window.get_font_height()
    return guess

def update_letters(puzzle, correct_word, guess):
    # Given a new guessed letter, update the state
    # of our puzzle. Only update letters if they 
    # haven't been guessed before.
    # - puzzle is a list representing the puzzles current state, 
    # each element is either a letter if that letter has been
    # guessed, or an underscore if it has not. 
    # - correct_word is a string or list containing the
    # answer
    # - guess is a string containing the players most
    # recent guessed letter
    # return : A boolean indicating if an update was performed    
    guess_correct = False
    for index in range(len(correct_word)):
        if guess == correct_word[index]:
            puzzle[index] = guess
            guess_correct = True
    return guess_correct

def is_word_found(puzzle):
    # Determines if the player has guessed all the letters
    # in the puzzle or not
    # - puzzle is a list representing the puzzles current state, 
    # each element is either a letter if that letter has been
    # guessed, or an underscore if it has not. 
    #return: a boolean indicating if all the letters have been guessed    
    if '_' in puzzle:
        word_found = False
    else:
        word_found = True
    return word_found

def play_game(window, puzzle, correct_word, max_guesses, string_coords):
    # Prompts the player for guesses and processes them until
    # the player has solved the puzzle or run out of guesses.
    # - window is the uagame.Window object to draw to
    # - puzzle is a list representing the puzzles current state, 
    # each element is either a letter if that letter has been
    # guessed, or an underscore if it has not. 
    # - correct_word is a string or list containing the
    # answer
    # - num_guesses is the maximum number of incorrect guesses allowed
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed
    #return: a boolean indicating if the player won or not    
    word_found = False
    guessed_letters = []
    # play game
    while max_guesses > 0 and word_found == False:
        guess = get_guess(window, max_guesses, string_coords)
        # get puzzle so far
        guess_correct = update_letters(puzzle, correct_word, guess)
        if guess_correct == False or guess in guessed_letters:
            max_guesses = max_guesses - 1
        guessed_letters.append(guess)     
        # display puzzle so far
        display_puzzle_string(window, puzzle, string_coords)
        word_found = is_word_found(puzzle)
    return word_found

def output_result(window, is_win, correct_word, string_coords):
    # Display whether the player was successful or unsuccessful
    # - window is the uagame.Window object to draw to
    # - is_win is a bool which is true if the player guessed the word
    # - correct_word is a string or list containing the
    # answer
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed    
    congrats = 'Good job! You found the word!'    
    console = 'Not quite, the correct word was '+correct_word+'. Better luck next time'
    if is_win:
        draw_line(window,congrats,string_coords)
    else:
        draw_line(window,console,string_coords)

def end_game(window, string_coords):
    # Prompt the player to end the game and close the window
    # - window is the uagame.Window object to draw to
    # - string_coords is a list containing the x,y int coordinates where
    # the next line should be displayed    
    end_prompt = 'Press enter to end the game'
    window.input_string(end_prompt,string_coords[0],string_coords[1])
    window.close()       
     
main()
