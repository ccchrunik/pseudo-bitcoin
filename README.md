# NM-Lab Blockchain

## Prerequisites

```bash
$ pip3 install virtualenv
$ virtualenv -p python3.7 venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

## Usage
### Change to `src` directory (Important!!!)
```bash
$ cd src
$ chmod +x pseudoBitcoin.py
```

### All Command
```
Usage: pseudoBitcoin.py [OPTIONS] CMD

Options:
  -n, --name TEXT           create the blockchain by the given name
  -a, --address TEXT        account address
  -u, --username TEXT       create a new user one the blockchain
  -b, --balance INTEGER     value to add to or substract from account balance
  -h, --height INTEGER      Print blocks with the given height in the
                            blockchain

  -d, --direction TEXT      The direction of print block funcion (front or
                            back)

  -from TEXT                transaction source
  -to TEXT                  transaction destination
  -amount INTEGER           transaction value
  -o, --option TEXT         The option for several commands, force: fire
                            transactions

  -r, --repetition INTEGER  How many times to send a same transaction
  --help                    Show this message and exit.
```

### Create a blockchain
```bash
$ ./pseudoBitcoin.py createblockchain -n <THE_FIRST_USER_NAME>
```

### Create a user
```bash
$ ./pseudoBitcoin.py createuser -u <USER_NAME>
```

### Send a transaction
```bash
# normal case
$ ./pseudoBitcoin.py send -from <SENDER_ADDRESS> -to <RECEIVER_ADDRESS> -amount <VALUE>

# repetition
$ ./pseudoBitcoin.py send -from <SENDER_ADDRESS> -to <RECEIVER_ADDRESS> -amount <VALUE> -r <REP_TIMES>

# force to mine a block
$ ./pseudoBitcoin.py send -from <SENDER_ADDRESS> -to <RECEIVER_ADDRESS> -amount <VALUE> -o force

# Combine the above two cases
$ ./pseudoBitcoin.py send -from <SENDER_ADDRESS> -to <RECEIVER_ADDRESS> -amount <VALUE> -r <REP_TIMES> -o force
```

### Print the whole blockchain
```bash
$ ./pseudoBitcoin.py printchain
```

### Print part of the blockchain
```bash
# print the first <HEIGHT> blocks
$ ./pseudoBitcoin.py printblock -h <HEIGHT> 

# print the last <HEIGHT> blocks
$ ./pseudoBitcoin.py printblock -h <HEIGHT> -d back

# print a single block with the given block
$ ./pseudoBitcoin.py printblock -h <HEIGHT> -d unique
```

### Example
```bash
$ ./pseudoBitcoin.py createblockchain -n 'Eric Chen'
$ ./pseudoBitcoin.py createuser -u 'user 1'
$ ./pseudoBitcoin.py send -from rE4pJEL7Uaj4PosP87twdGu9bayVvv8wnhhKRvWHpq8ND3C3suWGyDcn7NqKSYXiyJT3T4s -to wWsJgk7iNindSY9P3f8S8Ycvat3TTPJ8RwZUZpFfZHQzmWpyYZowj8qAoCd75SVphCcJTRg -amount 1
$ ./pseudoBitcoin.py printchain
$ ./pseudoBitcoin.py printblock -h 0 -d back
```

## Functionalities

In this project, I implement several features listed below
- Block
- Blockchain
- PoW
- Database (folder)
- Command Line Interface
- Account model
- Sign and Verify
- Mining reward
- Merkle Tree
- Additional features
    - transactions grouping
    - blocks grouping
    - files grouping
    - Instant storage
    - Well-documented source code

Most features are the implemented nearly the same as told in the NM-Lab course, so I will skip them. Instead, I will talk about some additional features that I modify or add in this project.

### Database
I use `json` module to save and retrieve data. I choose it because it can save data in human-readable format.

For **Block**, **Wallet** and **Transaction**, I all implemented **serialze** and **deserialze** static methods for the blockchain to easily transform class data to a string and then save it to some specific files.

### Account Model
Since UTXO model is too complicated as I added more and more features on the blockchain, I decided to switch to Account model for its simplicity. I name it **Wallet** in my project.

In each wallet, it has 5 attributes
- name
- balance
- signing key
- verifying key
- address

The address will be generated when the wallet is created. Be careful, you have only one chance to remember you account address (though now you can directly see it under `/data/info/wallet`) if someone wrap it to a frontend program.

Other attributes cannot be directly accessed by users. You can get balance by calling the class methods. However, signingkey and verifying key are used only in internal methods, users have no means to get it.

By the way, I store all wallet in a **WalletPool** class instance, all operation in the blockchain only use WalletPool interface to interact with a specific wallet.


### Transactions
I store all transactions in a single **TransactionPool**.

A transaction has the following attributes
- source
- dest
- amount
- signature

The transaction signature will be generated when a transaction is being added to the transaction pool.

The **Transaction** class has **sign** and **verify** static methods for the blockchain to call and do sign and verify operations.

### Command Line Interface
I use `click` module to parse command line argument. 

To make the each functionality more manageable, I separate the main function and command line functions. I put command functions under `/src/Command.py`. 

I use **decorator factory** to provide a single entry point for executing the command. You can see the source code if you are interested.


### Transactions Grouping
Instead of wrapping a single transactions in a block, I set a threshold (100 in this project). Once we have **100** transactions, the blockchain will **automatically** wrap those transactions into a block. However, in the cli program, you actually can use `force` to fire transactions even it does not touch the threshold.

### Blocks Grouping
I set a `threshold` variable to make at most `threshold` number of blocks in each file. In the current settings, `threshold` is `100`. Once the number of blocks in a file exceed 100, I will **automatically** close it and create a new file with the subsequent index.

### Files Grouping
I split the data on the blockchain into two parts: **metadata** and **blocks data**. 

The metadata contains many metadata including **blockchain internal settings**, **users** and **uncommited transactions**, which are stored under `/data/info` folder.

The blocks data contains **all blocks data** including genesis block, which are stored under `/data/data` folder.


### Instant Storage
Although it sometimes being ignored when you only use cli instead of the underlying classes, I actually write some code to make the blockchain **store each transaction, each block, each user in the folder when they are created** rather than save all data just before the blockchain is terminated.


### Well-documented Source Code

For each class, I write some simple documentation about the accessible attributes and public methods and static methods.

For each methods, I write a little bit more about the description and interface of the method.

For each methods, I write some comments to clarify the logic to make reader easier to understand the implementation of each methods.

### More
Look at the source for more information.


## Source code
- https://github.com/woodcutter-eric/pseudo-bitcoin