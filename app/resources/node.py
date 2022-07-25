from typing import Optional

from aiohttp import ClientSession
import marshmallow_dataclass
from yarl import URL

from app.domain import node_rpc
from app.schema import BaseSchema

get_block_by_number_req_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetBlockByNumberRequest, base_schema=BaseSchema
)()
get_block_by_number_resp_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetBlockByNumberResponse, base_schema=BaseSchema
)()
get_transaction_receipt_req_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetTransactionReceiptRequest, base_schema=BaseSchema
)()
get_transaction_receipt_resp_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetTransactionReceiptResponse, base_schema=BaseSchema
)()
get_estimate_gas_req_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetEstimateGasRequest, base_schema=BaseSchema
)()
get_estimate_gas_error_resp_schema = marshmallow_dataclass.class_schema(
    node_rpc.GetEstimateGasErrorResponse, base_schema=BaseSchema
)()
node_response_schema = marshmallow_dataclass.class_schema(
    node_rpc.NodeResponse, base_schema=BaseSchema
)()


class HTTPNodeResource:
    """
    Req-res http calls via aiohttp session to json-rpc ethereum
    Main purpose: serialize dataclasses to proper rpc data and deserialize back responses

    ClientSession object may be stored in __init__ without passing to each method
    but then async context manager should be created
    and someone else deligated to manage this object livecircle
    """

    def __init__(self, api_key: str, url: str) -> None:
        self._api_key = api_key
        self._url = url

    async def get_block_by_number(
        self, block_id: int, session: ClientSession
    ) -> node_rpc.GetBlockByNumberResponse:
        request = node_rpc.GetBlockByNumberRequest(
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
            json_reps = await resp.json()
            return get_block_by_number_resp_schema.load(json_reps)

    async def get_transaction_receipt(
        self, transaction: node_rpc.TransactionObject, session: ClientSession
    ) -> node_rpc.GetTransactionReceiptResponse:
        request = node_rpc.GetTransactionReceiptRequest(params=(transaction.hash,))
        async with session.post(
            URL(self._url) / self._api_key, json=get_transaction_receipt_req_schema.dump(request)
        ) as resp:
            json_reps = await resp.json()
            return get_transaction_receipt_resp_schema.load(json_reps)

    async def get_estimated_gas_transfer_from(
        self, contract_address: str, session: ClientSession
    ) -> Optional[node_rpc.GetEstimateGasErrorResponse]:
        """
        ad-hoc request with hardcoded data
        not for wildcard purpose

        excpecting an error returned that address is not an owner
        it meens that method exist in contract
        """
        some_random_address = "0xE052113bd7D7700d623414a0a4585BCaE754E9d5"
        # generated once using https://abi.hashex.org/
        # safeTransferFrom with two random addresses and random token
        rpc_data = "0x42842e0e000000000000000000000000e052113bd7d7700d623414a0a4585bcae754e9d500000000000000000000000022407b385e0f464f166f1f05abcd015278192e9e0000000000000000000000000000000000000000000000000000000000000001"
        rpc_params = node_rpc.CallParams(
            from_=some_random_address, to=contract_address, data=rpc_data
        )
        request = node_rpc.GetEstimateGasRequest(params=(rpc_params,))

        async with session.post(
            URL(self._url) / self._api_key, json=get_estimate_gas_req_schema.dump(request)
        ) as resp:
            json_reps = await resp.json()
            if "result" in json_reps:
                return None
            return get_estimate_gas_error_resp_schema.load(json_reps)

    async def get_estimated_gas_owner_of(
        self, contract_address: str, session: ClientSession
    ) -> Optional[node_rpc.NodeResponse]:
        """
        ad-hoc request with hardcoded data
        not for wildcard purpose

        if transaction reverted then method dont exist
        """
        some_random_address = "0xE052113bd7D7700d623414a0a4585BCaE754E9d5"
        # generated once using https://abi.hashex.org/
        # ownerOf 1
        rpc_data = "0x6352211e0000000000000000000000000000000000000000000000000000000000000001"
        rpc_params = node_rpc.CallParams(
            from_=some_random_address, to=contract_address, data=rpc_data
        )
        request = node_rpc.GetEstimateGasRequest(params=(rpc_params,))

        async with session.post(
            URL(self._url) / self._api_key, json=get_estimate_gas_req_schema.dump(request)
        ) as resp:
            json_reps = await resp.json()
            if "error" in json_reps and json_reps["error"]["message"] == "execution reverted":
                return None
            return node_response_schema.load(json_reps)

    async def get_estimated_gas_balance_of(
        self, contract_address: str, session: ClientSession
    ) -> Optional[node_rpc.NodeResponse]:
        """
        ad-hoc request with hardcoded data
        not for wildcard purpose

        if transaction reverted then method dont exist
        """
        some_random_address = "0xE052113bd7D7700d623414a0a4585BCaE754E9d5"
        # generated once using https://abi.hashex.org/
        # balanceOf 0xE052113bd7D7700d623414a0a4585BCaE754E9d5
        rpc_data = "70a08231000000000000000000000000e052113bd7d7700d623414a0a4585bcae754e9d5"
        rpc_params = node_rpc.CallParams(
            from_=some_random_address, to=contract_address, data=rpc_data
        )
        request = node_rpc.GetEstimateGasRequest(params=(rpc_params,))

        async with session.post(
            URL(self._url) / self._api_key, json=get_estimate_gas_req_schema.dump(request)
        ) as resp:
            json_reps = await resp.json()
            if "error" in json_reps and json_reps["error"]["message"] == "execution reverted":
                return None
            return node_response_schema.load(json_reps)
