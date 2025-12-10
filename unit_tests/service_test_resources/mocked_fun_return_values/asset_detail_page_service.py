"""
Mocked data for the asset detail page service service test
"""
from __future__ import annotations

from src.model.enums.enums_model import AssignmentEnumModel
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssignmentModel
from src.model.rgb_model import ListTransferAssetResponseModel
from src.model.rgb_model import ListTransferAssetWithBalanceResponseModel
from src.model.rgb_model import TransferAsset
from src.model.rgb_model import TransportEndpoint

mocked_data_when_transaction_type_issuance = TransferAsset(
    idx=1,
    created_at=1717565849,
    updated_at=1717565849,
    status='Settled',
    assignments=[
        AssignmentModel(
            type=AssignmentEnumModel.FUNGIBLE, value=1600,
        ),
    ],
    requested_assignment=AssignmentModel(
        type=AssignmentEnumModel.FUNGIBLE, value=1600,
    ),
    kind='Issuance',
    txid=None,
    recipient_id=None,
    receive_utxo=None,
    change_utxo=None,
    expiration=None,
    transport_endpoints=[],
)

mocked_data_when_transaction_type_send = TransferAsset(
    idx=2,
    created_at=1717566312,
    updated_at=1717567082,
    status='Settled',
    requested_assignment=AssignmentModel(
        type=AssignmentEnumModel.FUNGIBLE, value=1000,
    ),
    assignments=[
        AssignmentModel(
            type=AssignmentEnumModel.FUNGIBLE, value=1000,
        ),
    ],
    kind='Send',
    txid='5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a6ae',
    recipient_id='utxob:2okFKi2-8Ex84DQNt-jzCHrU4HA-vozR9aDut-VEdc5yBUX-Ktfqhk8',
    receive_utxo=None,
    change_utxo='23beece15fc30af37afae0b6499f8d5f91d3fe57168b5a5eeb97e9a65ecc818b:2',
    expiration=1717569912,
    transport_endpoints=[
        TransportEndpoint(
            endpoint='http://127.0.0.1:3000/json-rpc',
            transport_type='JsonRpc',
            used=True,
        ),
    ],
)
mocked_data_when_transaction_receive_blind = TransferAsset(
    idx=3,
    created_at=1717566191,
    updated_at=1717567096,
    status='Settled',
    requested_assignment=AssignmentModel(
        type=AssignmentEnumModel.FUNGIBLE, value=42,
    ),
    assignments=[AssignmentModel(type=AssignmentEnumModel.FUNGIBLE, value=42)],
    kind='ReceiveBlind',
    txid='5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a6ae',
    recipient_id='utxob:2okFKi2-8Ex84DQNt-jzCHrU4HA-vozR9aDut-VEdc5yBUX-Ktfqhk8',
    receive_utxo='3a7b2dfaca7186c5d68c960eb69f2ab164bb0a6e391607f06fcff96bc303c3c4:0',
    change_utxo=None,
    expiration=1717652591,
    transport_endpoints=[
        TransportEndpoint(
            endpoint='http://127.0.0.1:3000/json-rpc',
            transport_type='JsonRpc',
            used=True,
        ),
    ],
)

mocked_data_when_transaction_receive_witness = TransferAsset(
    idx=4,
    created_at=1717566191,
    updated_at=1717567096,
    status='Settled',
    requested_assignment=AssignmentModel(
        type=AssignmentEnumModel.FUNGIBLE, value=42,
    ),
    assignments=[AssignmentModel(type=AssignmentEnumModel.FUNGIBLE, value=42)],
    kind='ReceiveWitness',
    txid='5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a6ae',
    recipient_id='utxob:2okFKi2-8Ex84DQNt-jzCHrU4HA-vozR9aDut-VEdc5yBUX-Ktfqhk8',
    receive_utxo='3a7b2dfaca7186c5d68c960eb69f2ab164bb0a6e391607f06fcff96bc303c3c4:0',
    change_utxo=None,
    expiration=1717652591,
    transport_endpoints=[
        TransportEndpoint(
            endpoint='http://127.0.0.1:3000/json-rpc',
            transport_type='JsonRpc',
            used=True,
        ),
    ],
)

mocked_data_when_transaction_invalid = TransferAsset(
    idx=5,
    created_at=1717566191,
    updated_at=1717567096,
    status='Settled',
    requested_assignment=AssignmentModel(
        type=AssignmentEnumModel.FUNGIBLE, value=42,
    ),
    assignments=[AssignmentModel(type=AssignmentEnumModel.FUNGIBLE, value=42)],
    kind='Invalid',
    txid='5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a6ae',
    recipient_id='utxob:2okFKi2-8Ex84DQNt-jzCHrU4HA-vozR9aDut-VEdc5yBUX-Ktfqhk8',
    receive_utxo='3a7b2dfaca7186c5d68c960eb69f2ab164bb0a6e391607f06fcff96bc303c3c4:0',
    change_utxo=None,
    expiration=1717652591,
    transport_endpoints=[
        TransportEndpoint(
            endpoint='http://127.0.0.1:3000/json-rpc',
            transport_type='JsonRpc',
            used=True,
        ),
    ],
)

mocked_data_list_when_transaction_type_issuance = ListTransferAssetResponseModel(
    transfers=[mocked_data_when_transaction_type_issuance],
)
mocked_data_list_when_transaction_type_send = ListTransferAssetResponseModel(
    transfers=[mocked_data_when_transaction_type_send],
)
mocked_data_list_when_transaction_type_receive_blind = ListTransferAssetResponseModel(
    transfers=[mocked_data_when_transaction_receive_blind],
)
mocked_data_list_when_transaction_type_receive_witness = ListTransferAssetResponseModel(
    transfers=[mocked_data_when_transaction_receive_witness],
)
mocked_data_list_when_transaction_type_inValid = ListTransferAssetResponseModel(
    transfers=[mocked_data_when_transaction_invalid],
)

# Corrected date and time assignments
mocked_data_when_transaction_type_issuance.created_at_date = '2024-06-05'
mocked_data_when_transaction_type_issuance.created_at_time = '11:07:29'
mocked_data_when_transaction_type_issuance.updated_at_date = '2024-06-05'
mocked_data_when_transaction_type_issuance.updated_at_time = '11:07:29'
mocked_data_when_transaction_type_issuance.transfer_Status = (
    TransferStatusEnumModel.INTERNAL
)

mocked_data_when_transaction_type_send.created_at_date = '2024-06-05'
mocked_data_when_transaction_type_send.created_at_time = '11:15:12'
mocked_data_when_transaction_type_send.updated_at_date = '2024-06-05'
mocked_data_when_transaction_type_send.updated_at_time = '11:28:02'
mocked_data_when_transaction_type_send.transfer_Status = TransferStatusEnumModel.SENT

mocked_data_when_transaction_receive_blind.created_at_date = '2024-06-05'
mocked_data_when_transaction_receive_blind.created_at_time = '11:16:31'
mocked_data_when_transaction_receive_blind.updated_at_date = '2024-06-05'
mocked_data_when_transaction_receive_blind.updated_at_time = '11:31:36'
mocked_data_when_transaction_receive_blind.transfer_Status = (
    TransferStatusEnumModel.RECEIVED
)

mocked_data_when_transaction_receive_witness.created_at_date = '2024-06-05'
mocked_data_when_transaction_receive_witness.created_at_time = '11:16:31'
mocked_data_when_transaction_receive_witness.updated_at_date = '2024-06-05'
mocked_data_when_transaction_receive_witness.updated_at_time = '11:31:36'
mocked_data_when_transaction_receive_witness.transfer_Status = (
    TransferStatusEnumModel.RECEIVED
)

# pylint: disable=invalid-name
mocked_data_asset_id = 'rgb:2pt8fPf-Rvt9UZvzw-EkoFpAdx4-U7PPZzZG9-wvZYHUVL4-rtPqGp7'
mocked_data_tx_id = '5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a6ae'
mocked_data_invalid_tx_id = (
    '5872b8b5333054e1e3768d897d9d0ccceb0e5a9388f2f83649241e8d2125a777'
)
mocked_data_no_transaction = None
# pylint: enable=invalid-name

mocked_data_asset_balance = AssetBalanceResponseModel(
    settled=1225,
    future=1141,
    spendable=0,
    offchain_inbound=0,
    offchain_outbound=0,
)
mocked_data_list_transaction_type_issuance = ListTransferAssetWithBalanceResponseModel(
    transfers=[
        mocked_data_when_transaction_type_issuance,
    ],
    asset_balance=mocked_data_asset_balance,
)
mocked_data_list_transaction_type_send = ListTransferAssetWithBalanceResponseModel(
    transfers=[
        mocked_data_when_transaction_type_send,
    ],
    asset_balance=mocked_data_asset_balance,
)
mocked_data_list_transaction_type_receive_blind = (
    ListTransferAssetWithBalanceResponseModel(
        transfers=[
            mocked_data_when_transaction_receive_blind,
        ],
        asset_balance=mocked_data_asset_balance,
    )
)
mocked_data_list_transaction_type_receive_witness = (
    ListTransferAssetWithBalanceResponseModel(
        transfers=[
            mocked_data_when_transaction_receive_witness,
        ],
        asset_balance=mocked_data_asset_balance,
    )
)
mocked_data_list_no_transaction = ListTransferAssetWithBalanceResponseModel(
    transfers=[],
    asset_balance=mocked_data_asset_balance,
)
mocked_data_list_all_transaction = ListTransferAssetWithBalanceResponseModel(
    transfers=[
        mocked_data_when_transaction_type_issuance,
        mocked_data_when_transaction_type_send,
        mocked_data_when_transaction_receive_blind,
        mocked_data_when_transaction_receive_witness,
    ],
    asset_balance=mocked_data_asset_balance,
)
