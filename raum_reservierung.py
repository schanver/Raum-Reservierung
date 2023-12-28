from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

info = []

def read_from_file():
    with open("credentials.txt",'r') as file:
        for line in file:
            info.append(line.strip())

def get_a_reservation():
    attempts = 5
    username = info[0]
    password = info[1]
    while True:
        try:
            browser = webdriver.Firefox()
            browser.get("https://saml2.cs.tu-dortmund.de/simplesaml/module.php/core/loginuserpass.php?AuthState=_09df7bb7f6e78e060d04f4d017e93dae9e16a08205%3Ahttps%3A%2F%2Fsaml2.cs.tu-dortmund.de%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fraumadm.cs.tu-dortmund.de%252FRaumId%26RelayState%3D%252Fcont%252Fde%252Flernraum%252Fsaml2%252Fdologin.sh%26cookieTime%3D1703414214")
      

            #Find and fill login information
            nutzername = browser.find_element(By.ID, 'username')
            passwort = browser.find_element(By.ID,'password')

            nutzername.send_keys(username)
            passwort.send_keys(password)

            login_button = browser.find_element(By.CLASS_NAME, 'btn')
            login_button.click()

            #Reservation page 
            WebDriverWait(browser,5).until(EC.title_contains('TU Dortmund - Fak. fuer Informatik / Raumadministration'))
           
            while True:
                attempt -= 1

                if attempt == 0:  #Check if there were too many unsuccessful attempts
                    print("Operation aborted.Please try again later.")
                    break

                target_cell = browser.find_elements(By.PARTIAL_LINK_TEXT, '>')
                if(len(target_cell) > 1):
                    target_cell[1].click()
                h2_element = browser.find_elements(By.TAG_NAME, 'h2')
                if h2_element[1].text == "RAUMBELEGUNG AM 10.01.2024":
                    break

            # Find the target cell ( For now it is OH12/4.037 ab 13 Uhr) 
            time_block = browser.find_element(By.XPATH, "//a[@title='Reservieren von Raum OH12/4.037 ab 13:00 Uhr']")
            time_block.click()
            
            title_field = WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.NAME, 'comment')))
            title_field.send_keys('Logik')

            time_period = Select(browser.find_element(By.NAME, 'mitlerner'))
            time_period.select_by_index(0)

            till = Select(browser.find_element(By.NAME, 'bis'))
            till.select_by_index(len(till.options)-1)
            
            submit_button = browser.find_element(By.XPATH, '//input[@name="action" and @value="Reservieren"]')
            submit_button.click()

            browser.implicitly_wait(2)
            browser.save_full_page_screenshot("raumreservierung.png")
            print("Den Raum wird für dich reserviert.")
            break
        finally:
            break 

            

#get_a_reservation()
read_from_file()
uname = info[0]
passw = info[1]

print(uname + " " + passw)
