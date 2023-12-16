from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://www.lordsandknights.com")

#wait until Email Form is loaded
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")))
time.sleep(1)

#get Elements
loginEmail = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[1]/input")
loginPassword = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[1]/div[2]/input")
loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[3]/form/div[3]/button")

#send and submit login Data
loginEmail.send_keys("unvish112+glados@gmail.com")
loginPassword.send_keys("samesame")
loginButton.click()

#Wait for World Selection Screen loading
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Wähle eine Welt"]')))
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

driver.quit()