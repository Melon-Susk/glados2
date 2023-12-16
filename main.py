from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from general import General
from construction import Construction
from recruitment import Recruitment
from science import Science
from silver import Silver
from util import Util
import time
from datetime import datetime

#Global Variables
EMAILS = []
PASSWORD = input("Passwort:")
emailAmount = input("Accountanzahl:")
CASTLENAMES = Util.loadJsonToDict('castlenames.json')

#Init Stuff
castlesSilver = {}

for i in range(1, int(emailAmount) + 1):
    EMAILS.append(f"unvish112+glados{i}@gmail.com")
print(EMAILS)


#ACCOUNT LOOP
while True:
    i = 0
    for i in range(len(EMAILS)):
        #Instantiate Driver
        options = Options()
        options.add_argument("--headless")
        firefox_binary_path = "/snap/bin/geckodriver"
        service = Service(executable_path=firefox_binary_path)
        driver = webdriver.Firefox(service=service, options=options)
        #driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.lordsandknights.com")

        #Login and load World
        try:
            login = General.loginAndWorldSelect(driver, EMAILS[i], PASSWORD)
            #Kill Pop-Ups
            General.popupKiller(driver)
        except:
            print("Fehler beim Login!\n")
            driver.quit()
            time.sleep(3)
            continue
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
            try:
                if newDay and (points > 60):
                    General.openBuildingMenu(driver)
                    eligibleSilver = Silver.openKeepMenu(driver)
                    if eligibleSilver:
                        castlesSilver[name] = Silver.buySilver(driver)
                    Util.reset(driver)
            except Exception as e:
                print("Fehler bei der Silberbeschaffung!\n")
                print(e)


            #Building Construction
            try:
                General.openBuildingMenu(driver)
                activeConstruction = Construction.checkForActiveConstruction(driver)
                if not activeConstruction:
                    buildingLevels = Construction.getBuildingLevels(driver)
                    buildOrderArray = Construction.createBuildOrder(buildingLevels, resourceDict)
                    Construction.startConstruction(driver, buildOrderArray)
                Util.reset(driver)
            except Exception as e:
                print("Fehler beim Gebäudeausbau!\n")
                print(e)



            #Science
            if points > 60:
                General.openBuildingMenu(driver)
                researchAvailable = Science.openLibraryMenu(driver)
                if researchAvailable:
                    Science.startResearch(driver)
                Util.reset(driver)


            #Recruitment
            if points > 80:
                General.openBuildingMenu(driver)
                eligibleRecruitment = Recruitment.openBarracksMenu(driver)
                if eligibleRecruitment:
                    amount = Recruitment.getCurrentUnitAmount(driver)
                    recruitmentPlan = Recruitment.determineRecruitmentPlan(points, amount)
                Util.reset(driver)

            #Get New Resource Amount and write to File
            resourceDict = General.getResourceAmount(driver)
            Util.appendToOverviewJson('resourceOverview.json', EMAILS[i], name, resourceDict)

            #Switch to next Castle
            time.sleep(1)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_RIGHT)
            print("")
            time.sleep(3)

        driver.quit()
        time.sleep(3)
    
    print("Zyklus abgeschlossen. Nächster Zyklus in 60 Sekunden")
    print("-----------------------------------------------------\n")
    time.sleep(60)



