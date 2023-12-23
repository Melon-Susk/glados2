from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
            return True
        except:
            return False

    
    @staticmethod
    def getBuildingLevels(driver):
        #Determine Eligible Buildings
        name, points = General.getCastleNameAndPoints(driver)
        if points < 100:
            buildingNamesArray = ["Taverne", "Bauernhof", "Holzfäller", "Holzlager", "Steinbruch", "Steinlager", "Erzmine", "Erzlager"]
        else:
            buildingNamesArray = ["Bergfried", "Zeughaus", "Taverne", "Bibliothek", "Wehranlagen", "Markt", 
                  "Bauernhof", "Holzfäller", "Holzlager", "Steinbruch", "Steinlager", "Erzmine", "Erzlager"]

        buildingLevelsDict = {}
        #Limit Scope to Building Menu
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")

        #Cycle through Building scopes to get number
        for i in range(len(buildingNamesArray)):
            conLevel = buildingContainer.find_element(By.XPATH, f'.//*[text()="{buildingNamesArray[i]}"]/ancestor::node()[1]//*[contains(text(),"Ausbaustufe")]').text
            conLevelNumb = re.findall(r'\d+', conLevel)
            buildingLevelsDict[buildingNamesArray[i]] = int(conLevelNumb[0])
        
        return buildingLevelsDict
    
    @staticmethod
    def createBuildOrder(buildingLevelsDict, resourceAmountDict):
        levelDict = buildingLevelsDict
        levelDict["Holzfäller"] = levelDict["Holzfäller"] - 15
        levelDict["Steinbruch"] = levelDict["Steinbruch"] - 15
        levelDict["Erzmine"] = levelDict["Erzmine"] - 10
        if resourceAmountDict["Untertanen"] < 10:
            levelDict["Bauernhof"] = levelDict["Bauernhof"] - 100
        elif resourceAmountDict["Untertanen"] < 100:
            levelDict["Bauernhof"] = levelDict["Bauernhof"] - 10
        if levelDict["Taverne"] < 2:
            levelDict["Taverne"] = levelDict["Taverne"] - 100
        elif levelDict["Taverne"] < 4:
            levelDict["Taverne"] = levelDict["Taverne"] - 5

        sortedBuildingArray = sorted(levelDict, key=levelDict.get)
        return sortedBuildingArray
    
    @staticmethod
    def startConstruction(driver, sortedBuildingArray):
        #Limit Scope to Building Menu
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")

        #Cycle through Build Order List
        for i in range(len(sortedBuildingArray)):
            buildButton = buildingContainer.find_element(By.XPATH, f'.//*[text()="{sortedBuildingArray[i]}"]/ancestor::node()[3]//button')
            buildButton.click()
            started = Construction.checkForActiveConstruction(driver, waitAmount=5)
            if started:
                print(f"Gebäudeausbau gestartet für {sortedBuildingArray[i]}")
                time.sleep(1)
                break
