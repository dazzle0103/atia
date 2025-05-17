import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json
import logging
import logging.handlers

from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import (SignAndSendRawMiddlewareBuilder, ExtraDataToPOAMiddleware)


def initWeb3(private_key, contract_address, contract_abi, ronin_rpc):
    # assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    # assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
    w3 = Web3(Web3.HTTPProvider(ronin_rpc))
    account: LocalAccount = Account.from_key(private_key)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

    checksumAddress = Web3.to_checksum_address(contract_address)
    contract = w3.eth.contract(address=checksumAddress, abi=contract_abi)
    return contract, account



def initLogger(filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger




def isValid(date_str):
    try:
        return datetime.today().date() <= datetime.strptime(date_str, "%d/%m/%Y").date()
    except Exception as e:
        print(f"Invalid date format: {date_str}, error: {e}")
        return False

def loginGoogle():
    scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    #credentials = Credentials.from_service_account_file("axiescholar-458710-fa392456405b.json", scopes=scopes)
    service_account_info = json.loads(os.environ["GOOGLE_SHEETS_CREDENTIALS"])
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(credentials)
    return client

def getData(worksheet, workbook="Axies"):
    try:
        client = loginGoogle()

        sheet = client.open(workbook).worksheet(worksheet)
        list_of_dicts = sheet.get_all_records()
        
        return list_of_dicts
    except Exception as e:
        print(f"Error in getData): {e}")
        return []


def getListOfAccountAddresses():
    return getListOf('Address')

def getListOfBearerToken():
    return getListOf('BearerToken')

def getListOfValidatorAddresses():
     list_of_validators = getData("Staking")
     return [entry['Address'] for entry in list_of_validators]

def getListOf(header, worksheet="AtiaBlessing", workbook="Axies"):    
        filtered_list = [
            entry for entry in getData(worksheet, workbook)
            if 'Enddate' in entry and header in entry and isValid(entry['Enddate'])
        ]
        return [entry[header] for entry in filtered_list]
    
def getList(worksheet="AtiaBlessing", workbook="Axies"):
    try:
        client = loginGoogle()

        sheet = client.open(workbook).worksheet(worksheet)
        list_of_dicts = sheet.get_all_records()
        
        filtered_list = [
            entry for entry in list_of_dicts
            if 'Enddate' in entry and isValid(entry['Enddate'])
        ]
        return filtered_list
    except Exception as e:
        print(f"Error in getList(): {e}")
        return []
