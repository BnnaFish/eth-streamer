import json
from typing import Any, AsyncGenerator

from aiohttp import ClientSession
from aioresponses import aioresponses
from pytest import fixture

from app.resources.node import HTTPNodeResource
from app.settings import node_config


@fixture
async def session() -> AsyncGenerator[ClientSession, None]:
    async with ClientSession(raise_for_status=True) as session:
        yield session


@fixture
def http_node_resource() -> HTTPNodeResource:
    return HTTPNodeResource(api_key=node_config.api_key, url=node_config.url)


@fixture
def get_by_number_json() -> dict[Any, Any]:
    with open("./tests/files/infura/get_by_number.json", "r") as f:
        return json.load(f)


@fixture
def get_transaction_receipt_json() -> dict[Any, Any]:
    with open("./tests/files/infura/get_transaction_receipt.json", "r") as f:
        return json.load(f)


@fixture
def get_estimated_gas_error_json() -> dict[Any, Any]:
    with open("./tests/files/infura/get_estimated_gas_error.json", "r") as f:
        return json.load(f)


@fixture
def get_estimated_gas_json() -> dict[Any, Any]:
    with open("./tests/files/infura/get_estimated_gas.json", "r") as f:
        return json.load(f)


@fixture
def get_estimated_gas_rejected_json() -> dict[Any, Any]:
    with open("./tests/files/infura/get_estimated_gas_rejected.json", "r") as f:
        return json.load(f)


@fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@fixture
def get_by_number_mock(mock_aioresponse, get_by_number_json) -> None:
    mock_aioresponse.post(f"{node_config.url}/{node_config.api_key}", payload=get_by_number_json)


@fixture
def get_transaction_receipt_mock(mock_aioresponse, get_transaction_receipt_json) -> None:
    mock_aioresponse.post(
        f"{node_config.url}/{node_config.api_key}", payload=get_transaction_receipt_json
    )


@fixture
def get_estimated_gas_error_mock(mock_aioresponse, get_estimated_gas_error_json) -> None:
    mock_aioresponse.post(
        f"{node_config.url}/{node_config.api_key}", payload=get_estimated_gas_error_json
    )


@fixture
def get_estimated_gas_mock(mock_aioresponse, get_estimated_gas_json) -> None:
    mock_aioresponse.post(
        f"{node_config.url}/{node_config.api_key}", payload=get_estimated_gas_json
    )


@fixture
def get_estimated_gas_rejected_mock(mock_aioresponse, get_estimated_gas_rejected_json) -> None:
    mock_aioresponse.post(
        f"{node_config.url}/{node_config.api_key}", payload=get_estimated_gas_rejected_json
    )
