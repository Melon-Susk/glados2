from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from util import Util
import time

#Global Variables
EMAILS = []
PASSWORD = input("Passwort:")
MODE = input("Zeitmodus?")

if MODE != "":
    emailAmount = input("Accountanzahl:")
    startAccount = input("Startaccount:")

    for i in range(int(startAccount), int(emailAmount) + 1):
        EMAILS.append(f"unvish112+glados{i}@gmail.com")
    print(EMAILS)
else:
    USEDACCOUNTS = {}
    timeSortedAccounts = Util.loadDatetimeJsonTodict('timeSortedAccounts.json')
    referenceAccounts = Util.loadJsonToDict('castlenames.json')

    for key in timeSortedAccounts:
        EMAILS.append(key)
    
    print(EMAILS)


#ACCOUNT LOOP
go = True
while go:
    i = 0
    for i in range(len(EMAILS)):
        #Instantiate Driver
        options = Options()
        options.binary_location = r'C:/Users/Lukas.Gosch/AppData/Local/Mozilla Firefox/firefox.exe'
        service = Service(executable_path=r'C:/Users/Lukas.Gosch/Documents/Privat/geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=options)

        #driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://www.lordsandknights.com")

        #Login and load World
        #wait until Email Form is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
        time.sleep(float(1))

        #Change language
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div")))
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="DE"]')))
        driver.find_element(By.XPATH, '//*[text()="DE"]').click()
        time.sleep(float(1))

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
        time.sleep(float(1))
        #Click on latest played World
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]").click()

        del timeSortedAccounts[EMAILS[i]]
        nextAccount = input("Continue?")

        if nextAccount == "":
            driver.quit()
        else:
            driver.quit()
            go = False
            break


#Update time sorted Accounts Dict
Util.refreshDatetimeDict(timeSortedAccounts, referenceAccounts)