from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import json
import pandas as pd


class Util:
    def __init__(self):
        pass
    
    @staticmethod
    def reset(driver):
        for i in range(5):
            try:
                profileMenu = driver.find_element(By.XPATH, '//*[text()="Profil"]')
                profileMenu.click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Spielerübersicht"]')))
                profileMenu.click()
                break
            except:
                print(f"Reset fail {i+1}")
                time.sleep(float(i))
                continue
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Spielerübersicht"]')))
            return False
        except:
            return True
        
    @staticmethod
    def checkNewDay(lastCheck):
        jetzt = datetime.now()

        if jetzt.date() > lastCheck.date():
            ist_neuer_tag = True
        else:
            ist_neuer_tag = False

        return ist_neuer_tag
    
    @staticmethod
    def loadJsonToDict(dateipfad):
        try:
            with open(dateipfad, 'r', encoding='utf-8') as datei:
                daten = json.load(datei)
                return daten
        except FileNotFoundError:
            print("Die Datei wurde nicht gefunden:", dateipfad)
            return None
        except json.JSONDecodeError:
            print("Fehler beim Parsen der JSON-Datei:", dateipfad)
            return None
    
    @staticmethod
    def appendToOverviewJson(dateipfad, accountName, castleName, resourceDict):
        with open(dateipfad, 'r', encoding='utf-8') as file:
            file_content = file.read()
            if not file_content:
                daten = {}
            else:
                daten = json.loads(file_content)
        
        if accountName not in daten:
            daten[accountName] = {}

        daten[accountName][castleName] = resourceDict

        with open(dateipfad, 'w', encoding='utf-8') as file:
            json.dump(daten, file)
    
    @staticmethod
    def determineCastleAndSilverAmount():
        # JSON-Daten laden
        with open('resourceOverview.json', 'r') as file:
            data = json.load(file)

        # Liste für die Ergebnisse
        ergebnisse = []

        # Verarbeite jeden Top-Level-Schlüssel
        for email, burgen in data.items():
            anzahl_burgen = len(burgen)
            summe_silber = sum(burg.get("Silber", 0) for burg in burgen.values())
        
            # Benötigtes Silber berechnen
            ben_silber = anzahl_burgen * 1000 - 1000
            if ben_silber <= summe_silber:
                ben_silber = "SILBER AUSREICHEND"
            else:
                ben_silber = ben_silber - summe_silber

            # Ergebnisse hinzufügen
            ergebnisse.append({"E-Mail": email, "Anzahl Burgen": anzahl_burgen, "Summe Silber": summe_silber, "Noch benötigt": ben_silber})

        # Erstelle einen DataFrame aus den Ergebnissen
        df = pd.DataFrame(ergebnisse)
        df.to_excel('silverOverview.xlsx', index=False)
    
    @staticmethod
    def isNight():
        jetzt = datetime.now()
        if jetzt.hour > 23:
            return True
        elif jetzt.hour < 5:
            return True
        return False

