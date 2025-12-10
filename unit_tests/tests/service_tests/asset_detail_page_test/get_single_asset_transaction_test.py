"""Unit tests for get_single_asset_transaction method """
from __future__ import annotations

from unittest.mock import patch

import pytest

from src.data.service.asset_detail_page_services import AssetDetailPageService
from src.model.rgb_model import ListTransfersRequestModel
from src.model.rgb_model import TransactionTxModel
from src.utils.custom_exception import CommonException
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_asset_id,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_invalid_tx_id,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_all_transaction,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_no_transaction,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_tx_id,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_when_transaction_type_send,
)

# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests  function
# pylint: disable=redefined-outer-name


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_get_single_asset_transaction_by_txid(mocked_get_asset_transaction_service):
    """Case 1 : Test service must return transaction based on tx_id"""
    mocked_get_asset_transaction_service.return_value = mocked_data_list_all_transaction
    result = AssetDetailPageService.get_single_asset_transaction(
        ListTransfersRequestModel(
            asset_id=mocked_data_asset_id,
        ),
        TransactionTxModel(tx_id=mocked_data_tx_id),
    )
    assert result == mocked_data_when_transaction_type_send
    assert result.idx == mocked_data_when_transaction_type_send.idx
    assert result.assignments[0].value == mocked_data_when_transaction_type_send.assignments[0].value
    assert result.txid == mocked_data_when_transaction_type_send.txid
    assert (
        result.created_at_date == mocked_data_when_transaction_type_send.created_at_date
    )
    assert (
        result.created_at_time == mocked_data_when_transaction_type_send.created_at_time
    )
    assert (
        result.updated_at_time == mocked_data_when_transaction_type_send.updated_at_time
    )
    assert (
        result.updated_at_date == mocked_data_when_transaction_type_send.updated_at_date
    )
    assert result.receive_utxo == mocked_data_when_transaction_type_send.receive_utxo
    assert result.recipient_id == mocked_data_when_transaction_type_send.recipient_id
    assert result.change_utxo == mocked_data_when_transaction_type_send.change_utxo
    assert result.status == mocked_data_when_transaction_type_send.status
    assert result.kind == mocked_data_when_transaction_type_send.kind
    assert result.expiration == mocked_data_when_transaction_type_send.expiration
    assert (
        result.transfer_Status == mocked_data_when_transaction_type_send.transfer_Status
    )
    assert result.created_at == mocked_data_when_transaction_type_send.created_at
    assert result.updated_at == mocked_data_when_transaction_type_send.updated_at
    assert (
        result.transport_endpoints
        == mocked_data_when_transaction_type_send.transport_endpoints
    )
    assert (
        result.transport_endpoints[0].endpoint
        == mocked_data_when_transaction_type_send.transport_endpoints[0].endpoint
    )
    assert (
        result.transport_endpoints[0].transport_type
        == mocked_data_when_transaction_type_send.transport_endpoints[0].transport_type
    )
    assert (
        result.transport_endpoints[0].used
        == mocked_data_when_transaction_type_send.transport_endpoints[0].used
    )


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_get_single_asset_transaction_by_idx(mocked_get_asset_transaction_service):
    """Case 2 : Test service must return transaction based on idx"""
    mocked_get_asset_transaction_service.return_value = mocked_data_list_all_transaction
    result = AssetDetailPageService.get_single_asset_transaction(
        ListTransfersRequestModel(
            asset_id=mocked_data_asset_id,
        ),
        TransactionTxModel(idx=2),
    )
    assert result == mocked_data_when_transaction_type_send
    assert result.idx == mocked_data_when_transaction_type_send.idx
    assert result.assignments[0].value == mocked_data_when_transaction_type_send.assignments[0].value
    assert result.txid == mocked_data_when_transaction_type_send.txid
    assert (
        result.created_at_date == mocked_data_when_transaction_type_send.created_at_date
    )
    assert (
        result.created_at_time == mocked_data_when_transaction_type_send.created_at_time
    )
    assert (
        result.updated_at_time == mocked_data_when_transaction_type_send.updated_at_time
    )
    assert (
        result.updated_at_date == mocked_data_when_transaction_type_send.updated_at_date
    )
    assert result.receive_utxo == mocked_data_when_transaction_type_send.receive_utxo
    assert result.recipient_id == mocked_data_when_transaction_type_send.recipient_id
    assert result.change_utxo == mocked_data_when_transaction_type_send.change_utxo
    assert result.status == mocked_data_when_transaction_type_send.status
    assert result.kind == mocked_data_when_transaction_type_send.kind
    assert result.expiration == mocked_data_when_transaction_type_send.expiration
    assert (
        result.transfer_Status == mocked_data_when_transaction_type_send.transfer_Status
    )
    assert result.created_at == mocked_data_when_transaction_type_send.created_at
    assert result.updated_at == mocked_data_when_transaction_type_send.updated_at
    assert (
        result.transport_endpoints
        == mocked_data_when_transaction_type_send.transport_endpoints
    )
    assert (
        result.transport_endpoints[0].endpoint
        == mocked_data_when_transaction_type_send.transport_endpoints[0].endpoint
    )
    assert (
        result.transport_endpoints[0].transport_type
        == mocked_data_when_transaction_type_send.transport_endpoints[0].transport_type
    )
    assert (
        result.transport_endpoints[0].used
        == mocked_data_when_transaction_type_send.transport_endpoints[0].used
    )


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_when_no_transaction_found(mocked_get_asset_transaction_service):
    """Case 3 : It should return None when no transaction found with idx and txid"""
    mocked_get_asset_transaction_service.return_value = mocked_data_list_all_transaction
    result_by_idx = AssetDetailPageService.get_single_asset_transaction(
        ListTransfersRequestModel(
            asset_id=mocked_data_asset_id,
        ),
        TransactionTxModel(idx=10),
    )
    result_by_txid = AssetDetailPageService.get_single_asset_transaction(
        ListTransfersRequestModel(
            asset_id=mocked_data_asset_id,
        ),
        TransactionTxModel(tx_id=mocked_data_invalid_tx_id),
    )
    assert result_by_idx is None
    assert result_by_txid is None


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_when_not_both_pass_txid_idx(mocked_get_asset_transaction_service):
    """Case 4 : It should throw error when both not passed txid and idx"""

    mocked_get_asset_transaction_service.return_value = mocked_data_list_all_transaction

    # Execute the function under test and expect CommonException instead
    with pytest.raises(CommonException) as exc_info:
        AssetDetailPageService.get_single_asset_transaction(
            ListTransfersRequestModel(
                asset_id=mocked_data_asset_id,
            ),
            TransactionTxModel(),
        )

    # Assert the exception message is as expected
    assert str(exc_info.value) == "Either 'tx_id' or 'idx' must be provided"


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_when_pass_both_txid_idx(mocked_get_asset_transaction_service):
    """Case 5 : It should throw error when we pass txid and idx both"""

    mocked_get_asset_transaction_service.return_value = mocked_data_list_all_transaction

    # Execute the function under test and expect CommonException instead
    with pytest.raises(CommonException) as exc_info:
        AssetDetailPageService.get_single_asset_transaction(
            ListTransfersRequestModel(
                asset_id=mocked_data_asset_id,
            ),
            TransactionTxModel(tx_id=mocked_data_tx_id, idx=2),
        )

    # Assert the exception message is as expected
    assert (
        str(
            exc_info.value,
        )
        == "Both 'tx_id' and 'idx' cannot be accepted at the same time."
    )


@patch(
    'src.data.service.asset_detail_page_services.AssetDetailPageService.get_asset_transactions',
)
def test_when_no_transaction(mocked_get_asset_transaction_service):
    """Case  6: It should return none when no transaction"""
    mocked_get_asset_transaction_service.return_value = mocked_data_list_no_transaction
    result = AssetDetailPageService.get_single_asset_transaction(
        ListTransfersRequestModel(
            asset_id=mocked_data_asset_id,
        ),
        TransactionTxModel(idx=2),
    )
    assert result is None
