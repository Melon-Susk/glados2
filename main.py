from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from general import General
from construction import Construction
from recruitment import Recruitment
from silver import Silver
from util import Util
import time
from datetime import datetime

EMAILS = ["unvish112+glados@gmail.com", "unvish112+glados1@gmail.com"]
PASSWORD = "samesame"
CASTLENAMES = Util.loadJsonToDict('castlenames.json')
BUILDING_NAMES = ["Bergfried", "Zeughaus", "Taverne", "Bibliothek", "Wehranlagen", "Markt", 
                  "Bauernhof", "Holzfäller", "Holzlager", "Steinbruch", "Steinlager", "Erzmine", "Erzlager"]

#Init Stuff
castlesSilver = {}


#ACCOUNT LOOP
while True:
    i = 0
    for i in range(len(EMAILS)):
        #Instantiate Driver
        driver = webdriver.Firefox()
        driver.set_window_size(1920, 1080)
        driver.get("https://www.lordsandknights.com")

        #Login and load World
        login = General.loginAndWorldSelect(driver, EMAILS[i], PASSWORD)
        #Select Main Castle for loop start
        General.selectMainCastle(driver, CASTLENAMES[EMAILS[i]])
        loopStart = False
        castleSafety = 0


        #CASTLE LOOP
        while castleSafety < 100:
            #General Castle Data
            name, points = General.getCastleNameAndPoints(driver)
            resourceDict = General.getResourceAmount(driver)

            #Check for Loop Completion
            if (name == CASTLENAMES[EMAILS[i]]) and (loopStart):
                break
            loopStart = True
            castleSafety += 1

            print(f"Ausgewählte Burg: {name}\nPunkte: {points}\nHolz: {resourceDict['Holz']}, Stein: {resourceDict['Stein']}, Erz: {resourceDict['Erz']}")


            #Silver
            try:
                silv = castlesSilver[name]
            except:
                castlesSilver[name] = datetime.now()
                silv = castlesSilver[name]
            newDay = Util.checkNewDay(silv)
            if newDay:
                General.openBuildingMenu(driver)
                eligibleSilver = Silver.openKeepMenu(driver)
                if eligibleSilver:
                    castlesSilver[name] = Silver.buySilver(driver)
                Util.reset(driver)


            #Building Construction
            General.openBuildingMenu(driver)
            activeConstruction = Construction.checkForActiveConstruction(driver)
            if not activeConstruction:
                buildingLevels = Construction.getBuildingLevels(driver, BUILDING_NAMES)
                buildOrderArray = Construction.createBuildOrder(buildingLevels, resourceDict)
                Construction.startConstruction(driver, buildOrderArray)
            Util.reset(driver)


            #Recruitment
            General.openBuildingMenu(driver)
            eligibleRecruitment = Recruitment.openBarracksMenu(driver)
            if eligibleRecruitment:
                amount = Recruitment.getCurrentUnitAmount(driver)
                recruitmentPlan = Recruitment.determineRecruitmentPlan(points, amount)
            Util.reset(driver)


            #Switch to next Castle
            time.sleep(1)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_RIGHT)
            print("")
            time.sleep(3)

        driver.quit()
        time.sleep(3)
    
    break
    #time.sleep(60)



