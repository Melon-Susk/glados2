from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re


class General:
    def __init__(self):
        pass

    @staticmethod
    def loginAndWorldSelect(driver, email, password, loginWaitTime, generalWaitTime=3):
        #wait until Email Form is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
        time.sleep(float(generalWaitTime))

        #Change language
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div")))
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="DE"]')))
        driver.find_element(By.XPATH, '//*[text()="DE"]').click()
        time.sleep(float(generalWaitTime))

        #get Elements
        loginEmail = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")
        print("Email Element gefunden...")
        loginPassword = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[2]/input")
        print("Passwort Element gefunden...")
        loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[3]/button")
        print("Button Element gefunden...")

        #send and submit login Data
        loginEmail.send_keys(email)
        loginPassword.send_keys(password)
        loginButton.click()
        print("Button geklickt...")

        #Wait for World Selection Screen loading
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Wähle eine Welt"]')))
        print("Weltauswahl geladen...")
        time.sleep(float(generalWaitTime))
        #Click on latest played World
        driver.find_element(By.XPATH, '//*[text()="Deutsch 26 (empfohlen)"]').click()
        print("Auf Welt geklickt...")
        #Wait for World to load
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Profil"]')))
        print("Profilelement gefunden...")
        time.sleep(int(loginWaitTime))

        #Validate Successfull World Loading
        profileMenu = driver.find_element(By.XPATH, '//*[text()="Profil"]')
        profileMenu.click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Spielerübersicht"]')))
        profileMenu.click()
        time.sleep(1)

        return True
    
    @staticmethod
    def getResourceAmount(driver):
        resources = ["Holz", "Stein", "Erz", "Untertanen", "Kupfer", "Silber"]
        resourceAmountDict = {}

        for i in range(len(resources)):
            scope = driver.find_element(By.XPATH, f"//div[@title='{resources[i]}']")
            amount = int(scope.find_element(By.XPATH, './/div[2]/div[1]').text)
            resourceAmountDict[resources[i]] = amount

        return resourceAmountDict

    @staticmethod
    def getCastleNameAndPoints(driver):
        name = driver.find_element(By.CSS_SELECTOR, '.habitat-chooser--title.text-name-with-emo-icons').find_element(By.XPATH, './span[1]').text
        points = driver.find_element(By.CSS_SELECTOR, '.habitat-chooser--title.text-name-with-emo-icons').find_element(By.XPATH, './span[2]').text
        points = re.findall(r'\d+', points)
        points = int(points[0])
        return name, points
    
    @staticmethod
    def openBuildingMenu(driver):
        profileMenu = driver.find_element(By.XPATH, '//*[text()="Gebäude"]')
        profileMenu.click()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Bauliste"]')))
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def selectMainCastle(driver, castleName):
        for i in range(1000):
            currentName, points = General.getCastleNameAndPoints(driver)
            if currentName == castleName:
                time.sleep(1)
                return

            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)
    
    @staticmethod
    def popupKiller(driver):
        for i in range(10):
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.event-pop-up-button.ButtonRedAccept')))
                driver.find_element(By.CSS_SELECTOR, '.event-pop-up-button.ButtonRedAccept').click()
                print("Pop-Up gefunden und beseitigt!")
                time.sleep(3)
            except:
                break
        

