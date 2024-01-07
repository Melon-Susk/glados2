from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from recruitment import Recruitment
import time

class Silver:
    def __init__(self):
        pass

    @staticmethod
    def openKeepMenu(driver):
        buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
        buildingContainer.find_element(By.XPATH, './/*[text()="Bergfried"]').click()
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

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Aktuelle Lagermenge des Ziels"]')))
        time.sleep(1)

        #Ochsenkarren auswählen
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-unit.icon-unit-10002')))
        except:
            print("Es sind noch keine Ochsenkarren in der Burg vorhanden. Es wird kein Silber eingetauscht!")
            return
        
        cartLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon-unit.icon-unit-10002').find_element(By.XPATH, "ancestor::node()[7]")
        scrollLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon-unit.icon-unit-10002').find_element(By.XPATH, "ancestor::node()[8]")
        cartLevel.find_element(By.TAG_NAME, 'input').send_keys("12")
        time.sleep(1)

        #Holz, Stein und Erz auswählen
        woodLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--1').find_element(By.XPATH, "ancestor::node()[7]")
        woodLevel.find_element(By.TAG_NAME, 'input').send_keys("10000")
        time.sleep(0.5)
        stoneLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--2').find_element(By.XPATH, "ancestor::node()[7]")
        stoneLevel.find_element(By.TAG_NAME, 'input').send_keys("10000")
        time.sleep(0.5)
        oreLevel = driver.find_element(By.CSS_SELECTOR, '.icon.icon.icon-resource.icon-resource--3').find_element(By.XPATH, "ancestor::node()[7]")
        oreLevel.find_element(By.TAG_NAME, 'input').send_keys("10000")
        time.sleep(0.5)

        #driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollLevel)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Silber eintauschen"]')))
        #driver.find_element(By.XPATH, '//*[text()="Silber eintauschen"]').click()
        print("SILBERBESCHAFFUNG GESTARTET")
        time.sleep(10)

