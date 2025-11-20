"""Service module for common operation in application"""
from __future__ import annotations

import src.flavour as bitcoin_network
from src.data.repository.common_operations_repository import CommonOperationRepository
from src.data.repository.setting_repository import SettingRepository
from src.model.common_operation_model import InitRequestModel
from src.model.common_operation_model import InitResponseModel
from src.model.common_operation_model import NetworkInfoResponseModel
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.common_operation_model import UnlockResponseModel
from src.model.enums.enums_model import NetworkEnumModel
from src.model.node_info_model import NodeInfoModel
from src.utils.constant import MNEMONIC_KEY
from src.utils.constant import WALLET_PASSWORD_KEY
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_KEYRING_STORE_NOT_ACCESSIBLE
from src.utils.error_message import ERROR_NETWORK_MISMATCH
from src.utils.error_message import ERROR_UNABLE_GET_MNEMONIC
from src.utils.error_message import ERROR_UNABLE_TO_GET_HASHED_MNEMONIC
from src.utils.handle_exception import handle_exceptions
from src.utils.helpers import check_node
from src.utils.helpers import get_bitcoin_config
from src.utils.helpers import hash_mnemonic
from src.utils.helpers import validate_mnemonic
from src.utils.keyring_storage import set_value


class CommonOperationService:
    """
    The CommonOperationService class provides static methods for managing the initialization
    and unlocking of a wallet within a Lightning Network node environment. It ensures
    that the wallet operates in the correct network context and handles exceptions during these operations.
    """

    @staticmethod
    def initialize_wallet(password: str) -> InitResponseModel:
        """
        Initializes the wallet with the provided password, unlocks it, and verifies
        that the node's network matches the expected network.
        """
        try:
            response: InitResponseModel = CommonOperationRepository.init(
                InitRequestModel(password=password),
            )
            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()
            bitcoin_config = get_bitcoin_config(stored_network, password)
            CommonOperationRepository.unlock(
                bitcoin_config,
            )
            network_info: NetworkInfoResponseModel = CommonOperationRepository.network_info()
            node_network = str.lower(network_info.network)
            if node_network != bitcoin_network.__network__:
                raise CommonException(ERROR_NETWORK_MISMATCH)
            return response
        except Exception as exc:
            return handle_exceptions(exc=exc)

    @staticmethod
    def enter_node_password(password: str) -> UnlockResponseModel:
        """
        Unlocks the wallet with the provided password after ensuring the node is locked,
        and verifies that the node's network matches the expected network.
        """
        try:

            stored_network: NetworkEnumModel = SettingRepository.get_wallet_network()
            bitcoin_config = get_bitcoin_config(stored_network, password)
            status: bool = check_node('unlock_required')
            if not status:
                CommonOperationRepository.lock()
            response: UnlockResponseModel = CommonOperationRepository.unlock(
                bitcoin_config,
            )
            network_info: NetworkInfoResponseModel = CommonOperationRepository.network_info()
            node_network = str.lower(network_info.network)
            if node_network != bitcoin_network.__network__:
                raise CommonException(ERROR_NETWORK_MISMATCH)
            return response
        except Exception as exc:
            return handle_exceptions(exc=exc)

    @staticmethod
    def keyring_toggle_enable_validation(mnemonic: str, password: str):
        """validate keyring enable """
        try:
            network: NetworkEnumModel = SettingRepository.get_wallet_network()
            is_mnemonic_stored = set_value(
                MNEMONIC_KEY, mnemonic, network.value,
            )
            validate_mnemonic(mnemonic_phrase=mnemonic)
            is_password_stored = set_value(
                WALLET_PASSWORD_KEY, password, network.value,
            )
            if is_mnemonic_stored is False or is_password_stored is False:
                raise CommonException(ERROR_KEYRING_STORE_NOT_ACCESSIBLE)
            SettingRepository.set_keyring_status(status=False)
        except Exception as exc:
            handle_exceptions(exc=exc)

    @staticmethod
    def set_node_info():
        """
        Fetch and store node information in the NodeInfoModel.

        This method retrieves the node information from the CommonOperationRepository
        and sets it in the NodeInfoModel for global access. It handles any exceptions
        that may occur during the fetching or setting of the node information and logs
        the error message if something goes wrong.

        Raises:
            Exception: If an error occurs while fetching or setting node information.
        """
        try:
            # Fetch node information from the repository
            # Store node information in the NodeInfoModel
            node_info_model = NodeInfoModel()
            if node_info_model.node_info is None:
                node_info: NodeInfoResponseModel = CommonOperationRepository.node_info()
                node_info_model.set_node_info(data=node_info)

        except Exception as exc:
            # Log and re-raise the exception if something goes wrong
            handle_exceptions(exc=exc)

    @staticmethod
    def get_hashed_mnemonic(mnemonic):
        """This method returns the hashed mnemonic"""
        if not mnemonic:
            raise CommonException(ERROR_UNABLE_GET_MNEMONIC)

        hashed_mnemonic = hash_mnemonic(mnemonic_phrase=mnemonic)

        if not hashed_mnemonic:
            raise CommonException(ERROR_UNABLE_TO_GET_HASHED_MNEMONIC)

        return hashed_mnemonic
