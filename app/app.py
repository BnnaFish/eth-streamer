from aiohttp import ClientSession

from app.resources.node import HTTPNodeResource
from app.settings import node_config
from app.usecases.streamer import stream_erc_contracts


async def stream_and_print(initial_block_id: int) -> None:
    """
    Build all dependencies and handle callback( just print in our case)
    """
    node_resource = HTTPNodeResource(api_key=node_config.api_key, url=node_config.url)
    async with ClientSession(raise_for_status=True) as session:
        async for discovered_contracts in stream_erc_contracts(  # noqa: WPS352 Found multiline loop
            initial_block_id=initial_block_id, session=session, node_resource=node_resource
        ):
            print(discovered_contracts)  # noqa: WPS421 Found wrong function call: print
