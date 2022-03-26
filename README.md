# ReverseBlockChainShell
RBCS (Reverse BlockChain Shell) is a tool that allows you to execute commands on a remote station running with complete anonymity.\
RBCS can work on any <a href="https://ethereum.org/en/">Ethereum</a> based network, e.g. Ethereum-MainNet or all other testnets.

![RBCS POC](https://github.com/Shakedash-dev/ReverseBlockChainShell/blob/main/RBCS.jpg)

## Pros & Cons
| Pros        | Cons        |
| ----------- | ----------- |
| Complete Anonimity | Require internet connection on both sides |
|  | Takes time to run each command |
|  | Setup requires basic blockchain knowledge |

## Requirements
This tool is setup to work on ganache for POC. To use this tool on a real network, you'll need to do the following steps:
1. Create an account on a network of your choise.
2. Give it some ETH.
3. Set `ACCOUNT_ADDR` to the your account address in `RBCS_Init.py`, `RBCS_Server.py`, and `RBCS_Client.py`.
3. Set `PRIVATE_KEY` to the your account's private key in `RBCS_Init.py`, `RBCS_Server.py`, and `RBCS_Client.py`.
4. Get an RPC URL from the internet in one way or another and set `RPC_URL` to it in `RBCS_Init.py`, `RBCS_Server.py`, and `RBCS_Client.py`.

## Usage
To use this tool you will need to follow these steps:
1. Run `RBCS_Init.py`.
2. In scripts `RBCS_Client.py` and `RBCS_Server.py` set `CONTRACT_ADDR` to the output of `RBCS_Init.py`.
3. Run server.
4. Run client on the remote machine.

## Dependencies
python3 in any version.\
Connection to the internet on both server and client.
