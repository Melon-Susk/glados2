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
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Verfügbare Missionen"]')))
            return True
        except:
            print("Das Tavernenmenü konnte nicht geöffnet werden. Die Forschungen werden übersprungen!")
            return False
