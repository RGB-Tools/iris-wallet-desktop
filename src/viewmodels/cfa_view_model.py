# pylint: disable=too-many-instance-attributes
# mypy: ignore-errors
"""This module contains the CFADetailViewModel class, which represents the view model
for the Bitcoin page activities.
"""
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.rgb_repository import RgbRepository
from src.data.repository.setting_repository import SettingRepository
from src.data.service.asset_detail_page_services import AssetDetailPageService
from src.model.enums.enums_model import AssetType
from src.model.enums.enums_model import AssignmentEnumModel
from src.model.enums.enums_model import NativeAuthType
from src.model.enums.enums_model import ToastPreset
from src.model.rgb_model import AssignmentModel
from src.model.rgb_model import FailTransferRequestModel
from src.model.rgb_model import FailTransferResponseModel
from src.model.rgb_model import ListOnAndOffChainTransfersWithBalance
from src.model.rgb_model import ListTransfersRequestModel
from src.model.rgb_model import SendAssetRequestModel
from src.model.rgb_model import SendAssetResponseModel
from src.utils.cache import Cache
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_AUTHENTICATION_CANCELLED
from src.utils.error_message import ERROR_FAIL_TRANSFER
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_ASSET_SENT
from src.utils.info_message import INFO_FAIL_TRANSFER_SUCCESSFULLY
from src.utils.info_message import INFO_REFRESH_SUCCESSFULLY
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class CFAViewModel(QObject, ThreadManager):
    """This class represents the activities of the bitcoin page."""

    asset_info = Signal(str, str, str, str)
    txn_list_loaded = Signal(str, str, str, str)
    send_cfa_button_clicked = Signal(bool)
    message = Signal(ToastPreset, str)
    is_loading = Signal(bool)
    refresh = Signal(bool)
    stop_loading = Signal(bool)

    def __init__(self, page_navigation: Any) -> None:
        super().__init__()
        self._page_navigation = page_navigation
        self.asset_info.connect(self.get_cfa_asset_detail)

        # Initializing default values for attributes
        self.asset_id = None
        self.asset_name = None
        self.image_path = None
        self.asset_type = None
        self.blinded_utxo = None
        self.transport_endpoints = None
        self.amount = None
        self.fee_rate = None
        self.min_confirmation = None
        self.txn_list = []

    def get_cfa_asset_detail(self, asset_id: str, asset_name: str, image_path: str, asset_type: str) -> None:
        """Retrieve CFA asset list."""

        def on_success(response: ListOnAndOffChainTransfersWithBalance) -> None:
            """Handle success for the CFA asset detail list."""
            self.txn_list = response
            self.txn_list_loaded.emit(
                asset_id, asset_name, image_path, asset_type,
            )
            self.asset_id, self.asset_name, self.image_path, self.asset_type = asset_id, asset_name, image_path, asset_type
            self.is_loading.emit(False)

        def on_error(error: CommonException) -> None:
            """Handle error for the main asset page."""
            self.txn_list_loaded.emit(
                asset_id, asset_name, image_path, asset_type,
            )
            self.is_loading.emit(False)
            ToastManager.error(description=error)

        try:
            self.run_in_thread(
                AssetDetailPageService.get_asset_transactions,
                {
                    'args': [ListTransfersRequestModel(asset_id=asset_id)],
                    'callback': on_success,
                    'error_callback': on_error,
                },
            )
        except Exception as e:
            on_error(CommonException(message=str(e)))

    def on_success_cfa(self, tx_id: SendAssetResponseModel) -> None:
        """Handle success for sending CFA asset."""
        self.is_loading.emit(False)
        self.send_cfa_button_clicked.emit(False)
        ToastManager.success(description=INFO_ASSET_SENT.format(tx_id.txid))

        if self.asset_type == AssetType.CFA.value:
            self._page_navigation.collectibles_asset_page()
        elif self.asset_type == AssetType.NIA.value:
            self._page_navigation.fungibles_asset_page()

    def on_error(self, error: CommonException) -> None:
        """Handle error for sending CFA asset."""
        self.is_loading.emit(False)
        self.send_cfa_button_clicked.emit(False)
        ToastManager.error(description=error.message)

    def on_success_send_rgb_asset(self, success: bool) -> None:
        """Callback function after native authentication is successful."""
        if success:
            self.send_cfa_button_clicked.emit(True)
            self.is_loading.emit(True)
            try:
                self.run_in_thread(
                    RgbRepository.send_asset,
                    {
                        'args': [
                            SendAssetRequestModel(
                                asset_id=self.asset_id,
                                assignment=AssignmentModel(
                                    type=AssignmentEnumModel.FUNGIBLE, value=self.amount,
                                ),
                                recipient_id=self.blinded_utxo,
                                transport_endpoints=self.transport_endpoints,
                                fee_rate=self.fee_rate,
                                min_confirmations=self.min_confirmation,
                            ),
                        ],
                        'callback': self.on_success_cfa,
                        'error_callback': self.on_error,
                    },
                )
            except Exception as e:
                self.on_error(CommonException(message=str(e)))
        else:
            ToastManager.error(description=ERROR_AUTHENTICATION_CANCELLED)

    def on_error_native_auth(self, error: Exception) -> None:
        """Callback function on error during native authentication."""
        description = error.message if isinstance(
            error, CommonException,
        ) else ERROR_SOMETHING_WENT_WRONG
        ToastManager.error(description=description)

    def on_send_click(self, amount: int, blinded_utxo: str, transport_endpoints: list, fee_rate: int, min_confirmation: int) -> None:
        """Starts a thread to execute the send_cfa function with the provided arguments."""
        self.amount = amount
        self.blinded_utxo = blinded_utxo
        self.transport_endpoints = transport_endpoints
        self.fee_rate = fee_rate
        self.min_confirmation = min_confirmation
        self.run_in_thread(
            SettingRepository.native_authentication,
            {
                'args': [NativeAuthType.MAJOR_OPERATION],
                'callback': self.on_success_send_rgb_asset,
                'error_callback': self.on_error_native_auth,
            },
        )

    def on_refresh_click(self) -> None:
        """Executes the refresh operation in a separate thread."""
        cache = Cache.get_cache_session()
        if cache is not None:
            cache.invalidate_cache()
        self.send_cfa_button_clicked.emit(True)
        self.is_loading.emit(True)

        def on_success_refresh() -> None:
            """Handle success for refreshing transactions."""
            self.is_loading.emit(False)
            self.refresh.emit(True)
            ToastManager.success(description=INFO_REFRESH_SUCCESSFULLY)
            self.get_cfa_asset_detail(
                self.asset_id, self.asset_name, None, self.asset_type,
            )

        def on_error(error: CommonException) -> None:
            """Handle error for refreshing transactions."""
            self.refresh.emit(False)
            self.is_loading.emit(False)
            ToastManager.error(
                description=f'{ERROR_SOMETHING_WENT_WRONG}: {error}',
            )

        try:
            self.run_in_thread(
                RgbRepository.refresh_transfer,
                {
                    'args': [],
                    'callback': on_success_refresh,
                    'error_callback': on_error,
                },
            )
        except Exception as e:
            on_error(CommonException(message=str(e)))

    def on_fail_transfer(self, batch_transfer_idx: int) -> None:
        """Executes the fail transfer operation in a separate thread."""
        self.is_loading.emit(True)

        def on_success_fail_transfer(response: FailTransferResponseModel) -> None:
            """Handle success for failing a transfer."""
            if response.transfers_changed:
                self.get_cfa_asset_detail(
                    self.asset_id, self.asset_name, None, self.asset_type,
                )
                ToastManager.success(
                    description=INFO_FAIL_TRANSFER_SUCCESSFULLY,
                )
            else:
                self.is_loading.emit(False)
                ToastManager.error(description=ERROR_FAIL_TRANSFER)

        def on_error(error: CommonException) -> None:
            """Handle error for failing a transfer."""
            self.is_loading.emit(False)
            ToastManager.error(
                description=f'{ERROR_SOMETHING_WENT_WRONG}: {error.message}',
            )

        try:
            self.run_in_thread(
                RgbRepository.fail_transfer,
                {
                    'args': [FailTransferRequestModel(batch_transfer_idx=batch_transfer_idx)],
                    'callback': on_success_fail_transfer,
                    'error_callback': on_error,
                },
            )
        except Exception as e:
            on_error(CommonException(message=str(e)))
