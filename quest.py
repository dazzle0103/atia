import logging
import logging.handlers
import os
from utils import getList

import requests
MAVIS_API = os.environ["MAVIS_API"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "quest.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)




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
            return data["data"]["verifyQuest"]
        else:
            if data['errors'][0]['message'] == 'Quest is already completed':
                logger.info(f'{quest_type} - Quest is already completed')
            else:
                logger.error(f"Error: {data['errors']}")
            return None
    else:
        logger.error(f"Error HTTP: {response.status_code} - {response.text}")
        return None

def main():
    ar = getList()
    for a in ar:
        logger.info(f"{a['Address']} | {a['Name']}")
        verify_quest(a, "PrayAtia", "0")
        verify_quest(a, "RollPouch", "0")
        verify_quest(a, "Win1ClassicBattle", "0")
        verify_quest(a, "Win1OriginsBattle", "0")
        verify_quest(a, "FeedCocoOwnedAxie", "0")
        logger.info('-' * 80)
main()