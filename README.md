# ReverseBlockChainShell
RBCS (Reverse BlockChain Shell) is a tool that allows you to execute commands on a remote station running with complete anonymity.\
RBCS can work on any Ethereum based network, e.g. Ethereum-MainNet or all other testnets.

## TestNets vs. MainNet
If you choose to use a testnet and not the mainnet, you won't need to pay real money to use the tool. Because testnet's ether is worthless.\
But testnets require some sort of authentication to gather test-Ether so this can leave a lead to the identity of the user.

## Usage
To use this tool you will need to follow these steps:
1. Create 2 wallets in a blockchain network.
2. In scripts `RBCS_Server.py` and `RBCS_Init.py` set `PRIVATE_KEY` to the first account's private key, and `ACCOUNT_ADDR` to the first account address.
3. In script `RBCS_Client.py` set `PRIVATE_KEY` to the second account's private key, and `ACCOUNT_ADDR` to the second account address.
4. Run `RBCS_Init.py`.
5. In scripts `RBCS_Client.py` and `RBCS_Server.py` set `CONTRACT_ADDR` to the output of `RBCS_Init.py`.
6. Run server.
7. Run client on the remote machine.


## Dependencies
python3 in any version.\
Connection to the internet on both server and client.
