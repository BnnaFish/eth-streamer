# eth-streamer

## Description

Test project to learn blockchain api.

Script that starts streaming addresses of ERC721 smart contracts that were created in the block, starting from the N-th block on Ethereum blockchain.
Each block should print an array of ERC721 smart contract addresses in the console.


## High level architecture

There is no strict way to determine if a contract is ERC-721 or not.

I'm using the hack inspired by this [article](https://medium.com/hackernoon/https-medium-com-momannn-live-testing-smart-contracts-with-estimategas-f45429086c3a)

Basically, if a contract implements the ERC interface then it's a [duck](https://i.ytimg.com/vi/WM1x2L1dFJk/maxresdefault.jpg).

Probing interface is made by get_estimatedGas rpc call. It will either be rejected(meaning no such method) or succeed.

If all methods succeed then I assume contract is highly likely to follow ERC-721 standart.

Necessary methods are: safeTransferFrom, ownerOf and balanceOf.

## Algorithm flow:

1. Get all transactions in a current block by calling eth_getBlockByNumber rpc
2. Keep only those with "to" attribute equals to null. (Contract created)
3. For each of them call eth_getTransactionReceipt to get created contracts address
4. Make 3 eth_estimateGas calls for each of the necessary methods
5. Yield result if all succeed

## Implementation

Service is made on top of python 3.10 and asyncio stack.

Uses Infura node api to make json-rpc calls to ethereum.

RPC calls made via http protocol.

Pipeline runs sequentially step by step. But http calls run concurrently where possible.
E.g. eth_getTransactionReceipt calls made in a batch mode all at once for all transactions in a block.
Full concurrency could be achieved using asynchronous queues but with significantly increasing code complexity.

## Current limitations

Script will break reaching head of blockchain. Could be fixed via while-true-sleep loop.
But this will add more complexity to configure.
Seems to be not so important in test project. But necessary in real production.

## Usage

First, [Infura](https://infura.io/) account have to be created to get an api key.

The key has to be placed in .env file just like in the default.env file.

Initial block id may be changed in docker-compose.yml. Default value is 13821429.

To run service:

``` bash
make dc.run
````

Stdout example:
```
Successfully built 404165cdb612
Successfully tagged eth-streamer_web:latest
Recreating eth-streamer_web_1 ... done
Attaching to eth-streamer_web_1
web_1               | ['0xd16bdccae06dfd701a59103446a17e22e9ca0ef0']
web_1               | ['0x0406db8351aa6839169bb363f63c2c808fee8f99']
web_1               | ['0xa7ccd0326757c6cee056b2c28d1571a4366152f3']
web_1               | ['0x6da1b24b55a9a55ad53a30c24cf6090fe5c82a07']
web_1               | ['0x9b4c6762b25575ab76a050a5dcacf406b1fdb051']
web_1               | ['0xeefba5763c798ca53d9b3426d900bca1fa45d27f']
web_1               | ['0x4db556d283e1d578db27589cb94e98d0a7c9797f']
```

To run tests and linters:

``` bash
make dc.test
make dc.test_integration
```

Unit tests run without an api-key. I.e. fully mocked from external internet.

But integration tests depend on the real Infura api.

**N.B.** integration tests take a while to find a second ERC-721 contract.
Screen will freeze without any message - it's ok.

## Project structure

```
.
|-- app - actual service code
|   |-- domain - entities in a form of dataclasses without additional of logic
|   |   `-- node_rpc.py - related to ethereum json-rpc api
|   |-- resources - external resources, i.e. databases or api
|   |   `-- node.py - handle http request to infura api
|   |-- usecases - business logic
|   |   |-- block_inspector.py - logic to process one block
|   |   `-- streamer.py - logic to process chain stream
|   |-- app.py - connect all pieces together to run script
|   |-- __main__.py - handle cli
|   |-- schema.py
|   `-- settings.py - parse settings from env files
|-- settings - holds envs and configs in nice structures that easy to use
|   |-- default.conf - common to all stages but could be override if needed
|   |-- local.conf - for local tests
|   |-- prod.conf
|   `-- stage.conf - qa and dev stage
|-- tests
|   |-- files
|   |   `-- infura
|   |       |-- get_by_number.json
|   |       |-- get_estimated_gas_error.json
|   |       |-- get_estimated_gas.json
|   |       |-- get_estimated_gas_rejected.json
|   |       `-- get_transaction_receipt.json
|   |-- integration
|   |   `-- test_usecases.py
|   |-- unit
|   |   `-- test_node_resource.py
|   `-- conftest.py
|-- .env - should be created manually to keep secretes out of git
|-- conftest.py - empty file in the root of the project to handle paths
|-- default.env - common envs for test and dev modes
|-- docker-compose.yml
|-- Dockerfile
|-- flake8.tests.ini - linter rules specified for ./tests python code
|-- Makefile - reusable terminal commands
|-- pyproject.toml - autogenerated by poetry
|-- README.md
|-- setup.cfg
|-- test.env - mocked envs for tests purpose
```

## Future improvements
- [ ] Add logging and logging config in settings
- [ ] Fix case when steam reaching head of blockchain
- [ ] Replace http to websocket
- [ ] Handle unexpected exceptions with retries
- [ ] Create proper fixture to mock external calls to infura assuming concurrency
- [ ] Project structure in README looks ugly. Find a way to make it nice.
