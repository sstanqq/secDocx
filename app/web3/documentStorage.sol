pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract DocumentStorage {
    enum TransactionType { Store, Send }

    struct Document {
        string hash;
        address owner;
        TransactionType transactionType;
        string name;
        uint size;
        uint timestamp;
    }

    mapping(address => string[]) private userDocuments;
    mapping(string => Document) public documents;

    function uploadDocument(string memory hash, string memory name, uint size) public {
        require(bytes(documents[hash].hash).length == 0, "Document already exists");

        documents[hash] = Document(hash, msg.sender, TransactionType.Store, name, size, now);
        userDocuments[msg.sender].push(hash);
    }

    function sendDocument(string memory hash, address recipient) public {
        require(bytes(documents[hash].hash).length != 0, "Document does not exist");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");

        documents[hash].owner = recipient;
        documents[hash].transactionType = TransactionType.Send;
    }

    function deleteDocument(string memory hash) public {
        require(bytes(documents[hash].hash).length != 0, "Document does not exist");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");

        delete documents[hash];
        string[] storage userDocs = userDocuments[msg.sender];
        for (uint i = 0; i < userDocs.length; i++) {
            if (keccak256(abi.encodePacked(userDocs[i])) == keccak256(abi.encodePacked(hash))) {
                userDocs[i] = userDocs[userDocs.length - 1];
                userDocs.pop();
                break;
            }
        }
    }

    function getUserDocuments() public view returns (Document[] memory) {
        Document[] memory docs = new Document[](userDocuments[msg.sender].length);
        for (uint i = 0; i < userDocuments[msg.sender].length; i++) {
            docs[i] = documents[userDocuments[msg.sender][i]];
        }
        return docs;
    }
}