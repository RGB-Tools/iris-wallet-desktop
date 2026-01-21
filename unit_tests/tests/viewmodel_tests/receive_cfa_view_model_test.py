"""Unit test for ReceiveCFAViewModel"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.model.rgb_model import RgbInvoiceDataResponseModel
from src.utils.custom_exception import CommonException
from src.viewmodels.receive_cfa_view_model import ReceiveCFAViewModel


@pytest.fixture
def mock_page_navigation(mocker):
    """Fixture to create a mock page navigation object."""
    return mocker.MagicMock()


@pytest.fixture
def receive_cfa_view_model(mock_page_navigation):
    """Fixture to create an instance of the ReceiveCFAViewModel class."""
    return ReceiveCFAViewModel(mock_page_navigation)


@patch('src.data.repository.rgb_repository.RgbRepository.rgb_invoice')
def test_get_rgb_invoice_success(mock_rgb_invoice, receive_cfa_view_model):
    """Test for successfully retrieving an RGB invoice."""
    mock_address_signal = Mock()
    receive_cfa_view_model.address.connect(mock_address_signal)
    mock_loading_signal = Mock()
    receive_cfa_view_model.hide_loading.connect(mock_loading_signal)

    mock_invoice_response = RgbInvoiceDataResponseModel(
        recipient_id='recipient_id',
        invoice='rgb_invoice_string',
        expiration_timestamp='1695811760',
        batch_transfer_idx=1,
    )

    mock_rgb_invoice.return_value = mock_invoice_response

    # Call get_rgb_invoice with a minimum confirmation argument
    receive_cfa_view_model.get_rgb_invoice(minimum_confirmations=1)
    receive_cfa_view_model.worker.result.emit(mock_invoice_response)

    mock_address_signal.assert_called_once_with(mock_invoice_response.invoice)
    mock_loading_signal.assert_called_once_with(False)


@patch('src.views.components.toast.ToastManager.error')
def test_on_error_shows_error_and_navigates(mock_toast, receive_cfa_view_model):
    """Test for handling errors in on_error method."""
    mock_loading_signal = Mock()
    receive_cfa_view_model.hide_loading.connect(mock_loading_signal)

    # Create a mock error
    mock_error = CommonException('Error occurred')

    # Call the on_error method with the mock error
    receive_cfa_view_model.on_error(mock_error)

    # Assert that the error toast was shown with the correct message
    mock_toast.assert_called_once_with(
        description='Error occurred',
    )

    # Assert that loading is hidden
    mock_loading_signal.assert_called_once_with(False)

    # Assert that the navigation to fungibles asset page occurred
    receive_cfa_view_model._page_navigation.fungibles_asset_page.assert_called_once()

    # Assert that the sidebar is checked
    sidebar_mock = Mock()
    receive_cfa_view_model._page_navigation.sidebar.return_value = sidebar_mock
    receive_cfa_view_model.on_error(mock_error)
    sidebar_mock.my_fungibles.setChecked.assert_called_once_with(True)
