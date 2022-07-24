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
class Error:
    message: str

    @property
    def is_rfc_721(self) -> bool:
        return (
            self.message == "execution reverted: ERC721: transfer caller is not owner nor approved"
        )


@dataclass
class NodeResponse:
    result: Optional[Any] = None
    error: Optional[Error] = None
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
class GetBlockByNumberResult:
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
class TransactionReceipt:
    contract_address: str = field(metadata={"data_key": "contractAddress"})


@dataclass
class GetTransactionReceiptResponse(NodeResponse):
    result: TransactionReceipt


@dataclass
class CallParams:
    from_: str = field(metadata={"data_key": "from"})
    to: str
    data: str


@dataclass
class GetEstimateGasRequest(NodeRequest):
    """
    https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_estimategas
    """

    params: tuple[CallParams]
    method: str = "eth_estimateGas"


@dataclass
class GetEstimateGasErrorResponse(NodeResponse):
    """
    We are interesting only in default error message here
    """


@dataclass
class GetEstimateGasResponse(NodeResponse):
    result: str
