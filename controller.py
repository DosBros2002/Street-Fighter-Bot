import socket
import json
from game_state import GameState
from command import Command
from buttons import Buttons
import csv
#from bot import fight
import os
import sys
from bot import Bot
import pandas as pd
import ast 


training_data = pd.read_csv('generated_data.csv')
training_array = training_data.values

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def set_up_buttons(training_array, button=Buttons()):
    buttons_dict = {}

    buttons_dict['Up'] = False 
    buttons_dict['Down'] = False
    buttons_dict['Right'] = False
    buttons_dict['Left'] = False
    buttons_dict['Select'] = False 
    buttons_dict['Start'] = False 
    buttons_dict['Y'] = False 
    buttons_dict['B'] = False
    buttons_dict['X'] = False 
    buttons_dict['A'] = False 
    buttons_dict['L'] = False 
    buttons_dict['R'] = False

    if training_array[0] == 1:
        buttons_dict['Up'] = True 

    if training_array[1] == 1:
        buttons_dict['Down'] = True

    if training_array[2] == 1:
        buttons_dict['Up'] = True
    
    if training_array[3] == 1:
        buttons_dict['Down'] = True
    
    if training_array[4] == 1:
        buttons_dict['Right'] = True

    if training_array[5] == 1:
        buttons_dict['Left'] = True
    
    if training_array[6] == 1:
        buttons_dict['Y'] = True

    if training_array[7] == 1:
        buttons_dict['B'] = True
    
    if training_array[8] == 1:
        buttons_dict['X'] = True
    
    if training_array[9] == 1:
        buttons_dict['A'] = True
    
    if training_array[10] == 1:
        buttons_dict['L'] = True

    if training_array[11] == 1:
        buttons_dict['R'] = True            

    return buttons_dict

def main():
    headers = ['timer', 'fight_result', 'has_round_started', 'is_round_over', 
               'player1.player_id', 'player1.health', 'player1.is_crouching', 'player1.is_jumping', 
               'player1.is_player_in_move', 'player1.move_id', 'player1.x_coord', 'player1.y_coord', 
               'player1.player_buttons.up', 'player1.player_buttons.down', 'player1.player_buttons.right', 
               'player1.player_buttons.left', 'player1.player_buttons.select', 'player1.player_buttons.start', 
               'player1.player_buttons.Y', 'player1.player_buttons.B', 'player1.player_buttons.X', 
               'player1.player_buttons.A', 'player1.player_buttons.L', 'player1.player_buttons.R', 
               'player2.player_id', 'player2.health', 'player2.is_crouching', 'player2.is_jumping', 
               'player2.is_player_in_move', 'player2.move_id', 'player2.x_coord', 'player2.y_coord', 
               'player2.player_buttons.up', 'player2.player_buttons.down', 'player2.player_buttons.right', 
               'player2.player_buttons.left', 'player2.player_buttons.select', 'player2.player_buttons.start', 
               'player2.player_buttons.Y', 'player2.player_buttons.B', 'player2.player_buttons.X', 
               'player2.player_buttons.A', 'player2.player_buttons.L', 'player2.player_buttons.R']
    column_names = "timer,fight_result,has_round_started,is_round_over,player1.player_id,player1.health,player1.is_crouching,player1.is_jumping,player1.is_player_in_move,player1.move_id,player1.x_coord,player1.y_coord,player1.player_buttons.up,player1.player_buttons.down,player1.player_buttons.right,player1.player_buttons.left,player1.player_buttons.select,player1.player_buttons.start,player1.player_buttons.Y,player1.player_buttons.B,player1.player_buttons.X,player1.player_buttons.A,player1.player_buttons.L,player1.player_buttons.R,player2.player_id,player2.health,player2.is_crouching,player2.is_jumping,player2.is_player_in_move,player2.move_id,player2.x_coord,player2.y_coord,player2.player_buttons.up,player2.player_buttons.down,player2.player_buttons.right,player2.player_buttons.left,player2.player_buttons.select,player2.player_buttons.start,player2.player_buttons.Y,player2.player_buttons.B,player2.player_buttons.X,player2.player_buttons.A,player2.player_buttons.L,player2.player_buttons.R"

    # Set up the CSV file
    csv_file = 'dataset.csv'
    file_exists = os.path.isfile(csv_file)

    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()
    bot_command = Command()
    button = Buttons()
    count = 0
    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)

        # Convert the string representation of the list to an actual list
        row_values_list = (current_game_state.get_game_data())
        flat_list = []

        for element in row_values_list:
            if isinstance(element, list):
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        

        # Create a DataFrame using the column names and row values
        df = pd.DataFrame([flat_list], columns=column_names.split(','))

        # Append the DataFrame to the CSV file
        with open(csv_file, 'a', newline='') as f:
            if not file_exists:
                df.to_csv(f, header=True, index=False)
                file_exists = True
            else:
                df.to_csv(f, header=False, index=False)        
        

        #bot_command = bot.fight(current_game_state,sys.argv[1])
        button.dict_to_object(set_up_buttons(training_array[count]))
        count = count + 1
        bot_command.player_buttons = button

        send(client_socket, bot_command)
if __name__ == '__main__':
   main()
