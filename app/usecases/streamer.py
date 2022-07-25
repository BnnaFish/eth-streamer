from collections.abc import AsyncGenerator
from itertools import count

from aiohttp import ClientSession

from app.resources.node import HTTPNodeResource
from app.usecases.block_inspector import find_contracts_in_block


async def stream_erc_contracts(
    initial_block_id: int, session: ClientSession, node_resource: HTTPNodeResource
) -> AsyncGenerator[list[str], None]:
    """
    Infinity generator from initial_block_id
    Yield list of erc-721 contracts if any
    """
    counter = count(initial_block_id)
    for block_id in counter:
        discovered_contracts = await find_contracts_in_block(
            block_id=block_id, node_resource=node_resource, session=session
        )
        if discovered_contracts:
            yield discovered_contracts
