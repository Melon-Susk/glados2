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
    def loginAndWorldSelect(driver, email, password):
        #wait until Email Form is loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
        time.sleep(1)

        #get Elements
        loginEmail = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")
        loginPassword = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[2]/input")
        loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[3]/button")

        #send and submit login Data
        loginEmail.send_keys(email)
        loginPassword.send_keys(password)
        loginButton.click()

        #Wait for World Selection Screen loading
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Wähle eine Welt"]')))
        time.sleep(1)
        #Click on latest played World
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]").click()
        #Wait for World to load
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Profil"]')))
        time.sleep(10)

        #Validate Successfull World Loading
        profileMenu = driver.find_element(By.XPATH, '//*[text()="Profil"]')
        profileMenu.click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Spielerübersicht"]')))
        profileMenu.click()

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
        

