import logging
import logging.handlers
import os
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import (SignAndSendRawMiddlewareBuilder, ExtraDataToPOAMiddleware)
from abi import abi

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

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
    logger.info(f"Loading secrets: {SOME_SECRET}")
    # assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    # assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
    w3 = Web3(Web3.HTTPProvider(ronin_rpc))
    account: LocalAccount = Account.from_key(private_key)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

    contract_address = '0x9D3936dBd9A794Ee31eF9F13814233D435bD806C' #atia blessing
    checksumAddress = Web3.to_checksum_address(contract_address)
    contract = w3.eth.contract(address=checksumAddress, abi=abi)
    accounts = [
        '0xd3daf3c63cc00b7e178985be0e446ba6f5dcece7', #amusedCamel
        '0x99f1ad08af12f51e337643ae8b224bee1a83f4f3', #feistyTomato
        '0xf57a14a0a2c9e1836f8cfc249516ec2b01b80182', #wigglyCow
        #'0x6df463a86f15ab754223fc56c99c2c24b9b42d2c', rainWeasel
        #'0x5886Dc1c4F14C5ab8e0E77eb50A3aFE4B0b06761' #dev
    ]
    _from = '0x5886Dc1c4F14C5ab8e0E77eb50A3aFE4B0b06761' #dev
    for user in accounts:
        status = contract.functions.getActivationStatus(Web3.to_checksum_address(user)).call()
        if status[1] == False:
            logger.info(f"User: {user} -> Starting Blessing Transaction")
            tx_hash = contract.functions.activateStreak(Web3.to_checksum_address(user)).transact({'from': _from})
            logger.info(f"User: {user} -> Transaction complete! {tx_hash}")
        else:
            logger.info(f"User: {user} -> Already blessed")
    logger.info('-' * 80)
