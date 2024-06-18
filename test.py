from ether.client import Web3Client
from ether.abis import erc20


if __name__ == "__main__":
    cli = (
        Web3Client["arb"]
        .with_account("")
        .with_argus("0x1B690a5D0Bbd1bDbD013DF13611dAec90EE4Af0c")
    )
    usdt = cli.eth.contract("0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9", abi=erc20)
    tx = usdt.functions.transfer(
        "0x21b78Bc5c584eD0974b1581bc9192CAe3937462D", 1000000
    ).transact()
    print("tx", tx)
