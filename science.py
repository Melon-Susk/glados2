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
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Verfügbare Forschung"]')))
            return True
        except:
            print("Das Bibliotheksmenü konnte nicht geöffnet werden. Die Forschungen werden übersprungen!")
            return False