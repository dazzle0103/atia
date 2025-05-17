import os
from web3 import Web3
from contracts.atia_abi import atia_abi, atia_address
from utils import getListOfAccountAddresses, initLogger, initWeb3






logger = initLogger("status.log")

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "SOME_SECRET not available!"

try:
    private_key = os.environ["PRIVATE_KEY"]
except KeyError:
    SOME_SECRET = "KEY not available!"

try:
    ronin_rpc = os.environ["RONIN_RPC"]
except KeyError:
    SOME_SECRET = "ronin_rpc not available!"




if __name__ == "__main__":
    contract, account = initWeb3(private_key, atia_address, atia_abi, ronin_rpc)    
    accounts = getListOfAccountAddresses()
    
    for user in accounts:
        status = contract.functions.getActivationStatus(Web3.to_checksum_address(user)).call()
        if status[1] == False:
            tx_hash = contract.functions.activateStreak(Web3.to_checksum_address(user)).transact({'from': account.address}) #dev
            logger.info(f"User: {user} -> Transaction complete! URL:https://app.roninchain.com/tx/0x{tx_hash.hex()}")
        else:
            logger.info(f"User: {user} -> Already blessed")
    logger.info('-' * 80)
