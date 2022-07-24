from app.usecases.block_inspector import find_contracts_in_block
from app.usecases.streamer import stream_rfc_contracts


async def test_block_inspector(http_node_resource, session) -> None:
    finded_contracts = await find_contracts_in_block(
        block_id=13821429, session=session, node_resource=http_node_resource
    )
    assert finded_contracts == ["0xd16bdccae06dfd701a59103446a17e22e9ca0ef0"]


async def test_streamer(http_node_resource, session) -> None:
    finded_lists_of_contracts = []
    async for finded_contracts in stream_rfc_contracts(
        start_block_id=13821429, session=session, node_resource=http_node_resource
    ):
        finded_lists_of_contracts.append(finded_contracts)
        if len(finded_lists_of_contracts) == 3:
            break
    assert finded_lists_of_contracts == [
        ["0xd16bdccae06dfd701a59103446a17e22e9ca0ef0"],
        ["0x0406db8351aa6839169bb363f63c2c808fee8f99"],
        ["0xa7ccd0326757c6cee056b2c28d1571a4366152f3"],
    ]
