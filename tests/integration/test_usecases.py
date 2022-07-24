from app.usecases.block_inspector import find_contracts_in_block


async def test_block_inspector(http_node_resource, session) -> None:
    finded_contracts = []
    async for contract_address in find_contracts_in_block(
        block_id=13821429, session=session, node_resource=http_node_resource
    ):
        finded_contracts.append(contract_address)
    assert finded_contracts == ["0xd16bdccae06dfd701a59103446a17e22e9ca0ef0"]
