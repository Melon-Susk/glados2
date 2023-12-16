from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Science:
    def __init__(self):
        pass

    @staticmethod
    def openLibraryMenu(driver):
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Bibliothek"]').click()
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Alle Forschungen fertigstellen"]')))
            print("Es gibt noch aktive Forschungen")
            return False
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Mögliche Forschungen"]')))
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//*[text()="Mögliche Forschungen"]').click()
            time.sleep(1)
            return True
        except:
            print("Das Bibliotheksmenü konnte nicht geöffnet werden. Die Forschungen werden übersprungen!")
            return False
        
    @staticmethod
    def startResearch(driver):
        projects = driver.find_element(By.XPATH, '//*[text()="Verfügbare Forschung"]/ancestor::node()[1]')
        buttons = projects.find_elements(By.TAG_NAME, 'button')

        #Press Start Research Buttons
        for i in range(len(buttons)):
            buttons[i].click()
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Alle Forschungen fertigstellen"]')))
                print("Forschung gestartet")
                return
            except:
                pass