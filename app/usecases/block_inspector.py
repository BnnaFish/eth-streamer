"""
Main code with logic to find ERC-721 contracts

Flow is follow:
1) get block data with all transactions
2) keep only those with "to" is null. It's a marker of contract created
3) take transactions hash and fetch its receipt
4) get contract address from receipt
5) then we should inspect if the contract support ERC-721 methods by calling estimatedGas
6) if a certain error returns - that's what we are looking for. Cause we are not owners
7) if method rejected then we assume it's never exists
8) print result and loop to #1
"""
import asyncio

from aiohttp import ClientSession

from app.resources.node import HTTPNodeResource


async def is_implementing_erc(
    contract_address: str, node_resource: HTTPNodeResource, session: ClientSession
) -> bool:
    """
    Inspect all necessary methods that should exist in contract to support rfc
    """
    # safeTransferFrom
    having_safe_transfer_from = await node_resource.get_estimated_gas_transfer_from(
        contract_address=contract_address, session=session
    )
    if having_safe_transfer_from is None or not having_safe_transfer_from.error.is_erc_721:  # type: ignore
        return False

    # ownerOf
    having_owned_of = await node_resource.get_estimated_gas_owner_of(
        contract_address=contract_address, session=session
    )
    if having_owned_of is None:
        return False

    # balancedOf
    having_balanced_of = await node_resource.get_estimated_gas_balance_of(
        contract_address=contract_address, session=session
    )
    return having_balanced_of is not None


async def find_contracts_in_block(
    block_id: int, node_resource: HTTPNodeResource, session: ClientSession
) -> list[str]:
    """
    Return all hashes of rpc-721 contracts for a given block if any

    Done in async generator style to provide streaming
    Batch requests done concurrently but steps of pipeline are still sequential

    Everything may be done concurrently via async queues
    but with significant code complexity overhead
    """
    transactions_resp = await node_resource.get_block_by_number(block_id=block_id, session=session)
    only_created_transactions = tuple(
        filter(lambda trns: trns.to is None, transactions_resp.result.transactions)
    )
    if not only_created_transactions:
        return []

    get_contract_address_tasks = [
        node_resource.get_transaction_receipt(transaction=trns, session=session)
        for trns in only_created_transactions
    ]
    contract_address_responses = await asyncio.gather(*get_contract_address_tasks)

    # boolean mask to filter by index
    interface_mask_tasks = [
        is_implementing_erc(
            contract_address=resp.result.contract_address,
            node_resource=node_resource,
            session=session,
        )
        for resp in contract_address_responses
    ]
    interface_mask = await asyncio.gather(*interface_mask_tasks)

    discovered_contracts = []
    for idx, resp in enumerate(contract_address_responses):
        if interface_mask[idx]:
            discovered_contracts.append(resp.result.contract_address)
    return discovered_contracts
