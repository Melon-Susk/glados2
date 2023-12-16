from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import re

class Silver:
    def __init__(self):
        pass

    @staticmethod
    def openKeepMenu(driver):
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Bergfried"]').click()
        #Auf aktive Silbertransporte prüfen
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Alle Rekrutierungen fertigstellen"]')))
            print("Es wird noch Silber transportiert")
            return False
        except:
            pass
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Tauschbare Waren"]')))
            return True
        except:
            print("Das Bergfriedmenü konnte nicht geöffnet werden. Der Silberkauf wird übersprungen!")
            return False
    
    @staticmethod
    def buySilver(driver):
        buyLevel = driver.find_element(By.XPATH, '//*[text()="Tauschbare Waren"]/ancestor::node()[1]')
        buyLevel.find_element(By.XPATH, './/*[text()="Silber"]').click()

        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Aktuelle Lagermenge des Ziels"]')))
        time.sleep(1)

        #Karren auswählen
        cartLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon-unit.icon-unit-10001').find_element(By.XPATH, "ancestor::node()[6]")
        scrollLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon-unit.icon-unit-10001').find_element(By.XPATH, "ancestor::node()[7]")
        cartLevel.find_element(By.CSS_SELECTOR, '.button.button--default.button-with-icon.widget-seek-bar-header__button.multiple').click()
        time.sleep(1)

        #Holz, Stein und Erz auswählen
        woodLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--1').find_element(By.XPATH, "ancestor::node()[6]")
        woodLevel.find_element(By.CSS_SELECTOR, '.button.button--default.button-with-icon.widget-seek-bar-header__button.multiple').click()
        time.sleep(0.5)
        stoneLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--2').find_element(By.XPATH, "ancestor::node()[6]")
        stoneLevel.find_element(By.CSS_SELECTOR, '.button.button--default.button-with-icon.widget-seek-bar-header__button.multiple').click()
        time.sleep(0.5)
        oreLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--3').find_element(By.XPATH, "ancestor::node()[6]")
        oreLevel.find_element(By.CSS_SELECTOR, '.button.button--default.button-with-icon.widget-seek-bar-header__button.multiple').click()
        time.sleep(0.5)

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollLevel)
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Silber eintauschen"]')))
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[text()="Silber eintauschen"]').click()
        time.sleep(5)

        return datetime.now()

