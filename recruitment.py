from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from construction import Construction
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
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/*[contains(text(),"Alle Rekrutierungen")]')))
            print("Es werden noch Einheiten rekrutiert")
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
    def openMarketMenu(driver):
        marketLevel = Construction.getBuildingLevels(driver)['Markt']
        if marketLevel < 5:
            return False

        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Markt"]').click()
        #Auf aktive Rekrutierungen prüfen
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, './/*[contains(text(),"Alle Rekrutierungen")]')))
            #print("Es sind noch Rekrutierungen im Gange. Die Rekrutierung von Ochsenkarren wird übersprungen")
            return False
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Tauschbare Waren"]')))
            return True
        except:
            print("Das Marktmenü kann nicht geöffnet werden. Die Rekrutierung von Ochsenkarren wird übersprungen")
            return False
    
    @staticmethod
    def recruitOchsenkarren(driver):
        try:
            unitData = driver.find_element(By.XPATH, './/*[contains(text(),"Ochsenkarren")]').text
            unitAmount = re.findall(r'\d+', unitData)
        except:
            print(f"Für die Ochsenkarren konnte die aktuelle Anzahl nicht ermittelt werden! Sie werden nicht rekrutiert")
            return
        
        amountToRecruit = 12 - int(unitAmount[0])
        if amountToRecruit < 1:
            return

        try:
            scrollDiv = driver.find_element(By.XPATH, './/*[contains(text(),"Ochsenkarren")]').find_element(By.XPATH, "ancestor::node()[4]")
            time.sleep(1)
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scrollDiv)
            localScope = driver.find_element(By.XPATH, './/*[contains(text(),"Ochsenkarren")]').find_element(By.XPATH, "ancestor::node()[3]")
            time.sleep(1)
            localScope.find_element(By.TAG_NAME, 'button').click()
        except:
            print("Ochsenkarren können zurzeit nicht rekrutiert werden")
            return
        
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(f"{amountToRecruit}")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-in-button.white.icon-game.icon-recruit')))
            buttonDiv = driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.white.icon-game.icon-recruit')
            buttonDiv.find_element(By.XPATH, "ancestor::node()[1]").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/*[contains(text(),"Alle Rekrutierungen")]')))
            print("Rekrutierung gestartet für Ochsenkarren")
            return
        except Exception as e:
            print("Fehler im Ausbildungsmenü der Ochsenkarren!\n")
            print(e)
            return
        
    @staticmethod
    def getCurrentUnitAmount(driver):
        units = ["Speerträger", "Armbrustschütze", "Panzerreiter", "Schwertkämpfer", "Bogenschütze", "Lanzenreiter"]
        unitAmountDict = {}

        for i in range(len(units)):
            try:
                unitData = driver.find_element(By.XPATH, f'.//*[contains(text(),"{units[i]}")]').text
                unitAmount = re.findall(r'\d+', unitData)
            except:
                print(f"Für {units[i]} konnte die aktuelle Anzahl nicht ermittelt werden! Die Klasse wird nicht rekrutiert")
                unitAmount = 10000
            unitAmountDict[units[i]] = int(unitAmount[0])
        
        return unitAmountDict
        
    @staticmethod
    def determineRecruitmentPlan(castleLevel, unitAmountDict):
        if castleLevel < 80:
            return {"Speerträger": 15, "Armbrustschütze": 0, "Panzerreiter": 0, "Schwertkämpfer": 0, "Bogenschütze": 15, "Lanzenreiter": 0}
        
        units = ["Speerträger", "Armbrustschütze", "Panzerreiter", "Schwertkämpfer", "Bogenschütze", "Lanzenreiter"]
        recruitmentDict = {}
        if castleLevel < 140:
            desiredAmount = [100,0,20,40,50,0]
        elif castleLevel < 200:
            desiredAmount = [100,0,50,100,100,0]
        elif castleLevel < 240:
            desiredAmount = [300,100,100,200,200,0]
        elif castleLevel < 300:
            desiredAmount = [600,600,600,325,425,425]

        for i in range(len(units)):
            amountToRecruit = desiredAmount[i] - unitAmountDict[units[i]]
            if amountToRecruit < 0:
                amountToRecruit = 0

            recruitmentDict[units[i]] = amountToRecruit
        
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

        