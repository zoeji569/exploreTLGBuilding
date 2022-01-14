#!/usr/bin/env python3
""" A simple program that allows user to explore TLG building. | Xuan.Ji@tlgcohort.com  Zicheng.Li@tlgcohort.com"""

# imports
import time # use time.sleep() in conversations
from datetime import date # used in Room 103
from datetime import timedelta # used in Room 103
import crayons # highlight some conversations/words
import requests # request API from OpenWeatherMap
import config


def main():
    ## A dictionary linking a room to other rooms
    rooms = {'lobby': {
                'name': '100',
                'available_directions' : 'Left, Right, Up',
                'L': '101',
                'R': '103',
                'U': '203',
                'coins': '1',
                'words': 'This is lobby.'},
             '101': {
                 'name': '101',
                 'available_directions': 'Left, Right, Up',
                 'L': '102',
                 'R': 'lobby',
                 'U': "201",
                 'coins': '2',
                 'words': 'This is Nancy Gale\'s office.'},
             '102': {
                 'name': '102',
                 'available_directions': 'Right, Up',
                 'U': '202',
                 'R': '201',
                 'coins': '2',
                 'words': 'This is Jay Rostosky\'s office.'},

             '103': {
                 'name': '103',
                 'available_directions': 'Left, Up',
                 'L': 'lobby',
                 'U': '204',
                 'coins':'1',
                 'words': 'This is Nelly Sugu\'s office'},
             '201': {
                'name': '201',
                'available_directions': 'Left, Right, Down',
                'L': '202',
                'R': '203',
                'D': '101',
                'coins': '3',
                'words': 'This is Sam Griffith\'s office'},
             '202': {
                'name': '202',
                'available_directions': 'Right, Down',
                'R': '201',
                'D': '102',
                'coins': '0',
                'words': 'This is John and Richard\'s office.'},
             '203': {
                'name': '203',
                'available_directions': 'Left, Down, Right',
                'L': '201',
                'R': '204',
                'D': '100',
                'coins': '0',
                'words': 'This is Meeting Room.'},
            '204': {
                'name': '204',
                'available_directions': 'Left, Down',
                'L': '203',
                'D': '103',
                'coins': '0',
                'words': 'This is snack room. We have some beverages in vending machine.'},
             }
    # movements
    directions = ['L', 'R', 'U', 'D']
    # start the player in the lobby
    current_room = rooms['lobby']
    coins = 0

    """called at runtime"""
    # open building ASCII file in read mode
    with open("ASCII arts/building.txt", "r") as building:
        # indent to keep the building object open
        # loop across the lines in the file
        for svr in building:
            # print and end without a newline
            print(svr, end="")
    print()

    """Show the game instructions when called"""
    def showInstructions():
        print(crayons.cyan('Please use L,R,U,D to move. Press Q to quit game.', bold=True))
    showInstructions()

    user_name=input("Please enter your name: ") # get user's name
    print(f"Hello, {user_name}! Welcome to TLG building!") # welcome message
    time.sleep(1)

    while True:
        # display current location
        print()
        print('You are in Room {}.'.format(current_room['name']))
        print(crayons.cyan(current_room['words'], bold=True))
        # show coins user found in current room
        if current_room['coins']:
            print(f"You found: " + current_room['coins'] + " coins in this room!")
        coins += int(current_room['coins'])
        # show total number of coins user have collected since game started
        print(f'You\'ve collected {coins} coins.')


        # different tasks in each room
        room_number = int(current_room['name'])
        # task in room 101
        if room_number == 101:
            print(f"Nancy: Hello {user_name}, Happy learning!")
        # task in room 102, user got 3 chances to guess correct numbers.
        elif room_number == 102:
            round = 0
            while True:
                round += 1
                print("The door is locked... It has a 3-digit password, would you like to guess what it is?")
                digit_1 = input(
                        "Digit 1 :(Hint:Temperature in Rochester,New York on Feb 27th, 2020 was ___ degree °F. ) Your guess--> ")
                digit_2 = input(
                        "Digit 2: (Hint:How many instructors we've had so far since the Apprenticeship program started (Including Sam)?) Your guess--> ")
                digit_3 = input("Digit 3: (Sorry, no more hint :) Your guess--> ")

                if digit_1 == '6' and digit_2 == '5' and digit_3 == '8':  # logic to check if user gave correct answer
                    print('Correct! You unlocked the door and found Jay sitting in there.')
                    print('Jay: You have a good memory! But it seems like I need to change my door password!')
                    print(
                            'Jay throw you a book -- <Effective Java> and asked you to read it 10 times. Then Jay kicked you out from his office.')
                    break  # break statement escapes the while loop
                elif round == 3:  # logic to ensure round has not yet reached 3
                    print(
                            'Sorry, you\'ve used all your chances. Now you\'ve triggered the alarm. Please go to another room so people won\'t catch ya!(You are welcome!)')
                    break  # break statement escapes the while loop
                else:  # if answer was wrong, and round is not yet equal to 3
                    print('Sorry. Try again!')

        # task in room 103, user's input will be wrote to file stuff_i_learnt_yesterday.txt.
        elif room_number == 103:
            learn=input(f"Nelly: Hi {user_name}, what did you learn last night?\nYou:")
            my_learn = open("stuff_i_learnt_yesterday.txt", "a")
            today = date.today()
            yesterday = today - timedelta(days = 1)
            my_learn.write(f"\nYesterday was: {yesterday}, {learn}\n")
            my_learn.close()
            print("Nelly: Great to hear that! You can see your answer in file named: stuff_i_learnt_yesterday.txt.\nNelly: Keep track of everything you're learning, it's a good habit.")
        # task in room 201
        elif room_number == 201:
            print(f"Sam: Hi {user_name}! I hope you enjoyed this course!")
            print(f"Sam: Sorry I'm busy watching your classmates' project, talk to you later!")

        # task in room 202. Use OpenWeatherMap API to get weather info when user enter City and State.
        elif room_number == 202:
            print(f"John: Hi {user_name}! How are you? I'm planning to go some other city today, "
                      f"do you have any suggestions?")
            print("Please enter a city name of USA")
            city = input("city: ")
            state = input("state: ")
            print(f"John: Great! Wait a second and let me take a look of the weather there.")
            api_url = "http://api.openweathermap.org/data/2.5/weather?"
            look_url = api_url + "appid=" + config.api_key + "&q=" + city + "," + state + ",usa"
            response = requests.get(look_url)
            x = response.json()
            # check for a 200 response
            if x["cod"] == 200:
                    y = x["main"]
                    current_temperature = y["temp"]
                    temp_in_f = (current_temperature - 273.15) * 9 / 5 + 32
                    formatted_temp_in_f = "{:.2f}".format(temp_in_f)
                    print(f"John: The temperature of {city}, {state} today is:\n{current_temperature} Kelvin, which is about {formatted_temp_in_f} °F.")
                    if temp_in_f >= 90:
                        print(f"It might be too hot to visit {city} now, I may go visit there next time! Thank you!")
                    elif temp_in_f >= 70:
                        print(f"It's pretty warm in {city}, nice weather for swimming! Thank you!")
                    elif temp_in_f >= 50:
                        print(f"It's a nice weather in {city}, great weather for outdoor activities! Thank you!")
                    elif temp_in_f >= 40:
                        print(f"It's a cool weather in {city}, I'll need to bring a jacket or a sweater. Thank you!")
                    elif temp_in_f >= 10:
                        print(f"It's pretty cold in {city}, I may need several layers on to be outside. Thank you!")
                    elif temp_in_f < 10:
                        print(f"Oh it's extremely cold in {city} now, I may go visit there next time! Thank you!")
            else:
                    print(" City Not Found ")
            print("Wondering what is the weather looking like in next 5 days")

        # task in room 203
        elif room_number == 203:
                print("Welcome to our Meeting room!")
                time.sleep(2)
                print("This room will be used by some guest from our partner company. You wanna check who's using it today?")
                time.sleep(2)
                print("Amaris!!")
                time.sleep(2)
                print(f"Amaris: Hi! Long time no see! Today, I have a quiz for you, You'll have 3 chances to answer. If you cannot answer correcly, you may be failed from Apprentice program.")
                round = 0  # integer round initiated to 0
                while True:  # sets up an infinite loop condition
                    round += 1  # increase the round counter
                    print('Which of the following is NOT one of Amazon\'s Leadership Principles? ''\n'
                          'A-Invent and Simplify''\n'
                          'B-Earn Trust''\n'
                          'C-Have Backbone; Disagree and Commit''\n'
                          'D-Spend money as much as you can')
                    answer = input("Your guess--> ")  # string answer collected from user
                    if answer == 'D':  # logic to check if user gave correct answer
                        print('Correct!')
                        break  # break statement escapes the while loop
                    elif round == 3:  # logic to ensure round has not yet reached 3
                        print('Sorry, the answer was D.')
                        break  # break statement escapes the while loop
                    else:  # if answer was wrong, and round is not yet equal to 3
                        print('Sorry. Try again!')
        # task in room 204
        elif room_number == 204:
                time.sleep(1)
                # open directory ASCII file in read mode
                with open("ASCII arts/vending_machine.txt", "r") as vending:
                    # indent to keep the building object open
                    # loop across the lines in the file
                    for svr in vending:
                        # print and end without a newline
                        print(svr, end="")
                print()


                # check if user have enough coins to purchase
                if coins < 1:
                    print("Sorry, you don't have enough coins. Please explore more rooms and get coins. See you later!")
                elif coins >= 1:
                    exchange = input(
                    f"Would you like something to drink? You've collected {coins} coins. Each beverage will cost 1 coin. Enter Y/N ")

                    # user select from different beverage by enter different letters.
                    if exchange == 'Y':
                        bev_choice=input(" We have [C]oke, [S]prite, [F]anta, [W]ater, and [L]emondade ")

                        bev_dict={'C':'ASCII arts/coke.txt',
                            'S':'ASCII arts/sprite.txt',
                            'F':'ASCII arts/fanta.txt',
                            'W':'ASCII arts/water.txt',
                            'L':'ASCII arts/lemonade.txt'}
                        if bev_choice in bev_dict:
                            bevfiletxt = bev_dict[bev_choice]
                            print("Getting your item... please wait...")
                            time.sleep(2)
                            coins -= 1
                            with open(str(bevfiletxt), "r") as bevfile:
                                # indent to keep the building object open
                                # loop across the lines in the file
                                for svr in bevfile:
                                    # print and end without a newline
                                 print(svr, end="")
                        print()
                        print("Here you go! Enjoy it!")
                        print("Thanks for purchasing! ")
                        # show coins left
                        print(f"Now you have {coins} coins.")

        # get user input
        movement = input('\nWhich direction do you want to go? Available directions for Room {}'.format(current_room['name']) + ' is: {}'.format(current_room['available_directions']) + '-->')
        # movement
        if movement in directions:
             if movement in current_room:
                 current_room = rooms[current_room[movement]]

             else:
                 # bad movement
                 print("Sorry, you can't go that way. Please select again. ")

        # quit game
        elif movement.lower() in ('q', 'quit'):
            print(crayons.cyan("Have a nice day!",bold=True))
            break

        # Invalid movement
        else:
            print("Sorry, I don't understand that movement. Please select again.")
            time.sleep(1)




if __name__ == "__main__":
    main()# this calls main function
input('Press ENTER to exit')


