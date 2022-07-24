# flake8: noqa WPS110 Found wrong variable name: params
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class NodeRequest:
    params: tuple[Any, ...]
    method: str
    jsonrpc: str = "2.0"
    id: int = 1


@dataclass
class NodeResponseResult:
    """
    Base class for results
    """


@dataclass
class NodeResponse:
    result: Optional[NodeResponseResult]
    jsonrpc: str = "2.0"
    id: int = 1


@dataclass
class GetBlockByNumberRequest(NodeRequest):
    """
    https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_getblockbynumber
    """

    params: tuple[str, bool]  # block number and flag to return full transaction objects
    method: str = "eth_getBlockByNumber"


@dataclass
class TransactionObject:
    to: Optional[str]
    hash: str


@dataclass
class GetBlockByNumberResult(NodeResponseResult):
    """
    Ommiting everything except transactions for simplisity in test project
    """

    transactions: list[TransactionObject]


@dataclass
class GetBlockByNumberResponse(NodeResponse):
    result: GetBlockByNumberResult


@dataclass
class GetTransactionReceiptRequest(NodeRequest):
    """
    https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_gettransactionreceipt
    """

    params: tuple[str]  # transaction_hash
    method: str = "eth_getTransactionReceipt"


@dataclass
class TransactionReceipt(NodeResponseResult):
    contract_address: str = field(metadata={"data_key": "contractAddress"})


@dataclass
class GetTransactionReceiptResponse(NodeResponse):
    result: TransactionReceipt
