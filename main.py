from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from general import General
from construction import Construction
from recruitment import Recruitment
from science import Science
from missions import Missions
from silver import Silver
from util import Util
import time
from datetime import datetime
import pytz
import os

#Global Variables
EMAILS = []
PASSWORD = input("Passwort:")
EMAILAMOUNT = input("Accountanzahl:")
LOGINTIME = input("Login Wartezeit:")
GENERALWAITTIME = input("Allgemeine Wartezeit:")
CASTLENAMES = Util.loadJsonToDict('castlenames.json')
TIMEZONE = pytz.timezone('Europe/Berlin')

#Init Stuff
castlesSilver = {}
sleep = False

for i in range(1, int(EMAILAMOUNT) + 1):
    EMAILS.append(f"unvish112+glados{i}@gmail.com")
print(EMAILS)


#ACCOUNT LOOP
while True:
    sleep = General.sleepTime(TIMEZONE)
    if not sleep:
        i = 0
        startTime = datetime.now(TIMEZONE)
        print(f"------ Zyklus startet um {startTime.strftime('%H:%M')} Uhr ------")
        for i in range(len(EMAILS)):
            #Instantiate Driver
            options = Options()
            options.add_argument("--headless")
            #options.binary_location = r'C:/Users/Lukas.Gosch/AppData/Local/Mozilla Firefox/firefox.exe'
            firefox_binary_path = "/snap/bin/geckodriver"
            service = Service(executable_path=firefox_binary_path)
            #service = Service(executable_path=r'C:/Users/Lukas.Gosch/Documents/Privat/geckodriver.exe')
            driver = webdriver.Firefox(service=service, options=options)
            #driver = webdriver.Firefox(options=options)
            driver.set_window_size(1920, 1080)
            #driver.maximize_window()
            driver.get("https://www.lordsandknights.de")
            print("Webseite geladen...")

            #Login and load World
            try:
                login = General.loginAndWorldSelect(driver, EMAILS[i], PASSWORD, LOGINTIME, GENERALWAITTIME)
                #Kill Pop-Ups
                General.popupKiller(driver)
            except Exception as e:
                print("Fehler beim Login!\n")
                print(e)
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
                try:
                    troopMovement = General.checkForMovement(driver)
                except:
                    troopMovement = True
                Util.reset(driver)

                #Check for Loop Completion
                if (name == CASTLENAMES[EMAILS[i]]) and (loopStart):
                    break
                loopStart = True
                castleSafety += 1

                print(f"\nAusgewählte Burg: {name}\nPunkte: {points}\nHolz: {resourceDict['Holz']}, Stein: {resourceDict['Stein']}, Erz: {resourceDict['Erz']}\nSilber: {resourceDict['Silber']}, Kupfer: {resourceDict['Kupfer']}")


                #Silver
                try:
                    if General.silverMode(TIMEZONE, sleep, points):
                        General.openBuildingMenu(driver)
                        eligibleSilver = Silver.openKeepMenu(driver)
                        if eligibleSilver:
                            Silver.buySilver(driver)
                except Exception as e:
                    print("Fehler bei der Silberbeschaffung!\n")
                    print(e)
                Util.reset(driver)


                #Building Construction
                if General.buildMode(TIMEZONE, sleep, points):
                    try:
                        General.openBuildingMenu(driver)
                        activeConstruction = Construction.checkForActiveConstruction(driver)
                        if not activeConstruction:
                            buildingLevels = Construction.getBuildingLevels(driver)
                            buildOrderArray = Construction.createBuildOrder(buildingLevels, resourceDict)
                            Construction.startConstruction(driver, buildOrderArray)
                        else:
                            print("Es werden noch Gebäude ausgebaut")
                    except Exception as e:
                        print("Fehler beim Gebäudeausbau!\n")
                        print(e)
                    Util.reset(driver)


                #Science
                if General.scienceMode(TIMEZONE, sleep, points):
                    try:
                        General.openBuildingMenu(driver)
                        researchAvailable = Science.openLibraryMenu(driver)
                        if researchAvailable:
                            Science.startResearch(driver)
                    except Exception as e:
                        print("Fehler bei der Forschung!\n")
                        print(e)
                    Util.reset(driver)

                
                #Recruitment
                if General.recruitMode(TIMEZONE, sleep):
                    try:
                        General.openBuildingMenu(driver)
                        eligibleMarketRecruitment = Recruitment.openMarketMenu(driver)
                        if eligibleMarketRecruitment:
                            Recruitment.recruitOchsenkarren(driver)
                    except Exception as e:
                        print("Fehler bei der Rekrutierung von Ochsenkarren!\n")
                        print(e)
                    Util.reset(driver)
                    try:
                        General.openBuildingMenu(driver)
                        eligibleRecruitment = Recruitment.openBarracksMenu(driver)
                        if eligibleRecruitment:
                            amount = Recruitment.getCurrentUnitAmount(driver)
                            recruitmentPlan = Recruitment.determineRecruitmentPlan(points, amount)
                            possibleRecruitments = Recruitment.getPossibleRecruitments(driver)
                            Recruitment.startRecruitment(driver, recruitmentPlan, possibleRecruitments)
                    except Exception as e:
                        print("Fehler bei der Rekrutierung!\n")
                        print(e)
                    Util.reset(driver)
                

                #Missions
                try:
                    General.openBuildingMenu(driver)
                    Missions.openTavernMenu(driver)
                    Missions.startAvailableMissions(driver)
                except Exception as e:
                        print("Fehler bei den Missionen!\n")
                        print(e)
                Util.reset(driver)

                #Get New Resource Amount and write to File
                try:
                    resourceDict = General.getResourceAmount(driver)
                    Util.appendToOverviewJson('resourceOverview.json', EMAILS[i], name, resourceDict)
                except Exception as e:
                    print("Fehler beim Verfassen des Resource Dicts!\n")
                    print(e)

                #Switch to next Castle
                try:
                    time.sleep(1)
                    body = driver.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.ARROW_RIGHT)
                    print("")
                    time.sleep(2)
                    Util.reset(driver)
                except Exception as e:
                    print("Fehler beim Burgenwechsel! Der Account wird übersprungen!\n")
                    print(e)
                    break


            driver.quit()
            time.sleep(3)

    if sleep:
        os.system('clear')
        print("Das Programm befindet sich im Schlafmodus. Neustart um 7 Uhr")
        time.sleep(600)
    else:
        Util.determineCastleAndSilverAmount()
        timeDiff = datetime.now(TIMEZONE) - startTime
        duration = int(timeDiff.total_seconds() / 60)
        print("\n-----------------------------------------------------")
        print("Zyklus abgeschlossen. Nächster Zyklus in 60 Sekunden")
        print(f"Dauer des Zyklus: {duration} Minuten")
        print("-----------------------------------------------------")
        time.sleep(60)
        os.system('clear')



