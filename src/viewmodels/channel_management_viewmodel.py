"""This module contains the ChannelManagementViewModel class, which represents the view model
for the channel management page activities.
"""
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from src.data.repository.channels_repository import ChannelRepository
from src.data.repository.rgb_repository import RgbRepository
from src.data.service.open_channel_service import LnNodeChannelManagement
from src.model.channels_model import Channel
from src.model.channels_model import ChannelsListResponseModel
from src.model.channels_model import CloseChannelRequestModel
from src.model.channels_model import CloseChannelResponseModel
from src.model.channels_model import HandleInsufficientAllocationSlotsModel
from src.model.channels_model import OpenChannelResponseModel
from src.model.channels_model import OpenChannelsRequestModel
from src.model.enums.enums_model import ChannelFetchingModel
from src.model.enums.enums_model import FilterAssetEnumModel
from src.model.rgb_model import AssetModel
from src.model.rgb_model import FilterAssetRequestModel
from src.model.rgb_model import GetAssetResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_CREATE_UTXO
from src.utils.error_message import ERROR_INSUFFICIENT_ALLOCATION_SLOT
from src.utils.error_message import ERROR_INSUFFICIENT_ASSET
from src.utils.error_message import ERROR_INVALID_PEER_TYPE
from src.utils.error_message import ERROR_INVALID_PUBKEY_TYPE
from src.utils.error_message import ERROR_NO_UNCOLORED_UTXOS_AVAILABLE
from src.utils.error_message import ERROR_SOMETHING_WENT_WRONG
from src.utils.info_message import INFO_CHANNEL_DELETED
from src.utils.worker import ThreadManager
from src.views.components.toast import ToastManager


class ChannelManagementViewModel(QObject, ThreadManager):
    """This class represents the activities of the channel management page."""
    list_loaded = Signal(bool)
    loading_started = Signal(bool)
    loading_finished = Signal(bool)
    is_loading = Signal(bool)
    channel_created = Signal()
    channel_deleted = Signal(bool)
    asset_loaded_signal = Signal()
    channel_loaded = Signal()
    is_channel_fetching = Signal(bool, str)

    def __init__(self, page_navigation) -> None:
        super().__init__()
        self._page_navigation = page_navigation
        self.channels: list[Channel] = []
        self.nia_asset: list[AssetModel] = []
        self.cfa_asset: list[AssetModel] = []
        self.assets_loaded = False
        self.channels_loaded = False
        self.total_asset_lookup_list: dict = {}
        self.loading_tasks = 0

    def update_loading(self, increment: bool):
        """
        Updates the loading task count and emits appropriate signals.

        Parameters:
        -----------
        increment : bool
            True to increment the loading task count, False to decrement.
        """
        self.loading_tasks += 1 if increment else -1
        if self.loading_tasks == 1 and increment:
            self.loading_started.emit(True)
        elif self.loading_tasks == 0 and not increment:
            self.loading_finished.emit(True)

    def available_channels(self):
        """This method retrieves channels for the channel management page."""
        self.is_channel_fetching.emit(
            True, ChannelFetchingModel.FETCHING.value,
        )
        self.update_loading(True)

        def success(channel_list: ChannelsListResponseModel):
            """This method is used  handle success."""
            if channel_list is not None:
                # Ensure we are only getting Channel objects and no None values
                self.channels = [
                    channel for channel in channel_list.channels if channel is not None
                ]
                self.channels.reverse()
                self.channels_loaded = True
                self.check_loading_completion()
                self.channel_loaded.emit()
            self.update_loading(False)
            self.is_channel_fetching.emit(
                False, ChannelFetchingModel.FETCHED.value,
            )

        def on_error(error: CommonException):
            """This method is used  handle error."""
            self.update_loading(False)
            self.is_channel_fetching.emit(
                False, ChannelFetchingModel.FAILED.value,
            )
            ToastManager.error(
                description=error.message,
            )

        self.run_in_thread(
            ChannelRepository.list_channel,
            {
                'callback': success,
                'error_callback': on_error,
            },
        )

    def navigate_to_create_channel_page(self):
        """This method used to navigate create channel page."""
        self._page_navigation.create_channel_page()

    def create_rgb_channel(self, pub_key: str, asset_id: str, amount: int, capacity_sat: str, push_msat: str) -> None:
        """This method used to create channels."""
        self.is_loading.emit(True)

        def on_success(response: OpenChannelResponseModel):
            if response.temporary_channel_id:
                self.is_loading.emit(False)
                self.channel_created.emit()

        def on_error(error: CommonException):
            if error.message in (ERROR_INVALID_PUBKEY_TYPE, ERROR_INVALID_PEER_TYPE, ERROR_INSUFFICIENT_ASSET):
                ToastManager.error(description=error.message)
                self.is_loading.emit(False)
            elif error.message in (ERROR_INSUFFICIENT_ALLOCATION_SLOT, ERROR_NO_UNCOLORED_UTXOS_AVAILABLE):
                params = HandleInsufficientAllocationSlotsModel(
                    capacity_sat=capacity_sat, pub_key=pub_key, push_msat=push_msat, asset_id=asset_id, amount=amount,
                )
                self.handle_insufficient_allocation(params)
            else:
                ToastManager.error(description=error.message)
                self.is_loading.emit(False)

        self.run_in_thread(
            LnNodeChannelManagement.open_channel,
            {
                'args': [
                    OpenChannelsRequestModel(
                        peer_pubkey_and_opt_addr=pub_key, push_msat=push_msat,
                        capacity_sat=capacity_sat, asset_amount=amount, asset_id=asset_id,
                    ),
                ],
                'callback': on_success,
                'error_callback': on_error,
            },
        )

    def get_asset_list(self):
        """This method handled to get nia asset list of the user"""
        self.update_loading(True)

        def on_success(response: GetAssetResponseModel):
            if response is not None:
                if response.nia:
                    self.nia_asset = [
                        nia for nia in response.nia if nia is not None
                    ]
                else:
                    self.nia_asset = []

                if response.cfa:
                    self.cfa_asset = [
                        cfa for cfa in response.cfa if cfa is not None
                    ]
                else:
                    self.cfa_asset = []

                self.nia_asset.reverse()
                self.total_asset_lookup_list = self.get_asset_name()
                self.asset_loaded_signal.emit()
                self.assets_loaded = True
                self.check_loading_completion()
            self.update_loading(False)

        def on_error(error: CommonException):
            self.update_loading(False)
            ToastManager.error(
                description=error.message,
            )

        self.run_in_thread(
            RgbRepository.get_assets,
            {
                'args': [FilterAssetRequestModel(filter_asset_schemas=[FilterAssetEnumModel.NIA, FilterAssetEnumModel.CFA])],
                'callback': on_success,
                'error_callback': on_error,
            },
        )

    def close_channel(self, channel_id: str, pub_key: str) -> None:
        """This method used to close channels."""
        self.loading_started.emit(True)

        def on_success(response: CloseChannelResponseModel):
            if response:
                self.loading_finished.emit(True)
                self.channel_deleted.emit(True)
            ToastManager.success(
                description=INFO_CHANNEL_DELETED.format(pub_key),
            )
            self._page_navigation.channel_management_page()

        def on_error(error: CommonException):
            ToastManager.error(
                description=error.message,
            )
            self.loading_finished.emit(True)

        self.run_in_thread(
            ChannelRepository.close_channel,
            {
                'args': [
                    CloseChannelRequestModel(
                        channel_id=channel_id, peer_pubkey=pub_key,
                    ),
                ],
                'callback': on_success,
                'error_callback': on_error,
            },
        )

    def create_channel_with_btc(self, pub_key: str, capacity: str, push_msat: str) -> None:
        """This method used to create channels for bitcoin."""
        try:
            self.is_loading.emit(True)

            def on_success(response: OpenChannelResponseModel):
                if response.temporary_channel_id:
                    self.is_loading.emit(False)
                    self.channel_created.emit()

            def on_error(error: CommonException):
                self.is_loading.emit(False)
                ToastManager.error(
                    description=error.message,
                )

            self.run_in_thread(
                LnNodeChannelManagement.open_channel,
                {
                    'args': [
                        OpenChannelsRequestModel(
                            peer_pubkey_and_opt_addr=pub_key, push_msat=push_msat, capacity_sat=capacity,
                        ),
                    ],
                    'callback': on_success,
                    'error_callback': on_error,
                },
            )
        except CommonException as error:
            self.is_loading.emit(False)
            ToastManager.error(
                description=error.message,
            )
        except Exception:
            self.is_loading.emit(False)
            ToastManager.error(
                description=ERROR_SOMETHING_WENT_WRONG,
            )

    def handle_insufficient_allocation(self, params: HandleInsufficientAllocationSlotsModel):
        """
        Handles cases where there is insufficient allocation for opening a channel by
        creating a new UTXO and attempting to create the channel.

        Parameters:
        -----------
        params : HandleInsufficientAllocationSlotsModel
            The model containing the required parameters to create the UTXO and channel.

        Behavior:
        ---------
        - Creates a UTXO using `RgbRepository.create_utxo` in a separate thread.
        - On successful UTXO creation, the channel is opened:
            - If it's a Bitcoin channel, the appropriate parameters are used.
            - If it's an RGB channel, asset-related parameters are passed.
        - If UTXO creation fails, an error toast is displayed, and the loading indicator is disabled.

        Callbacks:
        ----------
        - `on_success_creation_utxo`: Creates the channel with the given parameters after UTXO creation.
        - `on_error_creation_utxo`: Emits a loading signal and displays an error toast if UTXO creation fails.
        """
        def on_success_creation_utxo():
            """Callback executed on successful UTXO creation."""
            self.create_rgb_channel(
                params.pub_key, params.asset_id,
                params.amount, params.capacity_sat, params.push_msat,
            )

        def on_error_creation_utxo(error: CommonException):
            """Callback executed if UTXO creation fails."""
            self.is_loading.emit(False)
            ToastManager.error(
                description=ERROR_CREATE_UTXO.format(error.message),
            )

        self.run_in_thread(
            LnNodeChannelManagement.create_utxo_for_channel,
            {
                'args': [
                    params.capacity_sat,
                ],
                'callback': on_success_creation_utxo,
                'error_callback': on_error_creation_utxo,
            },
        )

    def check_loading_completion(self):
        """Checks if both assets and channels have been loaded."""
        if self.assets_loaded and self.channels_loaded:
            self.list_loaded.emit(True)

    def get_asset_name(self):
        """This method is used to map the name of the asset to their asset IDs"""
        nia_asset_lookup = {
            asset.asset_id: asset.name for asset in self.nia_asset
        }
        cfa_asset_lookup = {
            asset.asset_id: asset.name for asset in self.cfa_asset
        }
        self.total_asset_lookup_list = {
            **nia_asset_lookup, **cfa_asset_lookup,
        }

        return self.total_asset_lookup_list
