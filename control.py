from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

#Global Variables
EMAILS = []
PASSWORD = input("Passwort:")
emailAmount = input("Accountanzahl:")
startAccount = input("Startaccount:")

#Init Stuff
for i in range(int(startAccount), int(emailAmount) + 1):
    EMAILS.append(f"unvish112+glados{i}@gmail.com")
print(EMAILS)


#ACCOUNT LOOP
go = True
while go:
    i = 0
    for i in range(len(EMAILS)):
        #Instantiate Driver
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://www.lordsandknights.com")

        #Login and load World
        #wait until Email Form is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
        time.sleep(float(3))

        #get Elements
        loginEmail = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")
        loginPassword = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[2]/input")
        loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[3]/button")

        #send and submit login Data
        loginEmail.send_keys(EMAILS[i])
        loginPassword.send_keys(PASSWORD)
        loginButton.click()

        #Wait for World Selection Screen loading
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Wähle eine Welt"]')))
        time.sleep(float(3))
        #Click on latest played World
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]").click()

        nextAccount = input("Continue?")

        if nextAccount == "":
            driver.quit()
        else:
            driver.quit()
            go = False
            break