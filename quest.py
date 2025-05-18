import os
from utils import getList, initLogger, updateGoogleSheet
import requests
MAVIS_API = os.environ["MAVIS_API"]

logger = initLogger("quest.log")

def verify_quest(userdata, quest_type, variant):
    
    url = 'https://api-gateway.skymavis.com/graphql/marketplace'

    mutation_query = """
    mutation VerifyQuest($userAddress: String!, $questType: QuestType!, $variant: String!) {
      verifyQuest(userAddress: $userAddress, questType: $questType, variant: $variant) {
        questId: title
        type
        title
        status
        __typename
      }
    }
    """

    variables = {
        "userAddress": userdata['Address'],
        "questType": quest_type,
        "variant": variant
    }

    headers = {
        'authorization': f'Bearer {userdata["BearerToken"]}',
        'Accept': 'application/json',
        'X-API-Key': MAVIS_API
    }

    payload = {
        "operationName": "VerifyQuest",
        "query": mutation_query,
        "variables": variables
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "errors" not in data:
            quest = data["data"]["verifyQuest"] 
            logger.info(f"{quest['type']} - Status: {quest['status']}")
            return True
        else:
            error_message = data['errors'][0]['message']
            if error_message == 'Quest is already completed':
                logger.info(f'{quest_type} - {error_message}')
                return True
            elif error_message == 'Token invalid':
                logger.error(f'{quest_type} - {error_message}')
                tokens = getNewToken(userdata["RefreshToken"]) #and try again
                if tokens:
                    updateGoogleSheet(userdata['Name'], tokens['accessToken'], tokens['refreshToken'],"AtiaBlessing", "Axies")
                return False
            else:
                logger.error(f'Error: {quest_type} - {error_message}')
            return False
    else:
        logger.error(f"Error HTTP: {response.status_code} - {response.text}")
        return False


def getNewToken(rToken):
    logger.info(f'Getting new Token and Try again. also update google sheet to store bearer and refresh token.')
    AUTH_TOKEN_REFRESH_URL = "https://athena.skymavis.com/v2/public/auth/token/refresh"
    payload = {'refreshToken':rToken}
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url=AUTH_TOKEN_REFRESH_URL, json=payload, headers=headers)
    if 'accessToken' not in r.json():
        logger.info(f'Refresh worked!')
    else:
        print(r.json()['error_message'])
        return False
    return r.json()

def main():
    ar = getList()
    for a in ar:
        logger.info(f"{a['Address']} | {a['Name']}")
        if not verify_quest(a, "PrayAtia", "0"):
            #2nd try
            verify_quest(a, "PrayAtia", "0")
        verify_quest(a, "RollPouch", "0")
        verify_quest(a, "Win1ClassicBattle", "0")
        verify_quest(a, "Win1OriginsBattle", "0")
        verify_quest(a, "FeedCocoOwnedAxie", "0")
        logger.info('-' * 80)
main()