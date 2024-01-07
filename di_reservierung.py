from selenium import webdriver
import selenium
from selenium.webdriver import support
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

info = []

# TODO: Add the option to get back to back reservations

def read_from_file():
    with open("credentials.txt",'r') as file:
        for line in file:
            info.append(line.strip())

def get_a_reservation():
    read_from_file()
    username = info[0]
    password = info[1]
    browser = webdriver.Firefox()
    while True:
        try: 
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
           
            
                # Go to the next day till you reach 8 days later 
            loop = 1
            while loop <= 8:
                target_cell = browser.find_elements(By.PARTIAL_LINK_TEXT, '>')
                if(len(target_cell) > 1):
                    target_cell[1].click()
                loop += 1
                
            today = datetime.now()

            time_block_xpaths = [
    "//a[@title='Reservieren von Raum OH12/4.037 ab 14:00 Uhr']",
    "//a[@title='Reservieren von Raum OH12/4.029 ab 14:00 Uhr']",
    "//a[@title='Reservieren von Raum OH12/4.042 ab 14:00 Uhr']"
                                ]
            attempts = 0
            if today.weekday() == 2: 
               for time_block_xpath in time_block_xpaths:
                    try:
                        time_block = browser.find_element(By.XPATH, time_block_xpath)
                        time_block.click()

                        # Check if submit_button is present
                        try:
                            submit_button = WebDriverWait(browser, 2).until(
                            EC.element_to_be_clickable((By.XPATH, '//input[@name="action" and @value="Reservieren"]')))
            

                            title_field = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.NAME, 'comment')))
                            title_field.send_keys('DAP1')

                            time_period = Select(browser.find_element(By.NAME, 'mitlerner'))
                            time_period.select_by_index(0)

                            till = Select(browser.find_element(By.NAME, 'bis'))
                            till.select_by_index(len(till.options) - 1)

                            # Submit the form
                            submit_button.click()
                            break  # Break out of the loop if successful
                        except NoSuchElementException:
                            # If submit_button not found, continue to the next time block
                            attempts += 1
                            continue
                    except NoSuchElementException:
                        # If time_block not found, continue to the next time block
                        attempts += 1
                        continue

            if attempts > 2:
                print("Booking operation failed. Please try again")
                exit()     

            browser.implicitly_wait(2)
            browser.save_full_page_screenshot("raumreservierung.png")
            print("Den Raum wird für dich reserviert.")
            break
        finally:
            browser.quit()

            

get_a_reservation()

