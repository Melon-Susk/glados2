from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class Missions:
    def __init__(self):
        pass

    @staticmethod
    def openTavernMenu(driver):
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Taverne"]').click()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Mögliche Missionen"]')))
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//*[text()="Mögliche Missionen"]').click()
            time.sleep(1)
            return True
        except:
            print("Das Tavernenmenü konnte nicht geöffnet werden. Die Missionen werden übersprungen!")
            return False
    
    @staticmethod
    def startAvailableMissions(driver):
        try:
            missionsContainer = driver.find_element(By.XPATH, '//*[text()="Zur Einzelauswahl wechseln"]').find_element(By.XPATH, "ancestor::node()[4]")
        except:
            driver.find_element(By.XPATH, '//*[text()="Zur Gruppenauswahl wechseln"]').click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Zur Einzelauswahl wechseln"]')))
            missionsContainer = driver.find_element(By.XPATH, '//*[text()="Zur Einzelauswahl wechseln"]').find_element(By.XPATH, "ancestor::node()[4]")
        
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.menu-selectable')))
        except:
            print("Es sind keine Missionen verfügbar")
            return True
        
        checkboxes = missionsContainer.find_elements(By.CSS_SELECTOR, '.icon.menu-selectable')

        if len(checkboxes) == 0:
            return True

        for i in range(len(checkboxes)):
            checkboxes[i].click()
            time.sleep(0.5)
        
        missionsContainer.find_element(By.TAG_NAME, 'button').click()