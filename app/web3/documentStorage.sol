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

    struct Transaction {
        string name;
        string hash;
        address sender;
        address recipient;
        TransactionType txType;
        uint timestamp;
        bool status;
    }

    mapping(string => Document) private documents;
    mapping(address => string[]) private userDocuments;
    mapping(address => Transaction[]) private userTransactions;
    string[] private allDocuments; // Массив всех документов

    event DocumentUploaded(string hash, address indexed owner, string docName, uint timestamp);
    event DocumentSent(string hash, address indexed owner, address indexed recipient);
    event DocumentDeleted(string hash, address indexed owner);
    event TransactionRecorded(address indexed user, string hash, TransactionType txType, uint timestamp);

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

        userTransactions[msg.sender].push(Transaction({
            name: docName,
            hash: hash,
            sender: msg.sender,
            recipient: address(0),
            txType: TransactionType.Upload,
            timestamp: now,
            status: true
        }));

        emit DocumentUploaded(hash, msg.sender, docName, now);
        emit TransactionRecorded(msg.sender, hash, TransactionType.Upload, now);
    }

    function sendDocument(string memory hash, address recipient) public {
        require(bytes(hash).length > 0, "Hash cannot be empty");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");
        require(recipient != msg.sender, "Cannot send document to yourself");
        require(documents[hash].recipient == address(0), "Document already sent");

        documents[hash].recipient = recipient;
        documents[hash].transactionType = TransactionType.Send;
        documents[hash].isSent = true;

        // Добавляем транзакцию только один раз для отправителя и получателя
        userTransactions[msg.sender].push(Transaction({
            name: documents[hash].docName,
            hash: hash,
            sender: msg.sender,
            recipient: recipient,
            txType: TransactionType.Send,
            timestamp: now,
            status: true
        }));

        userTransactions[recipient].push(Transaction({
            name: documents[hash].docName,
            hash: hash,
            sender: msg.sender,
            recipient: recipient,
            txType: TransactionType.Send,
            timestamp: now,
            status: true
        }));

        emit DocumentSent(hash, msg.sender, recipient);
        emit TransactionRecorded(msg.sender, hash, TransactionType.Send, now);
    }

    function deleteDocument(string memory hash) public {
        require(bytes(hash).length > 0, "Hash cannot be empty");
        require(documents[hash].owner == msg.sender, "You are not the owner of this document");

        userTransactions[msg.sender].push(Transaction({
            name: documents[hash].docName,
            hash: hash,
            sender: msg.sender,
            recipient: address(0),
            txType: TransactionType.Delete,
            timestamp: now,
            status: true
        }));

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
        emit TransactionRecorded(msg.sender, hash, TransactionType.Delete, now);
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

    function getAllUserTransactions() public view returns (Transaction[] memory) {
        uint count = userTransactions[msg.sender].length;
        for (uint i = 0; i < allDocuments.length; i++) {
            if (documents[allDocuments[i]].recipient == msg.sender) {
                count++;
            }
        }

        Transaction[] memory allTransactions = new Transaction[](count);
        uint index = 0;

        for (uint i = 0; i < userTransactions[msg.sender].length; i++) {
            allTransactions[index] = userTransactions[msg.sender][i];
            index++;
        }

        for (uint i = 0; i < allDocuments.length; i++) {
            if (documents[allDocuments[i]].recipient == msg.sender) {
                allTransactions[index] = Transaction({
                    name: documents[allDocuments[i]].docName,
                    hash: documents[allDocuments[i]].hash,
                    sender: documents[allDocuments[i]].owner,
                    recipient: msg.sender,
                    txType: documents[allDocuments[i]].transactionType,
                    timestamp: documents[allDocuments[i]].timestamp,
                    status: documents[allDocuments[i]].isSent
                });
                index++;
            }
        }

        return allTransactions;
    }

}