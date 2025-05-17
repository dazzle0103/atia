import logging
import logging.handlers
import os
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import (SignAndSendRawMiddlewareBuilder, ExtraDataToPOAMiddleware)
from .contracts.staking_abi import staking_abi, staking_address
from utils import getListOfValidatorAddresses

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "staking.log",
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
    # assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    # assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
    w3 = Web3(Web3.HTTPProvider(ronin_rpc))
    account: LocalAccount = Account.from_key(private_key)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

    checksumAddress = Web3.to_checksum_address(staking_address)
    contract = w3.eth.contract(address=checksumAddress, abi=staking_abi)
    list_of_validators = getListOfValidatorAddresses()
    
    delegateAddress = "0x56f2B69D8f20568f69Eb4107733a1a2ce7BBc0Bc" #fableborn

    #tx_hash = contract.functions.delegateRewards(list_of_validators, delegateAddress).transact({'from': account.address})
    #logger.info(f"Restaking complete! URL:https://app.roninchain.com/tx/0x{tx_hash.hex()}")
    print(list_of_validators)