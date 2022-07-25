import asyncio

import click

from app.app import stream_and_print

TEST_BLOCK_ID = 13821429


@click.command()
@click.option("--initial_block_id", default=TEST_BLOCK_ID, help="Block id to start with")
def stream_and_print_cmd(initial_block_id):
    asyncio.run(stream_and_print(initial_block_id=initial_block_id))


if __name__ == "__main__":
    stream_and_print_cmd()
