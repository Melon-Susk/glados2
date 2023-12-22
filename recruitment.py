from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class Recruitment:
    def __init__(self):
        pass

    @staticmethod
    def openBarracksMenu(driver):
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Zeughaus"]').click()
        #Auf aktive Rekrutierungen prüfen
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Alle Rekrutierungen fertigstellen"]')))
            print("Es sind noch Rekrutierungen im Gange. Die Rekrutierung wird übersprungen")
            return False
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Mögliche Einheiten"]')))
            return True
        except:
            print("Das Zeughausmenü kann nicht geöffnet werden. Die Rekrutierungsfunktion wird übersprungen")
            return False
        
    @staticmethod
    def getCurrentUnitAmount(driver):
        units = ["Speerträger", "Armbrustschütze", "Panzerreiter", "Schwertkämpfer", "Bogenschütze", "Lanzenreiter"]
        unitAmountDict = {}

        for i in range(len(units)):
            unitData = driver.find_element(By.XPATH, f'.//*[contains(text(),"{units[i]}")]').text
            unitAmount = re.findall(r'\d+', unitData)
            unitAmountDict[units[i]] = int(unitAmount[0])
        
        return unitAmountDict
        
    @staticmethod
    def determineRecruitmentPlan(castleLevel, unitAmountDict):
        if castleLevel < 80:
            return {"Speerträger": 5, "Armbrustschütze": 0, "Panzerreiter": 0, "Schwertkämpfer": 0, "Bogenschütze": 0, "Lanzenreiter": 0}
        
        units = ["Speerträger", "Armbrustschütze", "Panzerreiter", "Schwertkämpfer", "Bogenschütze", "Lanzenreiter"]
        recruitmentDict = {}
        if castleLevel < 140:
            desiredAmount = [50,0,0,15,20,0]
        elif castleLevel < 200:
            desiredAmount = [100,50,20,30,30,0]
        elif castleLevel < 240:
            desiredAmount = [300,300,100,50,50,20]
        elif castleLevel < 300:
            desiredAmount = [600,600,600,325,425,425]

        for i in range(len(units)):
            recruitmentDict[units[i]] = desiredAmount[i] - unitAmountDict[units[i]]
        
        return recruitmentDict
    
    @staticmethod
    def getPossibleRecruitments(driver):
        units = ["Speerträger", "Armbrustschütze", "Panzerreiter", "Schwertkämpfer", "Bogenschütze", "Lanzenreiter"]
        possibleUnits = []

        driver.find_element(By.XPATH, '//*[text()="Mögliche Einheiten"]').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Defensive Einheiten"]')))

        unitScope = driver.find_element(By.XPATH, '//*[text()="Defensive Einheiten"]').find_element(By.XPATH, "ancestor::node()[1]")

        for i in range(len(units)):
            try:
                unitScope.find_element(By.XPATH, f'.//*[contains(text(),"{units[i]}")]')
                possibleUnits.append(units[i])
            except:
                continue
        
        return possibleUnits

    @staticmethod
    def startRecruitment(driver, recruitmentDict, possibleUnits):
        rdict = recruitmentDict
        pUnits = possibleUnits

        if len(pUnits) < 1:
            print("Es können zurzeit keine Einheiten ausgebildet werden")
            return

        for i in range(len(pUnits)):
            if rdict[pUnits[i]] > 0:
                localScope = driver.find_element(By.XPATH, f'.//*[contains(text(),"{pUnits[i]}")]').find_element(By.XPATH, "ancestor::node()[3]")
                localScope.find_element(By.TAG_NAME, 'button').click()

                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(f"{rdict[pUnits[i]]}")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-in-button.white.icon-game.icon-recruit')))
                buttonDiv = driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.white.icon-game.icon-recruit')
                buttonDiv.find_element(By.XPATH, "ancestor::node()[1]").click()
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/*[contains(text(),"Alle Rekrutierungen")]')))
                    print(f"Rekrutierung gestartet für {pUnits[i]}")
                    return
                except:
                    print(f"{pUnits[i]} konnte nicht ausgebildet werden!")
                    continue

        