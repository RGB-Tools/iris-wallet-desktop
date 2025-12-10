"""Unit test for RGB Asset transaction Detail ui."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication

from src.model.enums.enums_model import PaymentStatus
from src.model.enums.enums_model import TransferStatusEnumModel
from src.model.rgb_model import RgbAssetPageLoadModel
from src.model.rgb_model import TransportEndpoint
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_rgb_asset_transaction_detail import RGBAssetTransactionDetail


@pytest.fixture
def rgb_asset_transaction_detail_widget(qtbot):
    """Fixture to initialize the RGBAssetTransactionDetail widget."""
    mock_navigation = MagicMock()
    view_model = MagicMock(
        MainViewModel(
            mock_navigation,
        ),
    )  # Mock the view model

    # Create a mock for TransactionDetailPageModel with required attributes
    params = MagicMock(spec=TransactionDetailPageModel)
    params.tx_id = 'abcdx1234'
    params.amount = '0.01 BTC'
    params.asset_id = 'asset_1234'
    params.image_path = None
    params.asset_name = 'bitcoin'
    params.confirmation_date = '2024-09-30'
    params.confirmation_time = '10:40 AM'
    params.updated_date = '2024-09-30'
    params.updated_time = '10:40 AM'
    params.transaction_status = TransferStatusEnumModel.RECEIVE
    params.transfer_status = TransferStatusEnumModel.ON_GOING_TRANSFER
    params.consignment_endpoints = [
        TransportEndpoint(
            endpoint='endpoint_1',
            transport_type='type_1', used=False,
        ),
        TransportEndpoint(
            endpoint='endpoint_2', transport_type='type_2', used=True,
        ),
    ]
    params.recipient_id = 'recipient_124'
    params.receive_utxo = 'utxo_1234'
    params.change_utxo = 'utxo_4567'
    params.asset_type = 'NIA'
    params.is_off_chain = False  # Add the missing attribute

    # Initialize the widget
    widget = RGBAssetTransactionDetail(view_model, params)
    qtbot.add_widget(widget)  # Add widget to qtbot for proper cleanup
    return widget


def test_retranslate_ui(rgb_asset_transaction_detail_widget: RGBAssetTransactionDetail, qtbot):
    """Test the retranslate_ui method."""
    rgb_asset_transaction_detail_widget.retranslate_ui()

    expected_tx_id_text = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'transaction_id', None,
    )

    expected_blinded_utxo_text = QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'amount', None,
    )

    assert rgb_asset_transaction_detail_widget.tx_id_label.text() == expected_tx_id_text
    assert rgb_asset_transaction_detail_widget.rgb_amount_label.text(
    ) == expected_blinded_utxo_text


def test_set_rgb_asset_value(rgb_asset_transaction_detail_widget: RGBAssetTransactionDetail, qtbot):
    """Test the set_rgb_asset_value method."""

    # Ensure widget is reset before testing
    rgb_asset_transaction_detail_widget.params.confirmation_date = None
    rgb_asset_transaction_detail_widget.params.confirmation_time = None
    rgb_asset_transaction_detail_widget.date_value.setText(
        '',
    )  # Clear any previous text

    # Set transfer status to INTERNAL for testing
    rgb_asset_transaction_detail_widget.params.transfer_status = TransferStatusEnumModel.INTERNAL
    # Empty consignment_endpoints to simulate 'N/A' value
    rgb_asset_transaction_detail_widget.params.consignment_endpoints = []

    # Mock load_stylesheet function if used
    with patch('src.views.ui_rgb_asset_transaction_detail.load_stylesheet', return_value='mocked_stylesheet'):
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()

    # Check that the asset name and amount are set correctly
    assert rgb_asset_transaction_detail_widget.rgb_asset_name_value.text(
    ) == rgb_asset_transaction_detail_widget.params.asset_name
    assert rgb_asset_transaction_detail_widget.amount_value.text(
    ) == rgb_asset_transaction_detail_widget.params.amount

    # Now test the case when the transfer status is SENT
    rgb_asset_transaction_detail_widget.params.transfer_status = TransferStatusEnumModel.SENT
    with patch('src.views.ui_rgb_asset_transaction_detail.load_stylesheet', return_value='mocked_stylesheet'):
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()

    # Ensure the style sheet is applied
    expected_style = "font: 24px \"Inter\";\ncolor: #798094;\nbackground: transparent;\nborder: none;\nfont-weight: 600;"
    actual_style = rgb_asset_transaction_detail_widget.amount_value.styleSheet(
    ).strip()  # Normalize whitespace
    assert actual_style == expected_style.strip()

    # Test case when both confirmation_date and confirmation_time are provided
    rgb_asset_transaction_detail_widget.params.confirmation_date = '2024-12-29'
    rgb_asset_transaction_detail_widget.params.confirmation_time = '12:34:56'

    # Update the widget after setting parameters
    with patch('src.views.ui_rgb_asset_transaction_detail.load_stylesheet', return_value='mocked_stylesheet'):
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()

    # Ensure the concatenated date and time are set correctly
    expected_date_time_concat = f'{rgb_asset_transaction_detail_widget.params.confirmation_date} | {
        rgb_asset_transaction_detail_widget.params.confirmation_time
    }'
    assert rgb_asset_transaction_detail_widget.date_value.text() == expected_date_time_concat

    # Test case when confirmation_date is missing
    rgb_asset_transaction_detail_widget.params.confirmation_date = None
    rgb_asset_transaction_detail_widget.params.confirmation_time = '10:40 AM'
    with patch('src.views.ui_rgb_asset_transaction_detail.load_stylesheet', return_value='mocked_stylesheet'):
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()
    assert rgb_asset_transaction_detail_widget.date_label.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
    )
    assert rgb_asset_transaction_detail_widget.date_value.text(
    ) == rgb_asset_transaction_detail_widget.params.transaction_status

    # Test case when confirmation_time is missing
    rgb_asset_transaction_detail_widget.params.confirmation_date = '2024-09-30'
    rgb_asset_transaction_detail_widget.params.confirmation_time = None
    with patch('src.views.ui_rgb_asset_transaction_detail.load_stylesheet', return_value='mocked_stylesheet'):
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()
    assert rgb_asset_transaction_detail_widget.date_label.text() == QCoreApplication.translate(
        IRIS_WALLET_TRANSLATIONS_CONTEXT, 'status', None,
    )
    assert rgb_asset_transaction_detail_widget.date_value.text(
    ) == rgb_asset_transaction_detail_widget.params.transaction_status

    # Test case for is_off_chain condition
    # Set the parameter to True for the test
    rgb_asset_transaction_detail_widget.params.is_off_chain = True
    with patch.object(rgb_asset_transaction_detail_widget, 'handle_lightning_detail') as mock_handle_lightning_detail:
        rgb_asset_transaction_detail_widget.set_rgb_asset_value()
        # Ensure the method handle_lightning_detail is called
        mock_handle_lightning_detail.assert_called_once()

    # Reset is_off_chain for other tests
    rgb_asset_transaction_detail_widget.params.is_off_chain = False


def test_handle_lightning_detail(rgb_asset_transaction_detail_widget: RGBAssetTransactionDetail, qtbot):
    """Test the handle_lightning_detail method."""

    # Mock necessary parameters
    rgb_asset_transaction_detail_widget.params.transaction_status = PaymentStatus.SUCCESS.value
    rgb_asset_transaction_detail_widget.params.inbound = True  # Received transaction
    rgb_asset_transaction_detail_widget.params.confirmation_date = '2024-12-29'
    rgb_asset_transaction_detail_widget.params.confirmation_time = '12:34:56'
    rgb_asset_transaction_detail_widget.params.updated_date = '2024-12-30'
    rgb_asset_transaction_detail_widget.params.updated_time = '10:40:00'
    rgb_asset_transaction_detail_widget.tx_id = 'test_payment_hash'

    # Test case for successful received transaction
    rgb_asset_transaction_detail_widget.handle_lightning_detail()
    assert rgb_asset_transaction_detail_widget.amount_value.styleSheet(
    ) == 'color:#01A781;font-weight: 600'
    assert rgb_asset_transaction_detail_widget.tx_id_value.text() == 'test_payment_hash'
    assert rgb_asset_transaction_detail_widget.tx_id_value.styleSheet() == 'color:#01A781;'
    assert rgb_asset_transaction_detail_widget.date_value.text() == '2024-12-29 | 12:34:56'
    assert rgb_asset_transaction_detail_widget.blinded_utxo_value.text(
    ) == '2024-12-30 | 10:40:00'
    assert rgb_asset_transaction_detail_widget.unblinded_and_change_utxo_value.text(
    ) == PaymentStatus.SUCCESS.value

    # Test case for successful sent transaction
    rgb_asset_transaction_detail_widget.params.inbound = False
    rgb_asset_transaction_detail_widget.handle_lightning_detail()
    assert rgb_asset_transaction_detail_widget.amount_value.styleSheet(
    ) == 'color:#EB5A5A;font-weight: 600'

    # Test case for pending transaction
    rgb_asset_transaction_detail_widget.params.transaction_status = PaymentStatus.PENDING.value
    rgb_asset_transaction_detail_widget.handle_lightning_detail()
    assert rgb_asset_transaction_detail_widget.amount_value.styleSheet(
    ) == 'color:#959BAE;font-weight: 600'

    # Verify hidden elements
    assert not rgb_asset_transaction_detail_widget.consignment_endpoints_label.isVisible()
    assert not rgb_asset_transaction_detail_widget.consignment_endpoints_value.isVisible()

    # Verify widget sizing adjustments
    assert rgb_asset_transaction_detail_widget.rgb_asset_single_transaction_detail_widget.minimumHeight() == 650
    assert rgb_asset_transaction_detail_widget.rgb_asset_single_transaction_detail_widget.maximumHeight() == 650
    assert rgb_asset_transaction_detail_widget.transaction_detail_frame.minimumHeight() == 400
    assert rgb_asset_transaction_detail_widget.transaction_detail_frame.maximumHeight() == 400


def test_handle_close(rgb_asset_transaction_detail_widget: RGBAssetTransactionDetail, qtbot):
    """Test the handle_close method."""

    # Mock the required parameters in widget.params
    rgb_asset_transaction_detail_widget.params.asset_id = '123'
    rgb_asset_transaction_detail_widget.params.asset_name = 'Test Asset'
    rgb_asset_transaction_detail_widget.params.image_path = 'path/to/image'
    rgb_asset_transaction_detail_widget.params.asset_type = 'Test Type'

    # Mock the view model methods (signal and navigation)
    rgb_asset_transaction_detail_widget._view_model.cfa_view_model.asset_info = MagicMock()
    rgb_asset_transaction_detail_widget._view_model.page_navigation.cfa_detail_page = MagicMock()

    # Call the method to test
    rgb_asset_transaction_detail_widget.handle_close()

    # Assert that the signal is emitted with the correct parameters
    rgb_asset_transaction_detail_widget._view_model.cfa_view_model.asset_info.emit.assert_called_once_with(
        '123', 'Test Asset', 'path/to/image', 'Test Type',
    )

    # Assert that the navigation method is called with the correct argument
    rgb_asset_transaction_detail_widget._view_model.page_navigation.cfa_detail_page.assert_called_once_with(
        RgbAssetPageLoadModel(asset_type='Test Type'),
    )
