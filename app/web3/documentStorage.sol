pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract DocumentStorage {
    enum TransactionType { None, Upload, Delete, Download, Send }

    struct Document {
        string docName;
        string hash;
        address owner;
        address recipient;
        TransactionType transactionType;
        bool isSent;
        uint timestamp;
        uint size;
    }

    mapping(string => Document) private documents;
    mapping(address => string[]) private userDocuments;
    string[] private allDocuments; // Массив всех документов

    event DocumentUploaded(string hash, address indexed owner, string docName, uint timestamp);
    event DocumentSent(string hash, address indexed owner, address indexed recipient);
    event DocumentDeleted(string hash, address indexed owner);

    function uploadDocument(string memory hash, string memory docName, uint size) public {
        require(bytes(hash).length > 0, "Hash cannot be empty");
        require(bytes(docName).length > 0, "Document name cannot be empty");
        require(documents[hash].owner == address(0), "Document already exists");

        documents[hash] = Document({
            docName: docName,
            hash: hash,
            owner: msg.sender,
            recipient: address(0),
            transactionType: TransactionType.Upload,
            isSent: false,
            timestamp: now, // Store current block timestamp
            size: size
        });

        userDocuments[msg.sender].push(hash);
        allDocuments.push(hash);

        emit DocumentUploaded(hash, msg.sender, docName, now);
    }

    function sendDocument(string memory hash, address recipient) public {
        require(bytes(hash).length > 0, "Hash cannot be empty");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");
        require(recipient != msg.sender, "Cannot send document to yourself");
        require(documents[hash].recipient == address(0), "Document already sent");

        documents[hash].recipient = recipient;
        documents[hash].transactionType = TransactionType.Send;
        documents[hash].isSent = true;

        emit DocumentSent(hash, msg.sender, recipient);
    }

    function deleteDocument(string memory hash) public {
        require(bytes(hash).length > 0, "Hash cannot be empty");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");

        delete documents[hash];

        // Remove from userDocuments array
        string[] storage userDocs = userDocuments[msg.sender];
        for (uint i = 0; i < userDocs.length; i++) {
            if (keccak256(abi.encodePacked(userDocs[i])) == keccak256(abi.encodePacked(hash))) {
                userDocs[i] = userDocs[userDocs.length - 1];
                userDocs.pop();
                break;
            }
        }

        emit DocumentDeleted(hash, msg.sender);
    }

    function getDocumentOwner(string memory hash) public view returns (address) {
        return documents[hash].owner;
    }

    function getDocumentRecipient(string memory hash) public view returns (address) {
        return documents[hash].recipient;
    }

    function getTransactionType(string memory hash) public view returns (TransactionType) {
        return documents[hash].transactionType;
    }

    function isDocumentSent(string memory hash) public view returns (bool) {
        return documents[hash].isSent;
    }

    function getDocumentTimestamp(string memory hash) public view returns (uint) {
        return documents[hash].timestamp;
    }

    function getUserDocuments() public view returns (Document[] memory) {
        Document[] memory docs = new Document[](userDocuments[msg.sender].length);
        for (uint i = 0; i < userDocuments[msg.sender].length; i++) {
            docs[i] = documents[userDocuments[msg.sender][i]];
        }
        return docs;
    }

    function getReceivedDocuments() public view returns (Document[] memory) {
        uint count = 0;
        
        // Create a temporary array to count the number of received documents
        for (uint i = 0; i < allDocuments.length; i++) {
            if (documents[allDocuments[i]].recipient == msg.sender) {
                count++;
            }
        }

        // Create an array to hold the recipient's documents
        Document[] memory receivedDocs = new Document[](count);
        uint index = 0;
        for (uint i = 0; i < allDocuments.length; i++) {
            if (documents[allDocuments[i]].recipient == msg.sender) {
                receivedDocs[index] = documents[allDocuments[i]];
                index++;
            }
        }
        return receivedDocs;
    }

}