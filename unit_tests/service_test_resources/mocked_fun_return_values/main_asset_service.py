"""Mocked data for the main asset page service test"""
from __future__ import annotations

from src.model.btc_model import BalanceResponseModel
from src.model.btc_model import BalanceStatus
from src.model.common_operation_model import NodeInfoResponseModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssetModel
from src.model.rgb_model import GetAssetResponseModel
from src.model.rgb_model import Media
from src.model.rgb_model import Token


mock_nia_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    ticker='USDT',
    name='Tether',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=777000, future=777000, spendable=777000, offchain_outbound=0, offchain_inbound=0,
    ),
    media=None,
    token=None,
)

mock_uda_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    ticker='UNI',
    name='Unique',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=777000, future=777000, spendable=777000, offchain_outbound=0, offchain_inbound=0,
    ),
    token=Token(
        index=0,
        ticker='TKN',
        name='Token',
        details='token details',
        embedded_media=True,
        media=Media(
            file_path='/path/to/media',
            mime='text/plain',
            digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
            hex='0x00',
        ),
        attachments={
            '0': Media(
                file_path='path/to/attachment0',
                mime='text/plain',
                digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
                hex='0x00',
            ),
            '1': Media(
                file_path='path/to/attachment1',
                mime='image/png',
                digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
                hex='0x00',
            ),
        },
        reserves=False,
    ),
    media=None,
)

mock_cfa_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    name='Collectible',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=777000, future=777000, spendable=777000, offchain_outbound=0, offchain_inbound=0,
    ),
    media=Media(
        file_path='/path/to/media', mime='text/plain',
        digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
        hex=None,
    ),
    token=None,
)

mock_cfa_asset_when_wallet_type_connect = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    name='Collectible',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=777000, future=777000, spendable=777000, offchain_outbound=0, offchain_inbound=0,
    ),
    media=Media(
        file_path='/path/to/media', mime='text/plain',
        digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
        hex='bc8100fa8743c11bd243eb3259f4b012758651612fd9bf93bf8b734d17f02561',
    ),
    token=None,
)

mock_get_asset_response_model = GetAssetResponseModel(
    nia=[mock_nia_asset],
    cfa=[mock_cfa_asset],
    uda=[mock_uda_asset],
)

"""Mock Return Data Of Function - BtcRepository.get_btc_balance"""
mock_balance_response_data = BalanceResponseModel(
    vanilla=BalanceStatus(settled=777000, future=777000, spendable=777000),
    colored=BalanceStatus(settled=777000, future=777000, spendable=777000),
)

"""Mock Return Data Of Function - CommonOperationRepository.node_info()"""
mock_node_info_Response_model = NodeInfoResponseModel(
    pubkey='02270dadcd6e7ba0ef707dac72acccae1a3607453a8dd2aef36ff3be4e0d31f043',
    num_channels=0,
    num_usable_channels=0,
    local_balance_sat=0,
    eventual_close_fees_sat=892,
    pending_outbound_payments_sat=7852,
    num_peers=0,
    account_xpub_vanilla='02270dadcd6e7ba0ef707dac72acccae1a3607453a8dd2aef36ff3be4e0d31f043',
    account_xpub_colored='02270dadcd6e7ba0ef707dac72acccae1a3607453a8dd2aef36ff3be4e0d31f043',
    max_media_upload_size_mb=5,
    rgb_htlc_min_msat=1,
    rgb_channel_capacity_min_sat=1,
    channel_capacity_min_sat=1,
    channel_capacity_max_sat=1,
    channel_asset_min_amount=1,
    channel_asset_max_amount=1,
    network_nodes=1,
    network_channels=1,
)


"""Mock Return Data - if is_exhausted_asset_enabled true"""

mock_nia_asset_exhausted_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k333',
    ticker='TTK',
    name='super man',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=0, future=0, spendable=0, offchain_outbound=0, offchain_inbound=0,
    ),
    media=None,
    token=None,
)

mock_uda_asset_exhausted_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    ticker='UNI',
    name='Unique',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=0, future=0, spendable=0, offchain_outbound=0, offchain_inbound=0,
    ),
    token=Token(
        index=0,
        ticker='TKN',
        name='Token',
        details='token details',
        embedded_media=True,
        media=Media(
            file_path='/path/to/media',
            mime='text/plain',
            digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
            hex='0x00',
        ),
        attachments={
            '0': Media(
                file_path='path/to/attachment0',
                mime='text/plain',
                digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
                hex='0x00',
            ),
            '1': Media(
                file_path='path/to/attachment1',
                mime='image/png',
                digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
                hex='0x00',
            ),
        },
        reserves=False,
    ),
    media=None,
)

mock_cfa_asset_exhausted_asset = AssetModel(
    asset_id='rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    name='Collectible',
    details='asset details',
    precision=0,
    issued_supply=777,
    timestamp=1691160565,
    added_at=1691161979,
    balance=AssetBalanceResponseModel(
        settled=0, future=0, spendable=0, offchain_outbound=0, offchain_inbound=0,
    ),
    media=Media(
        file_path='/path/to/media', mime='text/plain',
        digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
        hex=None,
    ),
    token=None,
)


mock_get_asset_response_model_when_exhausted_asset = GetAssetResponseModel(
    nia=[mock_nia_asset, mock_nia_asset_exhausted_asset],
    cfa=[mock_cfa_asset, mock_cfa_asset_exhausted_asset],
    uda=[mock_uda_asset, mock_uda_asset_exhausted_asset],
)
