from web3 import Web3
from ether.client import Web3Client
from ether.dex.balancer import Balancer
from ether.dex.limit_order import get_quotes
from ether.dex.univ3 import Univ3Swap
from ether.middlewares.remote_signer import RemoteSigner
from rlp import encode
from web3.types import *
from ether.dex.univ2 import *


if __name__ == "__main__":
    # cli = Web3Client["local"].with_account('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
    # v2 = Univ2Swap(
    #     cli,
    #     "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    #     "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    #     "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    #     "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    # )
    # print(v2.quote(10 ** 18))
    # print(v2.swap(10 ** 18, 0).hex())

    cli = Web3Client["local"].with_account(
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    )
    dex = Balancer(cli, cli.to_checksum_address('0xba12222222228d8ba445958a75a0704d566bf2c8'),'0x596192bb6e41802428ac943d2f1476c1af25cc0e000000000000000000000659', '0xbf5495Efe5DB9ce00f80364C8B423567e58d2110')
    amount_out = dex.quote(10 ** 18)
    dex.swap(10 ** 18, amount_out-1)


    # cli = Web3Client["local"].with_account('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
    # v3 = Univ3Swap(
    #     cli,
    #     "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    #     "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    #     "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
    #     "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    #     "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    #     3000
    # )
    # dex, amount_price = get_quotes([v3], 250000000000000000000, 0, 100 * 10 ** 18)[0]
    # print(dex.swap(amount_price[0],0).hex())

    # print(v3.quote(10 ** 18))
    # print(v3.swap(10 ** 18, 0).hex())