from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from general import General
import time
import re


class Construction:
    def __init__(self):
        pass
    
    @staticmethod
    def checkForActiveConstruction(driver, waitAmount=2):
        try:
            WebDriverWait(driver, waitAmount).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Alle Gebäude fertigstellen"]')))
            try:
                buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
                buildingContainer.find_element(By.XPATH, './/*[text()="1"]')
            except:
                return 0
            return 1
        except:
            return 2

    @staticmethod
    def getBuildingLevels(driver):
        #Determine Eligible Buildings
        name, points = General.getCastleNameAndPoints(driver)
        if points < 100:
            buildingNamesArray = ["Taverne", "Markt", "Bauernhof", "Holzfäller", "Holzlager", "Steinbruch", "Steinlager", "Erzmine", "Erzlager"]
        else:
            buildingNamesArray = ["Bergfried", "Zeughaus", "Taverne", "Bibliothek", "Wehranlagen", "Markt", 
                  "Bauernhof", "Holzfäller", "Holzlager", "Steinbruch", "Steinlager", "Erzmine", "Erzlager"]

        buildingLevelsDict = {}
        #Limit Scope to Building Menu
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")

        #Cycle through Building scopes to get number
        for i in range(len(buildingNamesArray)):
            try:
                conLevel = buildingContainer.find_element(By.XPATH, f'.//*[text()="{buildingNamesArray[i]}"]/ancestor::node()[1]//*[contains(text(),"Ausbaustufe")]').text
                conLevelNumb = re.findall(r'\d+', conLevel)
            except:
                conLevelNumb = ["1000"]
            buildingLevelsDict[buildingNamesArray[i]] = int(conLevelNumb[0])
        
        return buildingLevelsDict
    
    @staticmethod
    def createBuildOrder(buildingLevelsDict, resourceAmountDict):
        levelDict = buildingLevelsDict
        levelDict["Holzfäller"] = levelDict["Holzfäller"] - 15
        levelDict["Steinbruch"] = levelDict["Steinbruch"] - 15
        levelDict["Erzmine"] = levelDict["Erzmine"] - 15
        levelDict["Holzlager"] = levelDict["Holzlager"] - 5
        levelDict["Steinlager"] = levelDict["Steinlager"] - 5
        levelDict["Erzlager"] = levelDict["Erzlager"] - 5
        if resourceAmountDict["Untertanen"] < 10:
            levelDict["Bauernhof"] = levelDict["Bauernhof"] - 100
        elif resourceAmountDict["Untertanen"] < 100:
            levelDict["Bauernhof"] = levelDict["Bauernhof"] - 10
        if levelDict["Taverne"] < 2:
            levelDict["Taverne"] = levelDict["Taverne"] - 100
        elif levelDict["Taverne"] > 3:
            levelDict["Taverne"] = levelDict["Taverne"] + 10
        if levelDict["Markt"] >= 5:
            levelDict["Markt"] = levelDict["Markt"] + 1000

        sortedBuildingArray = sorted(levelDict, key=levelDict.get)
        return sortedBuildingArray
    
    @staticmethod
    def startConstruction(driver, sortedBuildingArray, conAmount):
        if conAmount < 1:
            return
        
        buildSlots = conAmount
        #Limit Scope to Building Menu
        actions = ActionChains(driver)
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        actions.move_to_element(buildingContainer).click().perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()

        #Cycle through Build Order List
        if buildSlots < 1:
            return
        
        buildingRange = range(len(sortedBuildingArray))
        for i in buildingRange:
            targetBuilding = sortedBuildingArray.pop(i)
            buildButton = buildingContainer.find_element(By.XPATH, f'.//*[text()="{targetBuilding}"]/ancestor::node()[3]//button')
            buildButton.click()
            started = Construction.checkForActiveConstruction(driver, waitAmount=5)
            if started < buildSlots:
                print(f"Gebäudeausbau gestartet für {targetBuilding}")
                buildSlots -= 1
                time.sleep(1)
                break
