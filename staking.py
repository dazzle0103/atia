import os
from contracts.staking_abi import ronin_staking_abi, ronin_staking_address
from utils import getListOfValidatorAddresses, initLogger, initWeb3

logger = initLogger("staking.log")

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
    contract, account = initWeb3(private_key, ronin_staking_address, ronin_staking_abi, ronin_rpc)
    list_of_validators = getListOfValidatorAddresses()
    delegateAddress = "0x56f2B69D8f20568f69Eb4107733a1a2ce7BBc0Bc" #fableborn

    #tx_hash = contract.functions.delegateRewards(list_of_validators, delegateAddress).transact({'from': account.address})
    #logger.info(f"Restaking complete! URL:https://app.roninchain.com/tx/0x{tx_hash.hex()}")
    print(list_of_validators)