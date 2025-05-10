import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

def isValid(date_str):
    try:
        return datetime.today().date() <= datetime.strptime(date_str, "%d/%m/%Y").date()
    except Exception as e:
        print(f"Invalid date format: {date_str}, error: {e}")
        return False

def getListOfAddresses():
    return getListOf('Address')

def getListOfBearerToken():
    return getListOf('BearerToken')

def getListOf(header):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        #credentials = Credentials.from_service_account_file("axiescholar-458710-fa392456405b.json", scopes=scopes)
        service_account_info = json.loads(os.environ["GOOGLE_SHEETS_CREDENTIALS"])
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(credentials)

        sheet = client.open("Axies").worksheet("AtiaBlessing")
        list_of_dicts = sheet.get_all_records()
        
        filtered_list = [
            entry for entry in list_of_dicts
            if 'Enddate' in entry and header in entry and isValid(entry['Enddate'])
        ]
        return [entry[header] for entry in filtered_list]
    except Exception as e:
        print(f"Error in getListOf({header}): {e}")
        return []

def getList():
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        #credentials = Credentials.from_service_account_file("axiescholar-458710-fa392456405b.json", scopes=scopes)
        service_account_info = json.loads(os.environ["GOOGLE_SHEETS_CREDENTIALS"])
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(credentials)

        sheet = client.open("Axies").worksheet("AtiaBlessing")
        list_of_dicts = sheet.get_all_records()
        
        filtered_list = [
            entry for entry in list_of_dicts
            if 'Enddate' in entry and isValid(entry['Enddate'])
        ]
        return [entry for entry in filtered_list]
    except Exception as e:
        print(f"Error in getList(): {e}")
        return []
