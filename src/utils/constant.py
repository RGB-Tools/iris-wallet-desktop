"""This module contains constant variables.
"""
from __future__ import annotations

from src.model.enums.enums_model import NetworkEnumModel

DEFAULT_LOCALE = 'en_IN'
BACKED_URL_LIGHTNING_NETWORK = 'http://127.0.0.1:3001'
ORGANIZATION_NAME = 'rgb'
APP_NAME = 'iriswallet'
ORGANIZATION_DOMAIN = 'com.rgb.iriswallet'
LOG_FILE_MAX_SIZE = 1048576  # 1 mb
LOG_FILE_MAX_BACKUP_COUNT = 5
MNEMONIC_KEY = 'mnemonic'
WALLET_PASSWORD_KEY = 'wallet_password'
LIGHTNING_URL_KEY = 'lightning_network_url'
SAVED_BITCOIND_RPC_USER = 'bitcoind_rpc_username'
SAVED_BITCOIND_RPC_PASSWORD = 'bitcoind_rpc_password'
SAVED_BITCOIND_RPC_HOST = 'bitcoind_rpc_host'
SAVED_BITCOIND_RPC_PORT = 'bitcoind_rpc_port'
SAVED_INDEXER_URL = 'indexer_url'
SAVED_PROXY_ENDPOINT = 'proxy_endpoint'
SAVED_ANNOUNCE_ADDRESS = 'announce_addresses'
SAVED_ANNOUNCE_ALIAS = 'announce_alias'
LDK_PORT_KEY = 'ldk_port'
NODE_PUB_KEY = 'node_pub_key'
NETWORK_KET = 'network'
IS_EMBEDDED_KEY = 'embedded'
IS_REMOTE_KEY = 'remote'
CACHE_FILE_NAME = {
    NetworkEnumModel.MAINNET: 'iris-wallet-cache-mainnet',
    NetworkEnumModel.TESTNET: 'iris-wallet-cache-testnet',
    NetworkEnumModel.TESTNET4: 'iris-wallet-cache-testnet4',
    NetworkEnumModel.REGTEST: 'iris-wallet-cache-regtest',
}
DEFAULT_CACHE_FILENAME = 'iris-wallet-cache-default'
CACHE_FOLDER_NAME = 'cache'
CACHE_EXPIRE_TIMEOUT = 600
REQUEST_TIMEOUT = 120  # In seconds
NO_OF_UTXO = 1
MIN_CONFIRMATION = 1
UTXO_SIZE_SAT = 1000
UTXO_SIZE_SAT_FOR_OPENING_CHANNEL = 32000
MIN_UTXOS_SIZE = 1000
MIN_CAPACITY_SATS = 5506
FEE_RATE_FOR_CREATE_UTXOS = 5
CHANNEL_PUSH_MSAT = 1394000
RGB_INVOICE_DURATION_SECONDS = 86400
MAX_ATTEMPTS_TO_WAIT_FOR_NODE = 15
# each 1 sec so 30 sec wait for to close node successfully
MAX_ATTEMPTS_FOR_CLOSE = 30
NODE_CLOSE_INTERVAL = 1
INTERVAL = 2
MAX_RETRY_REFRESH_API = 3
FEE_RATE = 5
LN_INVOICE_EXPIRY_TIME = 3
LN_INVOICE_EXPIRY_TIME_UNIT = 'Hours'
G_SCOPES = ['https://www.googleapis.com/auth/drive.file']
NATIVE_LOGIN_ENABLED = 'nativeLoginEnabled'
IS_NATIVE_AUTHENTICATION_ENABLED = 'isNativeAuthenticationEnabled'
PRIVACY_POLICY_URL = 'https://iriswallet.com/privacy_policy.html'
TERMS_OF_SERVICE_URL = 'https://iriswallet.com/testnet/terms_of_service.html'
LOG_FOLDER_NAME = 'logs'
LN_BINARY_NAME = 'rgb-lightning-node'
PING_DNS_ADDRESS_FOR_NETWORK_CHECK = '8.8.8.8'
PING_DNS_SERVER_CALL_INTERVAL = 5000

BITCOIND_RPC_USER_REGTEST = 'user'
BITCOIND_RPC_PASSWORD_REGTEST = 'password'
BITCOIND_RPC_HOST_REGTEST = 'regtest-bitcoind.rgbtools.org'
BITCOIND_RPC_PORT_REGTEST = 80
INDEXER_URL_REGTEST = 'electrum.rgbtools.org:50041'
PROXY_ENDPOINT_REGTEST = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
LDK_DATA_NAME_REGTEST = 'dataldkregtest'

BITCOIND_RPC_USER_TESTNET = 'user'
BITCOIND_RPC_PASSWORD_TESTNET = 'password'
BITCOIND_RPC_HOST_TESTNET = 'electrum.iriswallet.com'
BITCOIND_RPC_PORT_TESTNET = 18332
INDEXER_URL_TESTNET = 'ssl://electrum.iriswallet.com:50013'
PROXY_ENDPOINT_TESTNET = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
LDK_DATA_NAME_TESTNET = 'dataldktestnet'

BITCOIND_RPC_USER_TESTNET4 = 'user'
BITCOIND_RPC_PASSWORD_TESTNET4 = 'password'
BITCOIND_RPC_HOST_TESTNET4 = 'electrum.iriswallet.com'
BITCOIND_RPC_PORT_TESTNET4 = 48332
INDEXER_URL_TESTNET4 = 'ssl://electrum.iriswallet.com:50053'
PROXY_ENDPOINT_TESTNET4 = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
LDK_DATA_NAME_TESTNET4 = 'dataldktestnet4'

BITCOIND_RPC_USER_SIGNET = 'user'
BITCOIND_RPC_PASSWORD_SIGNET = 'password'
BITCOIND_RPC_HOST_SIGNET = 'electrum.iriswallet.com'
BITCOIND_RPC_PORT_SIGNET = 18443
INDEXER_URL_SIGNET = 'ssl://electrum.iriswallet.com:50033'
PROXY_ENDPOINT_SIGNET = 'rpcs://proxy.iriswallet.com/0.2/json-rpc'
LDK_DATA_NAME_SIGNET = 'dataldksignet'

BITCOIND_RPC_USER_MAINNET = 'user'
BITCOIND_RPC_PASSWORD_MAINNET = 'password'
BITCOIND_RPC_HOST_MAINNET = 'localhost'
BITCOIND_RPC_PORT_MAINNET = 18447
INDEXER_URL_MAINNET = 'http://127.0.0.1:50003'
PROXY_ENDPOINT_MAINNET = 'http://127.0.0.1:3002/json-rpc'
LDK_DATA_NAME_MAINNET = 'dataldkmainnet'

ANNOUNCE_ADDRESS = 'pub.addr.example.com:9735'
ANNOUNCE_ALIAS = 'nodeAlias'

DAEMON_PORT = 3001
LDK_PORT = 9735

# Block values for fee estimation
SLOW_TRANSACTION_FEE_BLOCKS = 17
MEDIUM_TRANSACTION_FEE_BLOCKS = 7
FAST_TRANSACTION_FEE_BLOCKS = 1

# Faucet urls
rgbRegtestFaucetURLs: list[str] = ['http://127.0.0.1:8081']
rgbTestnetFaucetURLs: list[str] = [
    'https://rgb-faucet.iriswallet.com/testnet-planb2023',
    'https://rgb-faucet.iriswallet.com/testnet-random2023',
]
rgbTestnet4FaucetURLs: list[str] = [
    'https://rgb-faucet.iriswallet.com/testnet4-planb2023',
    'https://rgb-faucet.iriswallet.com/testnet4-random2023',
]
rgbMainnetFaucetURLs: list[str] = [
    'https://rgb-faucet.iriswallet.com/mainnet-random2023',
]

# Faucet api keys
API_KEY_OPERATOR = 'defaultoperatorapikey'
API_KEY = 'defaultapikey'

# Bitcoin explorer url
BITCOIN_EXPLORER_URL = 'https://mempool.space'

# Syncing chain info label timer in milliseconds
SYNCING_CHAIN_LABEL_TIMER = 5000

# Email and github issue url for error report
CONTACT_EMAIL = 'iriswalletdesktop@gmail.com'
GITHUB_ISSUE_LINK = 'https://github.com/RGB-Tools/iris-wallet-desktop/issues/new/choose'

# Translation context key
IRIS_WALLET_TRANSLATIONS_CONTEXT = 'iris_wallet_desktop'

# RGB lightning node commit ID
RGB_LN_COMMIT_ID_KEY = 'rgb_ln_commit_id'
CURRENT_RLN_NODE_COMMIT = 'f37933079be958908ebc7b24c604bd5558d24865'
COMPATIBLE_RLN_NODE_COMMITS = [
    'f37933079be958908ebc7b24c604bd5558d24865',
]

# Directory names used in paths
APP_DIR = 'app'
NODE_DIR = 'node'
