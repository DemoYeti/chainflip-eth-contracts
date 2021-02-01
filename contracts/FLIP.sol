pragma solidity ^0.7.0;


import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./abstract/Shared.sol";


contract FLIP is ERC20, Ownable, Shared {
    
    constructor(
        string memory name, 
        string memory symbol, 
        address receiver, 
        uint256 mintAmount
    ) ERC20(name, symbol) Ownable() {
        _mint(receiver, mintAmount);
    }

    function mint(address receiver, uint amount) external nzAddr(receiver) nzUint(amount) onlyOwner {
        _mint(receiver, amount);
    }
}