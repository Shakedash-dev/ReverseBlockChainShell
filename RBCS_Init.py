## Name        : ReverseBlockChainShell_Server_init_.py
## Date        : 30.01.2022
## Author      : Shkedo
## Description : This program will create a smart contract to connect to from the victim and attacker.
##               The program will print the address of the contract.
##               Be sure to insert the address to the CONTRACT_ADDRESS variable in both files.
##               Also, keep in mind that the address deploying needs to be the same as the address using the server (attacker).
##               And the victim address needs to be different.

# Imports.
from asyncio.windows_events import NULL
import os
from solcx import compile_standard
import json
from web3 import Web3
import math
from dotenv import load_dotenv

# Constants.
SOLIDITY_VERSION = "0.6.0"
CONTRACT_NAME = "Shell"
CONTRACT_FILE_PATH = "CnC.sol"
GANACHE_SERVICE = "HTTP://127.0.0.1:7545"
TESTNET_ID = 1337
ACCOUNT0_ADDR = "0xFd0cb7aE687CBf558724BF0e1543D81De92500B0"

# Main
def main():

    # Import enviorment variables.
    load_dotenv()

    # Compile contract.
    compiled_file = open("CompiledContract.json", "w")
    compiled_contract = CompileContrat(CONTRACT_FILE_PATH)

    # Dump the compiled contract into a json and get the abi and bytecode out of it.
    json.dump(compiled_contract, compiled_file)
    bytecode = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["evm"][
        "bytecode"
    ]["object"]
    abi = compiled_contract["contracts"][CONTRACT_FILE_PATH][CONTRACT_NAME]["abi"]

    # Initialize the web3 provider object.
    w3_engine = Web3(Web3.HTTPProvider(GANACHE_SERVICE))

    # Deploy the contract on ganache using web3.
    DiffCoinContract_forDeployment = w3_engine.eth.contract(abi=abi, bytecode=bytecode)
    DeployTx = w3_engine.eth.account.sign_transaction(
        DiffCoinContract_forDeployment.constructor().buildTransaction(
            {
                "gasPrice": w3_engine.eth.gas_price,
                "chainId": TESTNET_ID,
                "from": ACCOUNT0_ADDR,
                "nonce": w3_engine.eth.getTransactionCount(ACCOUNT0_ADDR),
            }
        ),
        os.getenv(
            "PRIVATE_KEY0"
        ),  # Takes the private key from ".env" file. (for privacy reasons)
    )
    tx_hash = w3_engine.eth.send_raw_transaction(DeployTx.rawTransaction)
    tx_receipt = w3_engine.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract Address: {tx_receipt.contractAddress}")
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
