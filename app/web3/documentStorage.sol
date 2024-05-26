pragma solidity ^0.8.0;

contract DocumentStorage {
    struct Document {
        bytes32 hash;
        address owner;
    }
    
    mapping(bytes32 => Document) public documents;

    function uploadDocument(bytes32 hash) public {
        require(documents[hash].hash == 0, "Document already exists");

        documents[hash] = Document(hash, msg.sender);
    }

    function sendDocument(bytes32 hash, address recipient) public {
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");

        documents[hash].owner = recipient;
    }
}