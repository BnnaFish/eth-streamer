from logging import getLogger

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
import marshmallow_dataclass
from yarl import URL

from app.domain.node_rpc import (
    GetBlockByNumberRequest,
    GetBlockByNumberResponse,
    GetTransactionReceiptRequest,
    GetTransactionReceiptResponse,
    TransactionObject,
)
from app.schema import BaseSchema

logger = getLogger(__name__)


get_block_by_number_req_schema = marshmallow_dataclass.class_schema(
    GetBlockByNumberRequest, base_schema=BaseSchema
)()
get_block_by_number_resp_schema = marshmallow_dataclass.class_schema(
    GetBlockByNumberResponse, base_schema=BaseSchema
)()
get_transaction_receipt_req_schema = marshmallow_dataclass.class_schema(
    GetTransactionReceiptRequest, base_schema=BaseSchema
)()
get_transaction_receipt_resp_schema = marshmallow_dataclass.class_schema(
    GetTransactionReceiptResponse, base_schema=BaseSchema
)()


class HTTPNodeResource:
    """
    Req-res http calls via aiohttp session
    """

    def __init__(self, api_key: str, url: str) -> None:
        self._api_key = api_key
        self._url = url

    async def get_block_by_number(
        self, block_id: int, session: ClientSession
    ) -> GetBlockByNumberResponse:
        request = GetBlockByNumberRequest(
            params=(
                hex(
                    block_id,
                ),
                True,
            )
        )
        async with session.post(
            URL(self._url) / self._api_key, json=get_block_by_number_req_schema.dump(request)
        ) as resp:
            try:
                json_reps = await resp.json()
            except ContentTypeError:
                logger.exception("Not json response. Got: %s", await resp.text())
                raise
            return get_block_by_number_resp_schema.load(json_reps)

    async def get_transaction_receipt(
        self, transaction: TransactionObject, session: ClientSession
    ) -> GetBlockByNumberResponse:
        request = GetTransactionReceiptRequest(params=(transaction.hash,))
        async with session.post(
            URL(self._url) / self._api_key, json=get_transaction_receipt_req_schema.dump(request)
        ) as resp:
            try:
                json_reps = await resp.json()
            except ContentTypeError:
                logger.exception("Not json response. Got: %s", await resp.text())
                raise
            return get_transaction_receipt_resp_schema.load(json_reps)
