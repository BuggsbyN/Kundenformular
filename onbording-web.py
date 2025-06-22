import streamlit as st

#Kundendaten speichern, abrufen , bearbeiten und löschen

import pandas as pd
import os


import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.title('Fitness-Onboarding')
#Persöhnliche Fragen
name = st.text_input('Gib deinen Namen ein')
alter= st.number_input('Gib dein Alter ein', min_value=15, max_value=100, step=1)
geschlecht = st.selectbox('Gib dein Geschlecht ein',["Mann","Frau","Anderes"])


#Fitness Hintergrund
Trainingsziel = st.text_input("zB. Muskelaufbau, Abnehmen, Ausdauer verbessern")
Motivation = st.text_input("Was ist deine Motivation")
Trainingserfahrung = st.selectbox("Gibt deine Trainingserfahung ein",["Anfänger", "Fortgeschritten","Profi"])
Sportarten = st.text_input("Welchen Sport hast du bis jetzt ausgeübt")

#Gesundheit und Einschränkungen
Verletzungen = st.text_input("Verletzungen oder Erkrankugen von denen ich wissen muss ?")

#Lifestyle & Alltag
Beruf = st.text_input("Schichtarbeit, Bürojob, viel draußen")
schlaf = st.number_input("wie viel schläfst du normalerweise ?", min_value=0.0, max_value=24.0, step=0.5)

#Ernährung
Ernährung = st.selectbox("Wie sieht es mit deiner Ernährung aus?", ["Normal", "Vegetarisch", "Vegan"])
Besonderes = st.text_input("hast du unverträglichkeiten ?")

#Ziele & Erwartungen
Ziele = st.text_input("was für Ziele hast du genau ?")
Woche = st.number_input("wie viele Tage kannst du trainieren in der Woche ?", min_value=1, max_value=7, step=1)
Trainer = st.text_input("Was erwartest du von mir ?")

#Sonstiges
Zugang = st.selectbox("Hast du Zugang zu einem Fitnessstudio ?",["Ja","Nein"])
Home = st.selectbox("Hast du eigenes Sportequipment zu Hause ?",["Ja","Nein"])

#Zusammenfassung der Daten das der Kunde seine gesamten daten noch einmal sieht und prüfen kann
if st.button("Zusammenfassung anzeigen"):
    st.subheader("Dein Fitnessprofil")
    st.write(f" Name:{name}")
    st.write(f" Alter: {alter} | Geschlecht: {geschlecht}")
    st.write(f" Trainingsziel: {Trainingsziel}")
    st.write(f" Motivation: {Motivation}")
    st.write(f" Trainingserfahrung: {Trainingserfahrung}")
    st.write(f"️ Sportarten bisher: {Sportarten}")
    st.write(f"️ Verletzungen/Krankheiten: {Verletzungen}")
    st.write(f" Beruf: {Beruf} |  Schlaf: {schlaf} Stunden")
    st.write(f" Ernährung: {Ernährung} | Besonderes: {Besonderes}")
    st.write(f" Ziele: {Ziele}")
    st.write(f" Trainingstage/Woche: {Woche}")
    st.write(f" Erwartung an Trainer: {Trainer}")
    st.write(f" Fitnessstudio-Zugang: {Zugang}")
    st.write(f" Heim-Equipment: {Home}")

#Kundendaten speichern
if st.button("Kundenprofil speichern"):
    neuer_Kunde = {
        "Name": name,
        "Alter": alter,
        "Geschlecht": geschlecht,
        "Trainingsziel": Trainingsziel,
        "Motivation": Motivation,
        "Trainingserfahrung": Trainingserfahrung,
        "Sportarten": Sportarten,
        "Verletzungen": Verletzungen,
        "Beruf": Beruf,
        "schlaf": schlaf,
        "Ernährung": Ernährung,
        "Ziele": Ziele,
        "Trainingstage/Woche": Woche,
        "Erwartung an Trainer": Trainer,
        "Fitnessstudio-Zugang": Zugang,
        "Heim-Equipment": Home
    }

    # CSV lokal speichern
    if os.path.exists("kunden.csv"):
        df = pd.read_csv("kunden.csv")
        df = pd.concat([df, pd.DataFrame([neuer_Kunde])], ignore_index=True)
    else:
        df = pd.DataFrame([neuer_Kunde])

    df.to_csv("kunden.csv", index=False)
    st.success("Kunde wurde lokal gespeichert")

    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials
    import gspread
    import streamlit as st


    def init_google_sheet():
        # Credentials & Service einrichten
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        spreadsheet_id = "1PDMFFM_S5k4lKzpsf6lk0AjqTwC2623TpC703jGHXOM"

        # Header definieren
        header = ["Name", "Alter", "Geschlecht", "Trainingsziel", "Motivation", "Trainingserfahrung",
                  "Sportarten", "Verletzungen", "Beruf", "Schlaf", "Ernährung", "Ziele",
                  "Trainingstage/Woche", "Erwartung an Trainer", "Fitnessstudio-Zugang", "Heim-Equipment"]

        # Kopfzeile schreiben
        values = [header]
        body = {'values': values}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="A1:P1",
            valueInputOption="RAW",
            body=body
        ).execute()

        # Formatierung und Spaltenbreite per batchUpdate
        requests = [
            # Kopfzeile fetten, zentrieren, grau hinterlegen
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(header)
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
                            "horizontalAlignment": "CENTER",
                            "textFormat": {"bold": True}
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                }
            },
            # Spaltenbreiten auf 160 Pixel
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": len(header)
                    },
                    "properties": {
                        "pixelSize": 160
                    },
                    "fields": "pixelSize"
                }
            },
            # Filter auf Kopfzeile setzen
            {
                "setBasicFilter": {
                    "filter": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": len(header)
                        }
                    }
                }
            }
        ]

        body = {"requests": requests}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()


    # Beispiel Nutzung in deinem Code:

    # Google Sheets Upload vorbereiten
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1PDMFFM_S5k4lKzpsf6lk0AjqTwC2623TpC703jGHXOM").sheet1

    # Einmalig die Tabelle initialisieren (nur einmal vor dem ersten Schreiben)
    init_google_sheet()

    # Dann neue Kundendaten anhängen
    sheet.append_row(list(neuer_Kunde.values()))
    st.success("Kunde wurde in Google Sheets eingetragen!")

from fpdf import FPDF
import re
def erstelle_pdf(Kundendaten):
    pdf = FPDF() #erstellen der neuen PDF
    pdf.add_page() #Seite hinzufügen
    pdf.set_font("Arial", size=10) #Schriftart und die Größe

    pdf.cell(200,10,txt=Kundendaten, ln=True, align="C") # erstellt die Seite in der gewünschten breite,höhe und zentriert
    pdf.ln(10) # fügt einen Zeilenumbruch hinzu und sorgt für abstand


    for key, value in Kundendaten.items(): #schleife für das dictionary fügt zb key= name mit dem Wert=Max zsm.
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="C")

    # Kundennamen für den Dateinamen verwenden
    name = Kundendaten.get("name", "Unbekannt")

    #Leert zeichen, die im Dateinamen Probleme machen könnten
    name_clean = re.sub(r"[^a-aA-z0-9_äöüÄÖÜß]",name)
    name_clean = name_clean.replace(" ","_") #Leerzeichen durch unterschriche ersetzten

    #Dateinamen im Namen
    dateiname = f"{name_clean}_Profil.pdf"

    pdf.output(dateiname)# speichert die aktuellen Daten unter dem Namen >Kundenprofil<







