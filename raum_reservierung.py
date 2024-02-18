

def read_from_file():
    pass

def menu():
    while True:
        day = str(input("Please enter date in which you want to reserve a room for (dd-mm-yyyy)")) 
	    pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$"        
