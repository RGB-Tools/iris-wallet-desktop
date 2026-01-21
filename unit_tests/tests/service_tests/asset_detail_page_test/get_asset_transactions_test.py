# pylint: disable=redefined-outer-name, unused-argument, unused-import
"""Unit tests for get_asset_transactions method """
from __future__ import annotations

import pytest

from src.data.service.asset_detail_page_services import AssetDetailPageService
from src.model.payments_model import ListPaymentResponseModel
from src.model.rgb_model import AssetIdModel
from src.model.rgb_model import ListOnAndOffChainTransfersWithBalance
from src.model.rgb_model import ListTransfersRequestModel
from src.utils.custom_exception import CommonException
from src.utils.custom_exception import ServiceOperationException
from unit_tests.repository_fixture.rgb_repository_mock import mock_get_asset_balance
from unit_tests.repository_fixture.rgb_repository_mock import mock_list_transfers
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_asset_balance,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_asset_id,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_no_transaction,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_transaction_type_issuance,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_transaction_type_receive_blind,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_transaction_type_receive_witness,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_transaction_type_send,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_when_transaction_type_inValid,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_when_transaction_type_issuance,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_when_transaction_type_receive_blind,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_when_transaction_type_receive_witness,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_list_when_transaction_type_send,
)
from unit_tests.service_test_resources.mocked_fun_return_values.asset_detail_page_service import (
    mocked_data_no_transaction,
)

# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name


@pytest.fixture
def request_mock(mocker):
    """Mock Request class"""
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_get = mocker.patch(
        'src.utils.request.Request.get', return_value=mock_response,
    )
    return mock_get


@pytest.fixture
def mock_list_payment(mocker):
    """Mock PaymentRepository list_payment method"""
    mock_response = mocker.MagicMock()
    mock_response.return_value = ListPaymentResponseModel(
        payments=[],
        chain_inbound=0,
        chain_outbound=0,
        lightning_inbound=0,
        lightning_outbound=0,
    )
    mock = mocker.patch(
        'src.data.repository.payments_repository.PaymentRepository.list_payment',
        return_value=mock_response.return_value,
    )
    return mock


@pytest.fixture
def mock_rgb_repository(mocker):
    """Mock RgbRepository"""
    return mocker.patch(
        'src.data.service.asset_detail_page_services.RgbRepository',
        autospec=True,
    )


def test_no_transaction(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 1: When no transaction"""
    list_transaction_mock_object = mock_list_transfers(
        mocked_data_no_transaction,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )

    result = AssetDetailPageService.get_asset_transactions(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )
    assert not result.onchain_transfers
    assert not result.off_chain_transfers
    assert result.asset_balance == mocked_data_list_no_transaction.asset_balance
    mock_list_payment.assert_called_once()
    assert isinstance(result, ListOnAndOffChainTransfersWithBalance)


def test_transaction_type_send(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 2: When transaction type issuence"""
    list_transaction_mock_object = mock_list_transfers(
        mocked_data_list_when_transaction_type_send,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )
    result = AssetDetailPageService.get_asset_transactions(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )

    # Verify the result structure
    assert isinstance(result, ListOnAndOffChainTransfersWithBalance)
    assert result.onchain_transfers == mocked_data_list_transaction_type_send.transfers
    assert result.asset_balance == mocked_data_list_transaction_type_send.asset_balance
    assert not result.off_chain_transfers
    mock_list_payment.assert_called_once()


def test_transaction_type_receive_blind(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 2: When transaction type receive blind"""
    list_transaction_mock_object = mock_list_transfers(
        mocked_data_list_when_transaction_type_receive_blind,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )
    result = AssetDetailPageService.get_asset_transactions(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )

    # Verify the result structure
    assert isinstance(result, ListOnAndOffChainTransfersWithBalance)
    assert result.onchain_transfers == mocked_data_list_transaction_type_receive_blind.transfers
    assert result.asset_balance == mocked_data_list_transaction_type_receive_blind.asset_balance
    assert not result.off_chain_transfers
    mock_list_payment.assert_called_once()


def test_transaction_type_receive_witness(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 2: When transaction type receive witness"""
    list_transaction_mock_object = mock_list_transfers(
        mocked_data_list_when_transaction_type_receive_witness,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )
    result = AssetDetailPageService.get_asset_transactions(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )

    # Verify the result structure
    assert isinstance(result, ListOnAndOffChainTransfersWithBalance)
    assert result.onchain_transfers == mocked_data_list_transaction_type_receive_witness.transfers
    assert result.asset_balance == mocked_data_list_transaction_type_receive_witness.asset_balance
    assert not result.off_chain_transfers
    mock_list_payment.assert_called_once()


def test_transaction_type_receive_issuence(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 2: When transaction type receive issuance"""
    list_transaction_mock_object = mock_list_transfers(
        mocked_data_list_when_transaction_type_issuance,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )
    result = AssetDetailPageService.get_asset_transactions(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )

    # Verify the result structure
    assert isinstance(result, ListOnAndOffChainTransfersWithBalance)
    assert result.onchain_transfers == mocked_data_list_transaction_type_issuance.transfers
    assert result.asset_balance == mocked_data_list_transaction_type_issuance.asset_balance
    assert not result.off_chain_transfers
    mock_list_payment.assert_called_once()


def test_transaction_type_invalid(mock_list_transfers, mock_get_asset_balance, request_mock, mock_list_payment):
    """case 6: When transaction type not valid"""
    # Configure mock_list_payment to raise exception before it's called
    mock_list_payment.side_effect = ServiceOperationException(
        'Unknown transaction type',
    )

    list_transaction_mock_object = mock_list_transfers(
        mocked_data_list_when_transaction_type_inValid,
    )
    asset_balance_mock_object = mock_get_asset_balance(
        mocked_data_asset_balance,
    )

    # Execute the function under test and expect CommonException instead
    with pytest.raises(CommonException) as exc_info:
        AssetDetailPageService.get_asset_transactions(
            ListTransfersRequestModel(asset_id=mocked_data_asset_id),
        )

    list_transaction_mock_object.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )
    asset_balance_mock_object.assert_called_once_with(
        AssetIdModel(asset_id=mocked_data_asset_id),
    )

    # Assert the exception message is as expected
    assert str(exc_info.value) == 'Unknown transaction type'


def test_list_transfers_error(mocker, mock_rgb_repository, request_mock, mock_list_payment):
    """case 7: When RgbRepository.list_transfers raises an error"""
    # Configure mock to raise an exception
    mock_rgb_repository.list_transfers.side_effect = ServiceOperationException(
        'Test error',
    )

    # Execute the function under test and expect CommonException
    with pytest.raises(CommonException) as exc_info:
        AssetDetailPageService.get_asset_transactions(
            ListTransfersRequestModel(asset_id=mocked_data_asset_id),
        )

    # Verify the mock was called
    mock_rgb_repository.list_transfers.assert_called_once_with(
        ListTransfersRequestModel(asset_id=mocked_data_asset_id),
    )

    # Verify other mocks were not called
    mock_rgb_repository.get_asset_balance.assert_not_called()
    mock_list_payment.assert_not_called()

    # Assert the exception message
    assert str(exc_info.value) == 'Test error'
