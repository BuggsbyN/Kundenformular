import streamlit as st
import pandas as pd
import os
import sys
import json

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread

st.title("Bereit für Veränderung? Erzähl mir, wer du bist!")

# Persönliche Fragen
name = st.text_input('Gib deinen Namen ein')
alter = st.number_input('Gib dein Alter ein', min_value=15, max_value=100, step=1)
geschlecht = st.selectbox('Gib dein Geschlecht ein?', ["Mann", "Frau", "Anderes"])

# Fitness Hintergrund
Trainingsschwerpunkt = st.multiselect(
    "Was sind deine Trainingsschwerpunkte?",
    options=[
        "Kraftaufbau",
        "Ausdauer verbessern",
        "Beweglichkeit erhöhen",
        "Gewicht reduzieren",
        "Muskeldefinition",
        "Schmerzfreiheit / Reha",
        "Allgemeine Fitness erhalten oder erhöhen"
    ])
Motivation = st.text_input("Was fällt dir aktuell schwer, wenn es um Fitness oder gesunden Alltag geht?",
                          help="Zum Beispiel:Dranbleiben,Ernährung,Zeit finden oder Schmerzen")
Trainingserfahrung = st.selectbox("Gib deine Trainingserfahrung ein", ["Anfänger", "Fortgeschritten", "Profi"])
Sportarten = st.text_input("Welchen Sport hast du bis jetzt ausgeübt?")

# Gesundheit und Einschränkungen
Verletzungen = st.text_input("Verletzungen oder Erkrankungen, von denen ich wissen muss?")

# Lifestyle & Alltag
Beruf = st.text_input("Was machst du beruflich?",
                     help="z.B. Beruf oder Tätigkeit angeben?")
schlaf = st.number_input("Wie viel schläfst du normalerweise?", min_value=0.0, max_value=24.0, step=0.5)

# Ernährung
Ernährung = st.selectbox("Wie sieht es mit deiner Ernährung aus?", ["Normal", "Vegetarisch", "Vegan"])
Besonderes = st.text_input("Hast du Unverträglichkeiten?")

# Ziele & Erwartungen
Ziele = st.text_input("Hast du ein konkretes Ziel oder Wunsch-Ergebnis?",)
Woche = st.number_input("Wie viele Tage kannst du trainieren in der Woche?", min_value=1, max_value=7, step=1)
Trainer = st.text_input("Was erwartest du von mir?")

# Sonstiges
Zugang = st.selectbox("Hast du Zugang zu einem Fitnessstudio?", ["Ja", "Nein"])
Home = st.selectbox("Hast du eigenes Sportequipment zu Hause?", ["Ja", "Nein"])

#email abfrage:
Email = st.text_input("Wie lautet deine Email-Adresse?")

# Zusammenfassung der Daten anzeigen
if st.button("Zusammenfassung anzeigen"):
    st.subheader("Dein Fitnessprofil")
    st.write(f"Name: {name}")
    st.write(f"Alter: {alter} | Geschlecht: {geschlecht}")
    st.write(f"Trainingsschwerpunkt: {Trainingsschwerpunkt}")
    st.write(f"Motivation: {Motivation}")
    st.write(f"Trainingserfahrung: {Trainingserfahrung}")
    st.write(f"Sportarten bisher: {Sportarten}")
    st.write(f"Verletzungen/Krankheiten: {Verletzungen}")
    st.write(f"Beruf: {Beruf} | Schlaf: {schlaf} Stunden")
    st.write(f"Ernährung: {Ernährung} | Besonderes: {Besonderes}")
    st.write(f"Ziele: {Ziele}")
    st.write(f"Trainingstage/Woche: {Woche}")
    st.write(f"Erwartung an Trainer: {Trainer}")
    st.write(f"Fitnessstudio-Zugang: {Zugang}")
    st.write(f"Heim-Equipment: {Home}")
    st.write(f"Email: {Email}")

# Funktion: Google Sheets initialisieren
def init_google_sheet():
    service_account_info = json.loads(st.secrets["google"]["service_account_json"])
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = "1Kj97Lq4DKMKDUIZK-W9wLUxFPfMsMMhoMBDTvBbfJJY"
    return service, spreadsheet_id


# Kopfzeilen für Google Sheet
header = ["Name", "Alter", "Geschlecht", "Trainingsschwerpunkt", "Motivation", "Trainingserfahrung",
          "Sportarten", "Verletzungen", "Beruf", "Schlaf", "Ernährung", "Ziele",
          "Trainingstage/Woche", "Erwartung an Trainer", "Fitnessstudio-Zugang", "Heim-Equipment"]

# Kundendaten speichern
if st.button("Kundenprofil speichern"):
    neuer_Kunde = {
        "Name": name,
        "Alter": alter,
        "Geschlecht": geschlecht,
        "Trainingsschwerpunkt": Trainingsschwerpunkt,
        "Motivation": Motivation,
        "Trainingserfahrung": Trainingserfahrung,
        "Sportarten": Sportarten,
        "Verletzungen": Verletzungen,
        "Beruf": Beruf,
        "Schlaf": schlaf,
        "Ernährung": Ernährung,
        "Ziele": Ziele,
        "Trainingstage/Woche": Woche,
        "Erwartung an Trainer": Trainer,
        "Fitnessstudio-Zugang": Zugang,
        "Heim-Equipment": Home,
        "Email": Email
    }

    # Google Sheets Service initialisieren
    service, spreadsheet_id = init_google_sheet()

    # Kopfzeile in Google Sheets schreiben (nur beim ersten Mal nötig)
    values = [header]
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="A1:Q1",
        valueInputOption="RAW",
        body=body
    ).execute()

    # Formatierung und Spaltenbreite per batchUpdate
    requests = [
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

    # Google Sheets mit gspread autorisieren und Daten anhängen
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    service_account_info = json.loads(st.secrets["google"]["service_account_json"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1

    # Neue Kundendaten als Liste anhängen
    sheet.append_row([neuer_Kunde[col] for col in header])

    st.success("Kunde wurde in Google Sheets eingetragen!")







