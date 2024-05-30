from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from util import Util
from general import General
import time
import json

MAILFRONT = 'pauljay1245+schradin'
MAILBACK = '@outlook.de'
PASSWORD = 'samesame'
REGIONMAP = True

#CREATE ACCOUNT LOOP
while True:
    #Instantiate Driver
    #options = Options()
    #options.binary_location = r'C:/Users/Lukas.Gosch/AppData/Local/Mozilla Firefox/firefox.exe'
    #service = Service(executable_path=r'C:/Users/Lukas.Gosch/Documents/Privat/geckodriver.exe')
    #driver = webdriver.Firefox(service=service, options=options)

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.lordsandknights.com")

    #Login and load World
    #wait until Email Form is loaded
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
    time.sleep(float(0.5))

    #Change language
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div")))
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div").click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="DE"]')))
    driver.find_element(By.XPATH, '//*[text()="DE"]').click()
    time.sleep(float(1))

    #Accept Terms
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/div[1]/form/div/div[1]/div[2]/div[2]/label').click()
    driver.find_element(By.CSS_SELECTOR, 'button.button-direct-play').click()

    #Wait until Tutorial Load
    time.sleep(15)

    """
    driver.refresh()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button-direct-play'))).click()

    #Wait for World Selection Screen loading
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Wähle eine Welt"]')))
    time.sleep(float(5))
    #Click on latest played World
    driver.find_element(By.XPATH, '//*[text()="Germanien X (DE) (empfohlen)"]').click()
    #Wait for World to load
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Profil"]')))
    time.sleep(int(10))
    """

    #Kill Pop-Ups
    General.popupKiller(driver)

    #Kill Tutorial
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-tutorial.icon-close-button'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Ja"]'))).click()

    #Kill Pop-Ups again lmao
    General.popupKiller(driver)

    #Validate Successfull Tutorial removal
    profileMenu = driver.find_element(By.XPATH, '//*[text()="Profil"]')
    profileMenu.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Spielerübersicht"]')))
    profileMenu.click()
    print("Welt erfolgreich geladen")
    
    #Karte öffnen und auf Befehl warten
    if REGIONMAP:
        driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.icon-game.white.icon-region').click()
    else:
        driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.icon-game.white.icon-button-political-map').click()
    
    createAcc = input('Fortfahren? (y/n)')

    if createAcc == 'q':
        driver.quit()
        break
    elif createAcc != 'y':
        driver.quit()
        time.sleep(30)
        continue
    
    #Nötige Dateien laden
    activeAccounts = Util.loadJsonToDict('castlenames.json')
    presetArray = Util.loadJsonToDict('accountNamesPreset.json')

    mailNumber = len(activeAccounts)
    fullMail = MAILFRONT + str(mailNumber) + MAILBACK
    print(fullMail)

    #Daten eintragen
    driver.find_element(By.XPATH, '//*[text()="Registrierung"]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[text()="E-Mail"]/ancestor::node()[2]//div[2]/div/input').send_keys(fullMail)
    driver.find_element(By.XPATH, '//*[text()="Kennwort"]/ancestor::node()[2]//div[2]/div/input').send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//*[text()="Passwort bestätigen"]/ancestor::node()[2]//div[2]/div/input').send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//*[text()="Registrieren"]').click()

    #Zur Burgansicht und Castlenames aktualisieren
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Profil"]')))
    activeAccounts[fullMail] = presetArray[mailNumber]
    with open('castlenames.json', 'w',) as f:
        json.dump(activeAccounts, f)

    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-in-button.icon-game.white.icon-bar-castle'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.icon.icon-in-button.icon-game.white.icon-build')))

    #Burgnamen festlegen
    General.openBuildingMenu(driver)
    buildingContainer = driver.find_element(By.XPATH, '//*[text()="Hauptgebäude"]').find_element(By.XPATH, "ancestor::node()[2]")
    buildingContainer.find_element(By.XPATH, './/*[text()="Bergfried"]').click()
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Tauschbare Waren"]')))
        driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.controls.menu-bar-edit').click()
        driver.find_element(By.XPATH, '//*[text()="Habitatsname"]/ancestor::node()[2]//div[2]/div/div[1]/input').clear()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[text()="Habitatsname"]/ancestor::node()[2]//div[2]/div/div[1]/input').send_keys(presetArray[mailNumber])
        driver.find_element(By.CSS_SELECTOR, '.icon.icon-in-button.controls.menu-accept').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{presetArray[mailNumber]}"]')))
    except:
        input("Das Bergfriedmenü konnte nicht geöffnet werden. Der Name muss manuell eingetragen werden!")
    
    driver.quit()
    time.sleep(30)
