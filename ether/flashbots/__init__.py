from typing import Union, Optional

from eth_account.signers.local import LocalAccount
from eth_typing import URI
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3._utils.module import attach_modules

from .flashbots import Flashbots
from .middleware import construct_flashbots_middleware
from .provider import FlashbotProvider

DEFAULT_FLASHBOTS_RELAY = "https://relay.flashbots.net"


def flashbot(
    w3: Web3,
    signature_account: LocalAccount,
):
    """
    Injects the flashbots module and middleware to w3.
    """

    flashbots_provider = FlashbotProvider(signature_account, DEFAULT_FLASHBOTS_RELAY)

    flash_middleware = construct_flashbots_middleware(flashbots_provider)
    w3.middleware_onion.add(flash_middleware)

    # attach modules to add the new namespace commands
    attach_modules(w3, {"flashbots": (Flashbots,)})
