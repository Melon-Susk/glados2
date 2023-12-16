from selenium import webdriver
from general import General
import time

#Global Variables
EMAILS = []
PASSWORD = input("Passwort:")
emailAmount = input("Accountanzahl:")

#Init Stuff
for i in range(1, int(emailAmount) + 1):
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
        login = General.loginAndWorldSelect(driver, EMAILS[i], PASSWORD, loginWaitTime=10)
        nextAccount = input("Continue?")

        if nextAccount == "":
            driver.quit()
        else:
            driver.quit()
            go = False
            break