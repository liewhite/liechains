from eth_account import Account
from web3 import Web3
from ether.chains import configs
from ether.utils import random_account
from web3.middleware import construct_sign_and_send_raw_middleware,geth_poa_middleware 


from ether.ws import WsClient
from ether.flashbots import flashbot
from ether.mev import providers


class Meta(type):
    def __getitem__(self, arg):
        return Web3Client(chain_config=configs[arg])


class Web3Client(Web3, metaclass=Meta):
    def __init__(
        self, chain_config=configs["ethereum"], pk=None, request_kwargs=None
    ) -> None:
        super().__init__(
            Web3.HTTPProvider(
                chain_config["node"]["rpc"], request_kwargs=request_kwargs
            )
        )
        # bsc
        if chain_config.get('is_poa'):
            self.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.config = chain_config
        self.w3 = self
        if pk:
            self.with_account(pk)

    def with_account(self, private_key: str):
        self.acc = self.eth.account.from_key(private_key)
        self.middleware_onion.add(construct_sign_and_send_raw_middleware(self.acc))
        self.eth.default_account = self.acc.address
        return self

    def with_mev(self, blox_token: str):
        rk = random_account()
        signer = Account.from_key(rk.key)
        flashbot(self, signer, blox_token, providers)
        return self

    def nonce(self):
        return self.eth.get_transaction_count(self.acc.address)

    def subscribe_txs(self):
        return WsClient(self.config["node"]["ws"], ["newPendingTransactions", True])

    def subscribe_blocks(self):
        return WsClient(self.config["node"]["ws"], ["newHeads"])

    def subscribe_logs(self, address=None, topics=[]):
        return WsClient(
            self.config["node"]["ws"], ["logs", {"address": address, "topics": topics}]
        )

if __name__ =="__main__":
    print(Web3Client['ethereum'])