"""Accessible name and description constants"""
# Application name
from __future__ import annotations

from src.model.enums.enums_model import WalletType
from src.utils.constant import APP_NAME

APP1_NAME = 'test_app_1'
APP2_NAME = 'test_app_2'
FIRST_SERVICE = f"{APP_NAME}_{APP1_NAME}"
SECOND_SERVICE = f"{APP_NAME}_{APP2_NAME}"
FIRST_APPLICATION = f"Iris Wallet Regtest {APP1_NAME}"
SECOND_APPLICATION = f"Iris Wallet Regtest {APP2_NAME}"
FIRST_APPLICATION_PATH = f"{APP_NAME}_{APP1_NAME}"
SECOND_APPLICATION_PATH = f"{APP_NAME}_{APP2_NAME}"
FIRST_APPLICATION_URL = 'http://127.0.0.1:3001'
SECOND_APPLICATION_URL = 'http://127.0.0.1:3002'
LN_PORT = '9736'

# Term and condition page
ACCEPT_BUTTON = 'accept_button'
DECLINE_BUTTON = 'decline_button'
TNC_TXT_DESCRIPTION = 'tnc_txt_description'

# Wallet or transfer selection page
OPTION_1_FRAME = 'option_1_frame'
OPTION_2_FRAME = 'option_2_frame'
WALLET_OR_TRANSFER_SELECTION_CLOSE_BUTTON = 'wallet_or_transfer_selection_close_button'
WALLET_OR_TRANSFER_SELECTION_CONTINUE_BUTTON = 'wallet_or_transfer_selection_continue_button'

# Wallet password page
CREATE_BUTTON = 'create_button'
RESTORE_BUTTON = 'restore_button'
SET_WALLET_PASSWORD_CLOSE_BUTTON = 'set_wallet_password_close_button'
SET_WALLET_PASSWORD_PROCEED_BUTTON = 'set_wallet_password_proceed_button'
PASSWORD_VISIBILITY_BUTTON = 'password_visibility_button'
CONFIRM_PASSWORD_VISIBILITY_BUTTON = 'confirm_password_visibility_button'
PASSWORD_INPUT = 'password_input'
CONFIRM_PASSWORD_INPUT = 'confirm_password_input'
PASSWORD_SUGGESTION_BUTTON = 'password_suggestion_button'

# Bitcoin details page
RECEIVE_BITCOIN_BUTTON = 'receive_bitcoin_button'
SEND_BITCOIN_BUTTON = 'send_bitcoin_button'
BITCOIN_CLOSE_BUTTON = 'bitcoin_close_button'
BITCOIN_BALANCE = 'bitcoin_balance'
BITCOIN_SPENDABLE_BALANCE = 'bitcoin_spendable_balance'
BITCOIN_REFRESH_BUTTON = 'bitcoin_refresh_button'

# Receive asset page
RECEIVER_ADDRESS = 'receiver_address'
RECEIVE_ASSET_CLOSE_BUTTON = 'receive_asset_close_button'
INVOICE_COPY_BUTTON = 'address_copy_button'

# Send asset page
ENTER_RECEIVER_ADDRESS = 'enter_receiver_address'
PAY_AMOUNT = 'pay_amount'
SEND_ASSET_CLOSE_BUTTON = 'send_asset_close_button'
SEND_ASSET_REFRESH_BUTTON = 'send_asset_refresh_button'
SEND_ASSET_BUTTON = 'send_asset_button'
ASSET_ADDRESS_VALIDATION_LABEL = 'asset_address_validation_label'

# Issue NIA asset page
ISSUE_NIA_ASSET = 'issue_nia_asset'
ISSUE_NIA_ASSET_CLOSE_BUTTON = 'issue_nia_asset_close_button'
NIA_ASSET_TICKER = 'nia_asset_ticker'
NIA_ASSET_NAME = 'nia_asset_name'
NIA_ASSET_AMOUNT = 'nia_asset_amount'
ISSUE_NIA_BUTTON = 'issue_nia_button'

# Success page
SUCCESS_PAGE_CLOSE_BUTTON = 'success_page_close_button'
SUCCESS_PAGE_HOME_BUTTON = 'success_page_home_button'

# Toaster
TOASTER_CLOSE_BUTTON = 'toaster_close_button'
TOASTER_DESCRIPTION = 'toaster_description'
TOASTER_TITLE = 'toaster_title'
TOASTER_FRAME = 'toaster_frame'

# Sidebar
BACKUP_BUTTON = 'backup_button'
FUNGIBLE_BUTTON = 'fungible_button'
COLLECTIBLE_BUTTON = 'collectible_button'
CHANNEL_MANAGEMENT_BUTTON = 'channel_management_button'
ABOUT_BUTTON = 'about_button'
HELP_BUTTON = 'help_button'
FAUCET_BUTTON = 'faucet_button'
SIDEBAR_RECEIVE_ASSET_BUTTON = 'sidebar_receive_asset_button'
VIEW_UNSPENT_LIST_BUTTON = 'view_unspent_list_button'
SETTINGS_BUTTON = 'settings_button'

# Issue CFA asset page
ISSUE_CFA_ASSET = 'issue_cfa_asset'
ISSUE_CFA_BUTTON = 'issue_cfa_button'
CFA_ASSET_DESCRIPTION = 'cfa_asset_description'
CFA_ASSET_NAME = 'cfa_asset_name'
CFA_ASSET_AMOUNT = 'cfa_asset_amount'
CFA_UPLOAD_FILE_BUTTON = 'cfa_upload_file_button'
ISSUE_CFA_ASSET_CLOSE_BUTTON = 'issue_cfa_asset_close_button'

# File chooser
FILE_CHOOSER = 'file chooser'

# Send LN invoice page
SEND_LN_INVOICE_CLOSE_BUTTON = 'send_ln_invoice_close_button'
LN_INVOICE_INPUT = 'ln_invoice_input'
SEND_LN_INVOICE_BUTTON = 'send_ln_invoice_button'
AMOUNT_VALIDATION_ERROR_LABEL = 'amount_validation_error_label'

# Asset details page
ASSET_SEND_BUTTON = 'asset_send_button'
ASSET_REFRESH_BUTTON = 'asset_refresh_button'
ASSET_CLOSE_BUTTON = 'asset_close_button'
ASSET_ON_CHAIN_TOTAL_BALANCE = 'asset_on_chain_total_balance'
ASSET_ON_CHAIN_SPENDABLE_BALANCE = 'asset_on_chain_spendable_balance'
ASSET_LIGHTNING_TOTAL_BALANCE = 'asset_lightning_total_balance'
ASSET_LIGHTNING_SPENDABLE_BALANCE = 'asset_lightning_spendable_balance'
ASSET_RECEIVE_BUTTON = 'asset_receive_button'
ASSET_AMOUNT_VALIDATION = 'asset_amount_validation'
ASSET_ID_COPY_BUTTON = 'asset_id_copy_button'
TRANSACTION_DETAIL_CLOSE_BUTTON = 'transaction_detail_close_button'
CONFIRMATION_DIALOG_CONTINUE_BUTTON = 'confirmation_dialog_continue_button'
CONFIRMATION_DIALOG_CANCEL_BUTTON = 'confirmation_dialog_cancel_button'
CONFIRMAION_DIALOG = 'confirmation_dialog'

# Asset transaction details page
AMOUNT_VALUE = 'amount_value'
ASSET_TRANSACTION_DETAIL_CLOSE_BUTTON = 'asset_transaction_detail_close_button'
ASSET_TX_ID = 'asset_tx_id'

# Create LN invoice
ASSET_AMOUNT_LN = 'asset_amount_ln'
EXPIRY_TIME = 'expiry_time_ln'
MSAT_AMOUNT = 'msat_amount'
CREATE_LN_INVOICE_BUTTON = 'create_ln_invoice_button'
CREATE_LN_INVOICE_AMOUNT_VALIDATION = 'create_ln_invoice_amount_validation'
CREATE_LN_INVOICE_CLOSE_BUTTON = 'create_ln_invoice_close_button'

# Fee rate
SLOW_CHECKBOX = 'slow_checkbox'
MEDIUM_CHECKBOX = 'medium_checkbox'
FAST_CHECKBOX = 'fast_checkbox'
CUSTOM_CHECKBOX = 'custom_checkbox'
FEE_RATE_INPUT = 'fee_rate_input'

# Bitcoin tx page
BITCOIN_TX_ID = 'bitcoin_tx_id'
BITCOIN_AMOUNT_VALUE = 'bitcoin_amount_value'
BITCOIN_TX_PAGE_CLOSE_BUTTON = 'bitcoin_tx_page_close_button'

# Transaction detail page
BITCOIN_TRANSACTION_DETAIL_FRAME = 'bitcoin_transaction_detail_frame'
RGB_TRANSACTION_DETAIL_ON_CHAIN_FRAME = 'rgb_transaction_detail_on_chain_frame'
RGB_TRANSACTION_DETAIL_LIGHTNING_FRAME = 'rgb_transaction_detail_lightning_frame'
TRANSFER_STATUS = 'transfer_status'

# Channel management page
CREATE_CHANNEL_BUTTON = 'create_channel_button'
CREATE_CHANNEL_CLOSE_BUTTON = 'create_channel_close_button'
NODE_URI_INPUT = 'node_uri_input'
CREATE_CHANNEL_ERROR_LABEL = 'create_channel_error_label'
CHANNEL_NEXT_BUTTON = 'channel_next_button'
CHANNEL_PREV_BUTTON = 'channel_prev_button'
CHANNEL_COMBOBOX = 'channel_combo_box'
CHANNEL_CAPACITY_SAT = 'channel_capacity_sat'
CHANNEL_ASSET_AMOUNT = 'channel_asset_amount'
PUSH_MSAT_VALUE = 'push_msat_value'
CHANNEL_STATUS = 'channel_status'

# Channel detail page
CHANNEL_DETAIL_DIALOG = 'channel_detail_dialog'
CHANNEL_DETAIL_CLOSE_BUTTON = 'channel_detail_close_button'
CLOSE_CHANNEL_BUTTON = 'close_channel_button'
CHANNEL_PEER_PUBKEY_COPY_BUTTON = 'channel_peer_pubkey_copy_button'
CLOSE_CHANNEL_CONTINUE_BUTTON = 'close_channel_continue_button'
CLOSE_CHANNEL_DIALOG = 'close_channel_dialog'
BTC_LOCAL_VALUE_LABEL = 'btc_local_value_label'
BTC_REMOTE_VALUE_LABEL = 'btc_remote_value_label'


# About page
ANNOUNCE_ADDRESS_ACCESSIBLE_DESCRIPTION = 'announce_address'
ANNOUNCE_ALIAS_ACCESSIBLE_DESCRIPTION = 'announce_alias'
NODE_PUBKEY_COPY_BUTTON = 'node_pubkey_copy_button'
LN_PEER_LISTENING_PORT_COPY_BUTTON = 'ln_peer_listening_port_copy_button'
INDEXER_URL_ACCESSIBLE_DESCRIPTION = 'indexer_url'
RGB_PROXY_URL_ACCESSIBLE_DESCRIPTION = 'rgb_proxy_url'
NODE_PUBKEY_ACCESSIBLE_DESCRIPTION = 'node_pubkey'
LN_PEER_LISTENING_PORT_ACCESSIBLE_DESCRIPTION = 'ln_peer_listening_port'
BITCOIND_HOST_ACCESSIBLE_DESCRIPTION = 'bitcoind_host'
BITCOIND_PORT_ACCESSIBLE_DESCRIPTION = 'bitcoind_port'
BITCOIND_HOST_COPY_BUTTON = 'bitcoind_host_copy_button'
BITCOIND_PORT_COPY_BUTTON = 'bitcoind_port_copy_button'
INDEXER_URL_COPY_BUTTON = 'indexer_url_copy_button'
RGB_PROXY_URL_COPY_BUTTON = 'rgb_proxy_url_copy_button'
ANNOUNCE_ADDRESS_COPY_BUTTON = 'announce_address_copy_button'
ANNOUNCE_ALIAS_COPY_BUTTON = 'announce_alias_copy_button'
DOWNLOAD_DEBUG_LOG = 'download_debug_log'

# Settings page
ASK_AUTH_FOR_IMPORTANT_QUESTION = 'auth_for_imp_question'
ASK_AUTH_FOR_APP_LOGIN = 'ask_auth_for_app_login'
HIDE_EXHAUSTED_ASSETS = 'hide_exhausted_assets'
KEYRING_STORAGE = 'keyring_storage'
SET_DEFAULT_FEE_RATE = 'set_default_fee_rate'
SET_DEFAULT_EXP_TIME = 'set_default_exp_time'
SET_DEFAULT_MIN_EXPIRATION = 'set_min_confirmation'
SPECIFY_INDEXER_URL = 'specify_indexer_url'
SPECIFY_RGB_PROXY_URL = 'specify_rgb_proxy_url'
SPECIFY_BITCOIND_HOST = 'specify_bitcoind_host'
SPECIFY_BITCOIND_PORT = 'specify_bitcoind_port'
SPECIFY_ANNOUNCE_ADD = 'specify_announce_add'
SPECIFY_ANNOUNCE_ALIAS = 'specify_announce_alias'
EXPIRY_TIME_COMBO_BOX = 'expiry_time_combo_box'
INPUT_BOX_NAME = 'input_box'
KEYRING_TOGGLE_BUTTON = 'keyring_toggle_button'
ASK_AUTH_FOR_APP_LOGIN_TOGGLE = 'ask_auth_for_app_login_toggle'
ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE = ''
HIDE_EXHAUSTED_ASSETS_TOGGLE = ''

# View unspent list page
UNSPENT_UTXO_ASSET_ID = 'unspent_utxo_asset_id'
UNSPENT_WIDGET = 'unspent_widget'
UNSPENT_CLICKABLE_FRAME = 'unspent_clickable_frame'
UNSPENT_UTXO_OUTPOINT = 'unspent_utxo_outpoint'

# LN endpoint page
LN_NODE_URL = 'ln_node_url'
PROCEED_BUTTON = 'proceed_button'
LN_ENDPOINT_CLOSE_BUTTON = 'ln_endpoint_close_button'

# Backup page
BACKUP_CLOSE_BUTTON = 'backup_close_button'
SHOW_MNEMONIC_BUTTON = 'show_mnemonic_button'
CONFIGURE_BACKUP_BUTTON = 'configure_backup_button'
BACKUP_WINDOW = 'backup_window'
BACKUP_NODE_DATA_BUTTON = 'backup_node_data_button'
MNEMONIC_FRAME = 'mnemonic_frame'

# Keyring dialog box
KEYRING_DIALOG_BOX = 'keyring_dialog_box'
KEYRING_MNEMONICS_FRAME = 'keyring_mnemonics_frame'
KEYRING_MNEMONIC_COPY_BUTTON = 'keyring_copy_button'
KEYRING_PASSWORD_FRAME = 'keyring_password_frame'
KEYRING_PASSWORD_COPY_BUTTON = 'keyring_password_copy_button'
KEYRING_PASSWORD_VALUE_LABEL = 'keyring_password_value_label'
KEYRING_MNEMONIC_VALUE_LABEL = 'keyring_mnemonic_value_label'
KEYRING_CONTINUE_BUTTON = 'keyring_continue_button'
KEYRING_CANCEL_BUTTON = 'keyring_cancel_button'
SAVE_CREDENTIALS_CHECK_BOX = 'save_credentials_check_box'

# Restore dialog box
RESTORE_DIALOG_BOX = 'restore_dialog_box'
RESTORE_MNEMONIC_INPUT = 'restore_mnemonic_input'
RESTORE_PASSWORD_INPUT = 'restore_password_input'
RESTORE_CONTINUE_BUTTON = 'restore_continue_button'

# Enter wallet password
ENTER_WALLET_PASSWORD = 'enter_wallet_password'
LOGIN_BUTTON = 'login_button'

# Header frame
NETWORK_AND_BACKUP_FRAME = 'network_and_backup_frame'
KEYRING_TOGGLE_BUTTON = 'keyring_toggle_button'
HIDE_EXHAUSTED_ASSETS_TOGGLE = 'hide_exhausted_assets_toggle'
ASK_AUTH_FOR_IMPORTANT_QUESTION_TOGGLE = 'ask_auth_for_important_question_toggle'
ASK_AUTH_FOR_APP_LOGIN_TOGGLE = 'ask_auth_for_app_login_toggle'

# Keyring dialog box
KEYRING_DIALOG_BOX = 'keyring_dialog_box'
KEYRING_MNEMONICS_FRAME = 'keyring_mnemonics_frame'
KEYRING_COPY_BUTTON = 'keyring_copy_button'
KEYRING_PASSWORD_FRAME = 'keyring_password_frame'
KEYRING_PASSWORD_COPY_BUTTON = 'keyring_password_copy_button'
KEYRING_PASSWORD_VALUE_LABEL = 'keyring_password_value_label'
KEYRING_MNEMONIC_VALUE_LABEL = 'keyring_mnemonic_value_label'


# Fungibles page
FUNGIBLES_SCROLL_WIDGETS = 'fungibles_scroll_widget'

# Help page
HELP_CARD_TITLE_ACCESSIBLE_DESCRIPTION = 'help_card_title'

# Keyring password
FIRST_SERVICE = 'iriswallet_test_app_1'
NATIVE_AUTH_ENABLE = 'isNativeAuthenticationEnabled_test_app_1'


# Test values used in tests
TEST_ANNOUNCE_ADDRESS = 'example.url.com:2222'
TEST_ANNOUNCE_ALIAS = 'testAlias'

# Default wallet modes
DEFAULT_WALLET_MODES = [
    WalletType.EMBEDDED_TYPE_WALLET.value, WalletType.REMOTE_TYPE_WALLET.value,
]
