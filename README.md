# VoidCoin

See it in action [here](http://parousia.pythonanywhere.com/)

A blockchain implementation in `python` and `django`. It builds largely on
[this]((https://hackernoon.com/learn-blockchains-by-building-one-117428612f46))
and [this](http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/).

## Features

1. Multiple wallets per user and saving in a django database (not recommended in a production system)
1. Signed transactions using private key
1. Node registration
1. User registration (optional). To keep things simple, registration only requires a user to provide an email
(not necessarily valid, but format is important) and a unique screen name (for identification)

## Views

### Home

This view shows a list of all blocks on the blockchain. A list of all signed and verified transactions that have not been added to a block are also shown

### Wallet Index

This shows a list of all wallets in the system. The wallets are stored in a django database with the following fields

    `alias` This is an identifier to help a registered user different between their different wallets
    `owner` This is the name of the registered user who creates the wallet
    'public_key` The wallet address or public key
    `private_key` The wallet private key. Only the user who owns this wallet can see this key, in their dashboard
    `balance` The amount of coin balance in the wallet

### Transactions Index

This shows a list of every single transaction in the blockchain

### Nodes index

This shows a list of all registered nodes

### Account view

Shows a user's account and all the wallets they own

## Resources
1. [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
1. [A Practical Introduction to Blockchain with Python](http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/)
1. [Blockchain demo](https://anders.com/blockchain/)

## To do

1. Activate recaptcha
1. Subtract coin from sender. Add coin to receiver
1. Limit total coin to amount in COINBASE

