import json
import time
from web3 import Web3
from ether.client import Web3Client
from ether.dex.swap import Swap

abi = json.loads(
    """[
    {
        "inputs": [
            {
                "internalType": "contract IAuthorizer",
                "name": "authorizer",
                "type": "address"
            },
            {
                "internalType": "contract IWETH",
                "name": "weth",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "pauseWindowDuration",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "bufferPeriodDuration",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "contract IAuthorizer",
                "name": "newAuthorizer",
                "type": "address"
            }
        ],
        "name": "AuthorizerChanged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "ExternalBalanceTransfer",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "contract IFlashLoanRecipient",
                "name": "recipient",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "feeAmount",
                "type": "uint256"
            }
        ],
        "name": "FlashLoan",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "int256",
                "name": "delta",
                "type": "int256"
            }
        ],
        "name": "InternalBalanceChanged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "bool",
                "name": "paused",
                "type": "bool"
            }
        ],
        "name": "PausedStateChanged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "liquidityProvider",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            },
            {
                "indexed": false,
                "internalType": "int256[]",
                "name": "deltas",
                "type": "int256[]"
            },
            {
                "indexed": false,
                "internalType": "uint256[]",
                "name": "protocolFeeAmounts",
                "type": "uint256[]"
            }
        ],
        "name": "PoolBalanceChanged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "assetManager",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "int256",
                "name": "cashDelta",
                "type": "int256"
            },
            {
                "indexed": false,
                "internalType": "int256",
                "name": "managedDelta",
                "type": "int256"
            }
        ],
        "name": "PoolBalanceManaged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "poolAddress",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "enum IVault.PoolSpecialization",
                "name": "specialization",
                "type": "uint8"
            }
        ],
        "name": "PoolRegistered",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "RelayerApprovalChanged",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "tokenIn",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "contract IERC20",
                "name": "tokenOut",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            }
        ],
        "name": "Swap",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": false,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            }
        ],
        "name": "TokensDeregistered",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "indexed": false,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            },
            {
                "indexed": false,
                "internalType": "address[]",
                "name": "assetManagers",
                "type": "address[]"
            }
        ],
        "name": "TokensRegistered",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "WETH",
        "outputs": [
            {
                "internalType": "contract IWETH",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IVault.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "poolId",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetInIndex",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetOutIndex",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct IVault.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]"
            },
            {
                "internalType": "contract IAsset[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool"
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple"
            },
            {
                "internalType": "int256[]",
                "name": "limits",
                "type": "int256[]"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "batchSwap",
        "outputs": [
            {
                "internalType": "int256[]",
                "name": "assetDeltas",
                "type": "int256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            }
        ],
        "name": "deregisterTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "address payable",
                "name": "recipient",
                "type": "address"
            },
            {
                "components": [
                    {
                        "internalType": "contract IAsset[]",
                        "name": "assets",
                        "type": "address[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "minAmountsOut",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IVault.ExitPoolRequest",
                "name": "request",
                "type": "tuple"
            }
        ],
        "name": "exitPool",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IFlashLoanRecipient",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            },
            {
                "internalType": "bytes",
                "name": "userData",
                "type": "bytes"
            }
        ],
        "name": "flashLoan",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "selector",
                "type": "bytes4"
            }
        ],
        "name": "getActionId",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAuthorizer",
        "outputs": [
            {
                "internalType": "contract IAuthorizer",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getDomainSeparator",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            }
        ],
        "name": "getInternalBalance",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "balances",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            }
        ],
        "name": "getNextNonce",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPausedState",
        "outputs": [
            {
                "internalType": "bool",
                "name": "paused",
                "type": "bool"
            },
            {
                "internalType": "uint256",
                "name": "pauseWindowEndTime",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "bufferPeriodEndTime",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            }
        ],
        "name": "getPool",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "enum IVault.PoolSpecialization",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address"
            }
        ],
        "name": "getPoolTokenInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "cash",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "managed",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "lastChangeBlock",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "assetManager",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            }
        ],
        "name": "getPoolTokens",
        "outputs": [
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "balances",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256",
                "name": "lastChangeBlock",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getProtocolFeesCollector",
        "outputs": [
            {
                "internalType": "contract ProtocolFeesCollector",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            }
        ],
        "name": "hasApprovedRelayer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "components": [
                    {
                        "internalType": "contract IAsset[]",
                        "name": "assets",
                        "type": "address[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "maxAmountsIn",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IVault.JoinPoolRequest",
                "name": "request",
                "type": "tuple"
            }
        ],
        "name": "joinPool",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "enum IVault.PoolBalanceOpKind",
                        "name": "kind",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "poolId",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "contract IERC20",
                        "name": "token",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IVault.PoolBalanceOp[]",
                "name": "ops",
                "type": "tuple[]"
            }
        ],
        "name": "managePoolBalance",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "enum IVault.UserBalanceOpKind",
                        "name": "kind",
                        "type": "uint8"
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "asset",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address"
                    }
                ],
                "internalType": "struct IVault.UserBalanceOp[]",
                "name": "ops",
                "type": "tuple[]"
            }
        ],
        "name": "manageUserBalance",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IVault.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "poolId",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetInIndex",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetOutIndex",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct IVault.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]"
            },
            {
                "internalType": "contract IAsset[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool"
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple"
            }
        ],
        "name": "queryBatchSwap",
        "outputs": [
            {
                "internalType": "int256[]",
                "name": "",
                "type": "int256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IVault.PoolSpecialization",
                "name": "specialization",
                "type": "uint8"
            }
        ],
        "name": "registerPool",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32"
            },
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]"
            },
            {
                "internalType": "address[]",
                "name": "assetManagers",
                "type": "address[]"
            }
        ],
        "name": "registerTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IAuthorizer",
                "name": "newAuthorizer",
                "type": "address"
            }
        ],
        "name": "setAuthorizer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "paused",
                "type": "bool"
            }
        ],
        "name": "setPaused",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "setRelayerApproval",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "poolId",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "enum IVault.SwapKind",
                        "name": "kind",
                        "type": "uint8"
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "assetIn",
                        "type": "address"
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "assetOut",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct IVault.SingleSwap",
                "name": "singleSwap",
                "type": "tuple"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "sender",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool"
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool"
                    }
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "limit",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swap",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountCalculated",
                "type": "uint256"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]"""
)

_router = Web3.to_checksum_address("0xba12222222228d8ba445958a75a0704d566bf2c8")
_pool = Web3.to_bytes(
    hexstr="0x596192bb6e41802428ac943d2f1476c1af25cc0e000000000000000000000659"
)

class Balancer(Swap):
    def __init__(self, w3: Web3Client, router_addr, pool_id, token_out) -> None:
        self.cli = w3
        self.router = w3.eth.contract(router_addr, abi=abi)
        self.pool_id = pool_id
        self.token_in = '0x0000000000000000000000000000000000000000'
        self.token_out = token_out
        self.sender = w3.acc.address

    def quote(self, amount_in) -> int:
        """
        根据token和amount_in报价
        各协议各自实现
        """
        return self.router.functions.swap(
            (self.pool_id, 0, self.token_in, self.token_out, amount_in, b""),
            (self.sender, False, self.sender, False),
            0,
            int(time.time()) + 3600,
        ).call({"from": self.sender, "value": amount_in})
    
    def swap(self, amount_in, min_amount_out):
        """
        执行swap
        """
        return self.router.functions.swap(
            (self.pool_id, 0, self.token_in, self.token_out, amount_in, b""),
            (self.sender, False, self.sender, False),
            min_amount_out,
            int(time.time()) + 3600,
        ).transact({"from": self.sender, "value": amount_in})

def swap_quote(
    w3: Web3,
    sender: str,
    tokenout,
    pool_id,
    amount_in,
    min_amount_out,
    timeout=30,
    router=_router,
    tokenin="0x0000000000000000000000000000000000000000",
) -> int:
    contract = w3.eth.contract(router, abi=abi)
    return contract.functions.swap(
        (pool, 0, tokenin, tokenout, amount_in, b""),
        (sender, False, sender, False),
        min_amount_out,
        int(time.time()) + timeout,
    ).call({"from": sender, "value": amount_in})


def swap(
    w3: Web3,
    sender: str,
    tokenout,
    amount_in,
    min_amount_out,
    timeout=30,
    router=_router,
    pool=_pool,
    tokenin="0x0000000000000000000000000000000000000000",
):
    """
    根据参数组装出交易的input
    """
    contract = w3.eth.contract(router, abi=abi)
    return contract.functions.swap(
        (pool, 0, tokenin, tokenout, amount_in, b""),
        (sender, False, sender, False),
        min_amount_out,
        int(time.time()) + timeout,
    ).transact(
        {
            "from": sender,
            "value": amount_in,
        }
    )


if __name__ == "__main__":
    cli = Web3Client["local"].with_account(
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    )

    print(
        swap_quote(
            cli,
            cli.acc.address,
            "0xbf5495Efe5DB9ce00f80364C8B423567e58d2110",
            10**22,
            0,
        )
    )
