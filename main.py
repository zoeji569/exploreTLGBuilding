#!/usr/bin/env python3
""" A simple program that allows user to explore TLG building. | Xuan.Ji@tlgcohort.com  Zicheng.Li@tlgcohort.com"""

# imports
import time # use time.sleep() in conversations
from datetime import datetime, date, timedelta # used in Room 103
import crayons # highlight some conversations/words
import requests # request API from OpenWeatherMap
import config # "hide" private API Key
from twython import Twython, TwythonError # "hide" private API Key
import math
import matplotlib.pyplot as plt


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
    private_key = Twython(config.api_key)

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
            print(f"Nancy: Hello {user_name}, welcome to TLG! Please feel free to look around!")
        # task in room 102, user got 3 chances to guess correct numbers.
        elif room_number == 102:
            round = 0
            while True:
                round += 1
                print("The door is locked... It has a 3-digit password, would you like to guess what it is?")
                digit_1 = input(
                        "Digit 1 :(Hint: Temperature in Rochester,New York on Feb 27th, 2020 was ___ degree °F. ) Your guess--> ")
                digit_2 = input(
                        "Digit 2: (Hint: How many instructors we've met so far since the Apprenticeship program started?) Your guess--> ")
                digit_3 = input("Digit 3: (Sorry, no more hint :) Your guess--> ")

                if digit_1 == '6' and digit_2 == '5' and digit_3 == '8':  # logic to check if user gave correct answer
                    print('Correct! You unlocked the door and found Jay sitting in there.')
                    print('Jay: You have a good memory! But it seems like I need to change my door password!')
                    print(
                            'Jay throw you a book -- <Effective Java> and asked you to read it 10 times before OJT. \nThen Jay kicked you out from his office.')
                    break  # break statement escapes the while loop
                elif round == 3:  # logic to ensure round has not yet reached 3
                    print(
                            'Sorry, you\'ve used all your chances. Now you\'ve triggered the alarm!! Please run to another room so people won\'t catch ya!(You are welcome!)')
                    break  # break statement escapes the while loop
                else:  # if answer was wrong, and round is not yet equal to 3
                    print('Password incorrect. Try again!')

        # task in room 103, user's input will be wrote to file stuff_i_learnt_yesterday.txt.
        elif room_number == 103:
            learn=input(f"Nelly: Hi {user_name}, what did you learn yesterday?\nYou:")
            my_learn = open("stuff_i_learnt_yesterday.txt", "a")
            today = date.today()
            yesterday = today - timedelta(days = 1)
            my_learn.write(f"\nYesterday was: {yesterday}, {learn}\n")
            my_learn.close()
            print("Nelly: Great to hear that! You can see your answer in file named: stuff_i_learnt_yesterday.txt.\nNelly: Keep track of everything you're learning, it's a good habit. Good luck!")
        # task in room 201
        elif room_number == 201:
            print(f"Sam: Hi {user_name}! I hope you enjoyed this course!")
            time.sleep(1)
            print("Sam: Sorry I'm busy watching your classmates' presentation, I'll talk to you later!")

        # task in room 202. Use OpenWeatherMap API to get weather info when user enter City and State.
        elif room_number == 202:
            print(f"John: Hi {user_name}! How are you? I'm planning to have a vacation in some other city later this week, but I'm worry about the weather. "
                      f"Do you have any suggestions?")
            print("Please enter a city name and state code in USA")
            city = input("city: ")
            state = input("state: ")
            api_url = "http://api.openweathermap.org/data/2.5/"
            forecast_url = api_url + "forecast?q=" + city + "," + state + ",us&appid=" + config.api_key
            response_forecast = requests.get(forecast_url)
            data_forecast = response_forecast.json()
            # check for a 200 response
            if data_forecast["cod"] == "200":
                data_dict = {data_forecast['list'][3]['dt_txt']: data_forecast['list'][3]['main']['temp'],
                             data_forecast['list'][11]['dt_txt']: data_forecast['list'][11]['main']['temp'],
                             data_forecast['list'][19]['dt_txt']: data_forecast['list'][19]['main']['temp'],
                             data_forecast['list'][27]['dt_txt']: data_forecast['list'][27]['main']['temp'],
                             data_forecast['list'][35]['dt_txt']: data_forecast['list'][35]['main']['temp']}

                # fix the data format from API
                dates = list(data_dict.keys())
                fixed_date = [element[:-9] for element in dates]
                temp_value = list(data_dict.values())
                temp = [math.trunc((element - 273.15) * 9 / 5 + 32) for element in temp_value]

                # create a new dictionary for terminal data.
                zip_iterator = zip(fixed_date, temp)
                fixed_dict = dict(zip_iterator)
                # print a table which shows next 5 days temperature
                print(f"Temperature in {city.upper()}, {state.upper()} for next 5 days:")
                # Print the names of the columns.
                print("{:<20} {:<15}".format('DATE', 'TEMP(°F)'))

                # print each data item.
                for key, value in fixed_dict.items():
                    temperature = value
                    print("{:<20} {:<15}".format(key, temperature))
                print("John: Great! Thanks for your suggestion!")
                print("(Please close the figure to move to another room.)")

                # bar chart for next 5 days temperature
                plt.figure(figsize=(9, 6))
                plt.rc('axes', titlesize=20, labelsize=15)
                plt.rc('xtick', labelsize=12)
                plt.title(f'5-Day Temperature Forecast\n {city.upper()} , {state.upper()}')
                plt.xlabel('Date')
                plt.ylabel('Avg Temp [°F]')


                plt.bar(fixed_date, temp)
                for index, val in enumerate(temp):
                    plt.text(x=index, y=val + 0.5, s=f"{val}" + "°F", fontdict=dict(fontsize=12))

                plt.show()
                plt.close()

            else:
                    print("City Not Found ")

        # task in room 203
        elif room_number == 203:
                print("Welcome to our Meeting room!")
                time.sleep(1)
                print("This room will be used by some guest from our partner company. Guess who's here today?")
                time.sleep(1)
                print("Amaris!!")
                time.sleep(1)
                print(f"Amaris: Hi {user_name}! Long time no see!\nToday, I have a quiz for you, you'll have 3 chances to answer.\nIf you cannot answer correcly, you may be failed from Apprentice program.")
                time.sleep(2)
                round = 0  # integer round initiated to 0
                while True:  # sets up an infinite loop condition
                    round += 1  # increase the round counter
                    print('Which of the following is NOT one of Amazon\'s Leadership Principles? ''\n'
                          'A - Invent and Simplify''\n'
                          'B - Earn Trust''\n'
                          'C - Have Backbone; Disagree and Commit''\n'
                          'D - Spend company\'s money as much as you like')
                    answer = input("Your guess--> ")  # string answer collected from user
                    if answer == 'D':  # logic to check if user gave correct answer
                        print('Correct!')
                        break  # break statement escapes the while loop
                    elif round == 3:  # logic to ensure round has not yet reached 3
                        print('Sorry, the answer was D. Please go talk to your manager.')
                        break  # break statement escapes the while loop
                    else:  # if answer was wrong, and round is not yet equal to 3
                        print('Sorry. Try again!')
        # task in room 204
        elif room_number == 204:
            path = 'ASCII arts/'

            def img_splitter(img):
                img_lines = img.splitlines()
                longest = 0
                for ind, line in enumerate(img_lines):
                    if line == "":
                        img_lines.pop(ind)
                    if len(line) > longest:
                        longest = len(line)
                for line in img_lines:
                    if len(line) < longest:
                        line.format(n=longest, c=" ")
                return img_lines

            def encrypt():
                imgList = []
                letterDICT = {'A': path + 'A.txt', 'B': path + 'B.txt', 'C': path + 'C.txt', 'D': path + 'D.txt',
                              'E': path + 'E.txt',
                              'F': path + 'F.txt', 'G': path + 'G.txt', 'H': path + 'H.txt', 'I': path + 'I.txt',
                              'J': path + 'J.txt',
                              'K': path + 'K.txt', 'L': path + 'L.txt', 'M': path + 'M.txt', 'N': path + 'N.txt',
                              'O': path + 'O.txt',
                              'P': path + 'P.txt', 'Q': path + 'Q.txt', 'R': path + 'R.txt', 'S': path + 'S.txt',
                              'T': path + 'T.txt',
                              'U': path + 'U.txt', 'V': path + 'V.txt', 'W': path + 'W.txt', 'X': path + 'X.txt',
                              'Y': path + 'Y.txt',
                              'Z': path + 'Z.txt'}

                letterScan = list(engLetters)
                for alphabet in letterScan:
                    if alphabet in letterDICT:
                        txtScan = letterDICT[alphabet]

                        with open(txtScan, 'r') as fr:
                            data = fr.read()
                            imgList.append(img_splitter(data))

                numLetters = len(imgList)
                zipped = zip(*imgList)
                for line in zipped:
                    match numLetters:
                        case 1:
                            print(line[0])
                        case 2:
                            print(line[0], line[1])
                        case 3:
                            print(line[0], line[1], line[2])
                        case 4:
                            print(line[0], line[1], line[2], line[3])
                        case 5:
                            print(line[0], line[1], line[2], line[3], line[4])
                        case 6:
                            print(line[0], line[1], line[2], line[3], line[4], line[5])
                        case 7:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6])
                        case 8:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7])
                        case 9:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8])
                        case 10:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8], line[9])
                        case 11:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8], line[9], line[10])
                        case 12:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8], line[9], line[10], line[11])
                        case 13:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8], line[9], line[10], line[11], line[12])
                        case 14:
                            print(line[0], line[1], line[2], line[3], line[4], line[5],
                                  line[6].line[7], line[8], line[9], line[10], line[11], line[12], line[13])
                print('\n')


            vm = path + "vending_machine.txt"
            with open(vm, 'r') as fr:
                print(fr.read(), end='\n')

                if coins < 1:
                    print("Sorry, you don't have enough coins. Please explore more rooms and get coins. See you later!")
                elif coins >= 1:
                    exchange = input(
                        f"Would you like something to drink? You've collected {coins} coins. "
                        f"Each beverage will cost 1 coin. Enter Y/N ")

                    # user select from different beverage by enter different letters.
                    if exchange.upper() == 'Y':
                        print("Sorry the machine is being hacked by the Aliens")
                        print("They want to know your choice by using their language")

                        decision = input("Use 2 coins to get the decoder to purchase the drink [Y/N]")
                        if decision.upper() == 'N':
                            message = "bye"
                            engLetters = message.upper()
                            print(message)
                            encrypt()

                        elif decision.upper() == 'Y':
                            bev_choice = input(
                                "Enter you drink types [coke], [sprite], [fanta], [water], and [lemonade]")
                            bev_choice = bev_choice.upper()
                            engLetters = bev_choice
                            encrypt()

                            bev_dict = {'COKE': path + "coke.txt",
                                        'SPRITE': path + 'sprite.txt',
                                        'FANTA': path + 'fanta.txt',
                                        'WATER': path + 'water.txt',
                                        'LEMONADE': path + 'lemonade.txt'}

                            if bev_choice in bev_dict:
                                bevfiletxt = bev_dict[bev_choice]
                                print("Getting your item... please wait...")
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

                    elif exchange.upper() == 'N':
                        print("Come back when you are thirsty")

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


