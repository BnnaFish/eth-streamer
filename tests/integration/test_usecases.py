from app.usecases.block_inspector import find_contracts_in_block
from app.usecases.streamer import stream_erc_contracts


async def test_block_inspector(http_node_resource, session) -> None:
    discovered_contracts = await find_contracts_in_block(
        block_id=13821429, session=session, node_resource=http_node_resource
    )
    assert discovered_contracts == ["0xd16bdccae06dfd701a59103446a17e22e9ca0ef0"]


async def test_streamer(http_node_resource, session) -> None:
    discovered_lists_of_contracts = []
    stream = stream_erc_contracts(
        initial_block_id=13821429, session=session, node_resource=http_node_resource
    )

    async for discovered_contracts in stream:
        discovered_lists_of_contracts.append(discovered_contracts)
        if len(discovered_lists_of_contracts) == 3:
            break
    assert discovered_lists_of_contracts == [
        ["0xd16bdccae06dfd701a59103446a17e22e9ca0ef0"],
        ["0x0406db8351aa6839169bb363f63c2c808fee8f99"],
        ["0xa7ccd0326757c6cee056b2c28d1571a4366152f3"],
    ]
