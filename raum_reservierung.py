import re

def read_from_file():
    pass

def menu():
    room_choice = 0
    while True:
        day = str(input("Please enter date in which you want to reserve a room for (dd-mm-yyyy)"))
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$"  
            if bool(re.match(pattern,day)) == True:
                break
        room_choice = str(input("Which room do you want to reserve? Here are the options? Choose from 1-5?
        1. OH12/xxxx
        2. OH12/yxyyy
        3. OH12/sssss
        4. OH12/dsdsds
"))
    room = rooms[room_choice]

