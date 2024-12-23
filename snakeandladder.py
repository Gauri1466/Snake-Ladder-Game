import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load sound effects
coin_move_sound = pygame.mixer.Sound(r"C:\Users\Gauri\Downloads\sounds\coin_move.mp3")
ladder_climb_sound = pygame.mixer.Sound(r"C:\Users\Gauri\Downloads\sounds\ladder_climb.mp3")
snake_bite_sound = pygame.mixer.Sound(r"C:\Users\Gauri\Downloads\sounds\snake_bite.mp3")
win_sound = pygame.mixer.Sound(r"C:\Users\Gauri\Downloads\sounds\win_sound.mp3")


# Global variables
player_1 = None
player_2 = None
current_position_1 = 0
current_position_2 = 0
turn = 1  # Player 1 starts
Dice = []
index = {}
consecutive_sixes = {1: 0, 2: 0}  # To track consecutive sixes for each player
game_over = False  # To track if the game is finished

def start_game():
    global dice_button, message_label, player_buttons

    # Buttons for players
    player_buttons = {
        1: tk.Button(win, text="Player - 1", height=2, width=10, fg="red", bg="cyan",
                     font=('Cursive', 14, 'bold'), activebackground='blue', command=lambda: roll_dice(1)),
        2: tk.Button(win, text="Player - 2", height=2, width=10, fg="red", bg="cyan",
                     font=('Cursive', 14, 'bold'), activebackground='orange', command=lambda: roll_dice(2)),
    }
    player_buttons[1].place(x=1000, y=350)
    player_buttons[2].place(x=1000, y=520)

    # Dice image button
    global dice_button
    dice_button = tk.Button(win, image=Dice[0], height=80, width=80, bg="blue")
    dice_button.place(x=1025, y=420)

    # Exit button
    b3 = tk.Button(win, text="END", height=1, width=10, fg="red", bg="black",
                   font=('Cursive', 14, 'bold'), activebackground='red', command=win.destroy)
    b3.place(x=1000, y=0)

    # Message Label
    global message_label
    message_label = tk.Label(win, text="Player 1's turn!", font=('Cursive', 14, 'bold'), fg="black", bg="yellow")
    message_label.place(x=400, y=800)

def reset_coin():
    global player_1, player_2, current_position_1, current_position_2, consecutive_sixes, game_over
    current_position_1 = 0
    current_position_2 = 0
    consecutive_sixes = {1: 0, 2: 0}
    game_over = False
    player_1.place(x=index[1][0], y=index[1][1])
    player_2.place(x=index[1][0] + 40, y=index[1][1])  # Offset for player 2

def local_dice_images():
    global Dice
    names = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
    for nam in names:
        image_path = r"C:\Users\Gauri\Downloads\images" + "\\" + nam
        im = Image.open(image_path)
        im = im.resize((65, 65))
        im = ImageTk.PhotoImage(im)
        Dice.append(im)
# def check_ladder(turn):
#     global current_position_1,current_position_2
#     global ladder
#     f=0 #no ladder
#     if turn==1:
#         if current_position_1 in ladder:
#             current_position_1=ladder[current_position_1]
#             f=1
#     else:
#         if current_position_2 in ladder:
#             current_position_2=ladder[current_position_2]
#             f=1
#     return f
def roll_dice(player):
    global Dice, current_position_1, current_position_2, turn, consecutive_sixes, game_over

    if game_over:
        return

    if turn != player:
        message_label.config(text=f"Not Player {player}'s turn!")
        return

    # Roll the dice
    r = random.randint(1, 6)
    print(f"Dice roll: {r}")

    # Update dice image
    dice_button.config(image=Dice[r - 1])

    # Handle consecutive sixes
    if r == 6:
        consecutive_sixes[turn] += 1
    else:
        consecutive_sixes[turn] = 0  # Reset consecutive sixes if not 6

    # Handle three consecutive sixes
    if consecutive_sixes[turn] == 3:
        message_label.config(text="Lalch buri bala hai! Turn skipped!")
        consecutive_sixes[turn] = 0
        turn = 2 if turn == 1 else 1
        return

    # Update player position
    current_position = current_position_1 if turn == 1 else current_position_2
    new_position = current_position + r

    if new_position > 64:
        message_label.config(text=f"Player {turn} cannot move beyond position 64!")
        return

    # Check for ladders or snakes
    if new_position in ladder:
        pygame.mixer.Sound.play(ladder_climb_sound)
        message_label.config(text=f"Player {turn} climbs a ladder!")
        new_position = ladder[new_position]
    elif new_position in Snake:
        pygame.mixer.Sound.play(snake_bite_sound)
        message_label.config(text=f"Player {turn} gets bitten by a snake!")
        new_position = Snake[new_position]

    # Move the player's coin
    pygame.mixer.Sound.play(coin_move_sound)
    move_coin(new_position, player_1 if turn == 1 else player_2)
    if turn == 1:
        current_position_1 = new_position
    else:
        current_position_2 = new_position

    # Check for win
    if new_position == 64:
        pygame.mixer.Sound.play(win_sound)
        message_label.config(text=f"Player {turn} wins!")
        display_winner_popup(turn)
        game_over = True
        return

    # Switch turn unless a six was rolled
    if r != 6:
        turn = 2 if turn == 1 else 1
    message_label.config(text=f"Player {turn}'s turn!")

def display_winner_popup(player):
    """Display a button in the center of the board to announce the winner."""
    winner_button = tk.Button(
        win,
        text=f"Player {player} Wins!",
        font=('Cursive', 20, 'bold'),
        bg="gold",
        fg="black",
        command=win.destroy  # Close the game when the button is clicked
    )
    winner_button.place(x=500, y=400)  # Adjust the position to center of the board

def move_coin(new_position, player):
    if new_position in index:
        x, y = index[new_position]
        player.place(x=x, y=y)
    else:
        print(f"Invalid board position: {new_position}")

def get_index():
    global index
    num = [64, 63, 62, 61, 60, 59, 58, 57, 49, 50, 51, 52, 53, 54, 55, 56, 
           48, 47, 46, 45, 44, 43, 42, 41, 33, 34, 35, 36, 37, 38, 39, 40, 
           32, 31, 30, 29, 28, 27, 26, 25, 17, 18, 19, 20, 21, 22, 23, 24, 
           16, 15, 14, 13, 12, 11, 10, 9, 1, 2, 3, 4, 5, 6, 7, 8]

    row = 50
    i = 0
    for x in range(1, 9):  # 8 rows
        col = 50
        for y in range(1, 9):  # 8 columns
            if i < len(num):
                index[num[i]] = (col, row)
                i += 1
            col += 95
        row += 98
    print("Index mapping:", index)

#Ladder Bottom to top
ladder={1:30,4:11,17:33,24:60,28:38,36:46,41:55,49:63}
#snake bottom to top
Snake={62:47,58:20,54:44,51:35,40:22,34:14,13:3,}
# Tkinter window
win = tk.Tk()
win.geometry("1200x1000")
win.title("Snakes And Ladders")

# Create a frame
f1 = tk.Frame(win, width=1200, height=750, relief='raised')
f1.place(x=0, y=0)

# Set board
board_img = ImageTk.PhotoImage(Image.open(r"C:\Users\Gauri\Downloads\images\snakeladder.png"))
Lab = tk.Label(f1, image=board_img)
Lab.place(x=0, y=0)

# Player 1 coin
player_1 = tk.Canvas(win, width=30, height=30)
player_1.create_oval(10, 10, 30, 30, fill='blue')

# Player 2 coin
player_2 = tk.Canvas(win, width=30, height=30)
player_2.create_oval(10, 10, 30, 30, fill='orange')

# Initialize game
get_index()  # Map the board positions
local_dice_images()  # Load dice images
reset_coin()  # Place coins at the start
start_game()  # Set up game buttons

win.mainloop()
