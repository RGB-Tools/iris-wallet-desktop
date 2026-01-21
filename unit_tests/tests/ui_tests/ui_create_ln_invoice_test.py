"""Unit test for Create LN Invoice UI."""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked objects in test functions
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from PySide6.QtCore import QCoreApplication

from src.model.enums.enums_model import AssetType
from src.utils.constant import IRIS_WALLET_TRANSLATIONS_CONTEXT
from src.viewmodels.ln_offchain_view_model import LnOffChainViewModel
from src.viewmodels.main_view_model import MainViewModel
from src.views.ui_create_ln_invoice import CreateLnInvoiceWidget


@pytest.fixture
def create_ln_invoice_page_navigation():
    """Fixture to create a mocked page navigation object."""
    mock_navigation = MagicMock()
    return mock_navigation


@pytest.fixture
def mock_create_ln_invoice_view_model(create_ln_invoice_page_navigation):
    """Fixture to create a MainViewModel instance with mocked channel view model."""
    mock_view_model = MagicMock(
        spec=MainViewModel(
            create_ln_invoice_page_navigation,
        ),
    )
    mock_view_model.channel_view_model = MagicMock(
        spec=LnOffChainViewModel(create_ln_invoice_page_navigation),
    )
    return mock_view_model


@pytest.fixture
def create_ln_invoice_widget(qtbot, mock_create_ln_invoice_view_model):
    """Fixture to create a CreateLnInvoiceWidget instance."""

    # Provide values for asset_name and asset_type
    asset_name = 'Bitcoin'  # Replace with the actual name if needed
    asset_type = 'BTC'  # Replace with the actual asset type if needed

    # Mock the NodeInfoModel and its node_info property
    mock_node_info = MagicMock()
    mock_node_info.rgb_htlc_min_msat = 1000  # Mock the required attribute

    mock_node_info_model = MagicMock()
    mock_node_info_model.node_info = mock_node_info

    # Mock the NodeInfoModel constructor to return the mocked instance
    with patch('src.views.ui_create_ln_invoice.NodeInfoModel', return_value=mock_node_info_model):
        # Initialize the widget with all required arguments
        widget = CreateLnInvoiceWidget(
            mock_create_ln_invoice_view_model, asset_id=AssetType.BITCOIN.value, asset_name=asset_name, asset_type=asset_type,
        )

    qtbot.addWidget(widget)
    return widget


def test_initial_ui_state(create_ln_invoice_widget):
    """Test the initial state of the UI elements in CreateLnInvoiceWidget."""
    widget = create_ln_invoice_widget
    assert widget.amount_input.text() == ''
    assert widget.expiry_input.text() == '3'
    assert not widget.create_button.isEnabled()


def test_amount_input_enable_button(qtbot, create_ln_invoice_widget):
    """Test enabling the create button when amount input is provided."""
    widget = create_ln_invoice_widget
    qtbot.keyClicks(widget.amount_input, '1000')
    qtbot.keyClicks(widget.expiry_input, '3600')
    assert widget.create_button.isEnabled()


def test_expiry_input_enable_button(qtbot, create_ln_invoice_widget):
    """Test enabling the create button when expiry input is provided."""
    widget = create_ln_invoice_widget
    qtbot.keyClicks(widget.expiry_input, '3600')
    qtbot.keyClicks(widget.amount_input, '1000')
    assert widget.create_button.isEnabled()


def test_close_button_navigation(mock_create_ln_invoice_view_model, create_ln_invoice_widget, qtbot):
    """Test navigation when the close button is clicked."""
    widget = create_ln_invoice_widget
    # Mock the page navigation method
    mock_method = mock_create_ln_invoice_view_model.page_navigation.fungibles_asset_page
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            mock_create_ln_invoice_view_model.page_navigation,
            'fungibles_asset_page', mock_method,
        )
        widget.close_btn_ln_invoice_page.click()
        assert mock_method.called


def test_get_ln_invoice(mock_create_ln_invoice_view_model, create_ln_invoice_widget, qtbot):
    """Test calling get_invoice method with correct parameters."""

    # Create the widget and simulate user input
    widget = create_ln_invoice_widget
    widget.msat_amount_value = MagicMock()
    widget.amount_input = MagicMock()
    widget.expiry_input = MagicMock()
    widget.time_unit_combobox = MagicMock()
    widget.render_timer = MagicMock()
    widget.amt_msat_value = 'amt_msat'

    # Set up mock return values
    widget.amount_input.text.return_value = '1000'
    widget.expiry_input.text.return_value = '3600'
    widget.time_unit_combobox.currentText.return_value = 'minutes'

    # Mock the view model method to check if it was called correctly
    mock_method = MagicMock()
    mock_create_ln_invoice_view_model.ln_offchain_view_model.get_invoice = mock_method

    # Mock get_expiry_time_in_seconds
    widget.get_expiry_time_in_seconds = MagicMock(return_value=216000)

    # Test case when asset_id is Bitcoin
    widget.asset_id = AssetType.BITCOIN.value
    widget.msat_amount_value.text.return_value = ''  # Empty MSAT value for Bitcoin
    widget.get_ln_invoice()

    # Check Bitcoin case uses amount_msat (converted from amount)
    _, kwargs = mock_method.call_args
    assert 'amount_msat' in kwargs
    assert kwargs['amount_msat'] == '1000'
    assert kwargs['expiry'] == 216000  # Expiry time in seconds (3600 * 60)

    # Test case when asset_id is not Bitcoin and msat_amount_value is empty
    widget.asset_id = 'OTHER'
    widget.msat_amount_value.text.return_value = ''  # Empty MSAT value
    widget.get_ln_invoice()

    # Check non-Bitcoin case with empty msat uses amount_input converted to msat
    _, kwargs = mock_method.call_args
    assert 'amount_msat' in kwargs
    assert kwargs['amount'] == '1000'
    assert kwargs['asset_id'] == 'OTHER'
    assert kwargs['expiry'] == 216000

    # Test case when asset_id is not Bitcoin and msat_amount_value is set
    widget.msat_amount_value.text.return_value = '2000'  # Set MSAT value
    widget.get_ln_invoice()

    # Check non-Bitcoin case uses msat_amount_value when available
    _, kwargs = mock_method.call_args
    assert 'amount_msat' in kwargs
    assert kwargs['amount_msat'] == 2000000

    # Test page navigation after invoice creation
    mock_page_navigation = MagicMock()
    widget._view_model.page_navigation.receive_cfa_page = mock_page_navigation

    widget.get_ln_invoice()
    mock_page_navigation.assert_called_once()


def test_get_max_asset_remote_balance(create_ln_invoice_widget, mock_create_ln_invoice_view_model):
    """Test the get_max_asset_remote_balance function."""

    # Create mock channels with various attributes
    mock_channel_1 = MagicMock()
    mock_channel_1.asset_id = 'BTC'
    mock_channel_1.is_usable = True
    mock_channel_1.ready = True
    mock_channel_1.asset_remote_amount = 1000

    mock_channel_2 = MagicMock()
    mock_channel_2.asset_id = 'BTC'
    mock_channel_2.is_usable = True
    mock_channel_2.ready = True
    mock_channel_2.asset_remote_amount = 1500

    mock_channel_3 = MagicMock()
    mock_channel_3.asset_id = 'BTC'
    mock_channel_3.is_usable = False  # Not usable
    mock_channel_3.ready = False  # Not ready

    mock_channel_4 = MagicMock()
    mock_channel_4.asset_id = 'ETH'  # Different asset_id
    mock_channel_4.is_usable = True
    mock_channel_4.ready = True
    mock_channel_4.asset_remote_amount = 2000

    # Assign the channels to the view model
    mock_create_ln_invoice_view_model.channel_view_model.channels = [
        mock_channel_1, mock_channel_2, mock_channel_3, mock_channel_4,
    ]

    # Set asset_id to BTC and initialize the class
    create_ln_invoice_widget.asset_id = 'BTC'

    # Call the method
    create_ln_invoice_widget.get_max_asset_remote_balance()

    # Check that the max_asset_local_amount is updated to the correct maximum
    assert create_ln_invoice_widget.max_asset_local_amount == 1500


def test_validate_asset_amount(create_ln_invoice_widget, mock_create_ln_invoice_view_model, qtbot):
    """Test the validate_asset_amount function."""

    # Mock a non-Bitcoin asset
    create_ln_invoice_widget.asset_id = 'LTC'  # Assume "LTC" is not Bitcoin
    create_ln_invoice_widget.max_asset_local_amount = 1000  # Set a max asset balance

    # Test with an empty amount input
    # Clear the input to simulate empty input
    create_ln_invoice_widget.amount_input.clear()
    create_ln_invoice_widget.validate_asset_amount()
    # Check if the validation label is hidden (as input is empty)
    assert create_ln_invoice_widget.asset_balance_validation_label.isHidden()

    # Test when amount is less than max_asset_local_amount
    qtbot.keyClicks(
        create_ln_invoice_widget.amount_input,
        '500',
    )  # Enter an amount less than max
    create_ln_invoice_widget.validate_asset_amount()
    # Check if the validation label is hidden (as the amount is within the limit)
    assert create_ln_invoice_widget.asset_balance_validation_label.isHidden()

    # Test when amount is greater than max_asset_local_amount
    qtbot.keyClicks(
        create_ln_invoice_widget.amount_input,
        '1500',
    )  # Enter an amount greater than max
    create_ln_invoice_widget.validate_asset_amount()
    # Check if the validation label is shown (as the amount exceeds the balance)
    assert not create_ln_invoice_widget.asset_balance_validation_label.isHidden()

    # Test when amount is equal to max_asset_local_amount
    qtbot.keyClicks(
        create_ln_invoice_widget.amount_input,
        '1000',
    )  # Enter an amount equal to max
    create_ln_invoice_widget.validate_asset_amount()
    # Check if the validation label is hidden (as the amount is within the limit)
    assert not create_ln_invoice_widget.asset_balance_validation_label.isVisible()

    # Test when max_asset_local_amount is None (should hide the validation label)
    create_ln_invoice_widget.max_asset_local_amount = None
    qtbot.keyClicks(create_ln_invoice_widget.amount_input, '500')
    create_ln_invoice_widget.validate_asset_amount()
    # Check if the validation label is hidden (since max_asset_local_amount is None)
    assert create_ln_invoice_widget.asset_balance_validation_label.isHidden()


def test_get_expiry_time_in_seconds(create_ln_invoice_widget, qtbot):
    """Test the get_expiry_time_in_seconds function."""

    # Test case when the unit is 'minutes'
    create_ln_invoice_widget.expiry_input.setText('5')  # Set expiry input to 5
    create_ln_invoice_widget.time_unit_combobox.setCurrentText(
        'minutes',
    )  # Select "Minutes"
    expiry_time = create_ln_invoice_widget.get_expiry_time_in_seconds()
    assert expiry_time == 5 * 60  # 5 minutes in seconds, should be 300

    # Test case when the unit is 'hours'
    create_ln_invoice_widget.expiry_input.setText('2')  # Set expiry input to 2
    create_ln_invoice_widget.time_unit_combobox.setCurrentText(
        'hours',
    )  # Select "Hours"
    expiry_time = create_ln_invoice_widget.get_expiry_time_in_seconds()
    assert expiry_time == 2 * 3600  # 2 hours in seconds, should be 7200

    # Test case when the unit is 'days'
    create_ln_invoice_widget.expiry_input.setText('1')  # Set expiry input to 1
    create_ln_invoice_widget.time_unit_combobox.setCurrentText(
        'days',
    )  # Select "Days"
    expiry_time = create_ln_invoice_widget.get_expiry_time_in_seconds()
    assert expiry_time == 1 * 86400  # 1 day in seconds, should be 86400

    # Test case when the expiry input is empty (should return 0)
    create_ln_invoice_widget.expiry_input.setText('')  # Clear expiry input
    create_ln_invoice_widget.time_unit_combobox.setCurrentText(
        'minutes',
    )  # Select "Minutes"
    expiry_time = create_ln_invoice_widget.get_expiry_time_in_seconds()
    assert expiry_time == 0  # Empty input should return 0


def test_msat_value_is_valid(create_ln_invoice_widget):
    """Test the msat_value_is_valid function."""

    # Mock channels
    mock_channel_1 = MagicMock()
    mock_channel_1.asset_id = 'BTC'
    mock_channel_1.is_usable = True
    mock_channel_1.ready = True
    mock_channel_1.inbound_balance_msat = 7000000  # 7,000,000 msat

    mock_channel_2 = MagicMock()
    mock_channel_2.asset_id = 'BTC'
    mock_channel_2.is_usable = True
    mock_channel_2.ready = True
    mock_channel_2.inbound_balance_msat = 10000000  # 10,000,000 msat

    mock_channel_3 = MagicMock()
    mock_channel_3.asset_id = 'BTC'
    mock_channel_3.is_usable = False
    mock_channel_3.ready = False
    mock_channel_3.inbound_balance_msat = 5000000  # Should be ignored

    create_ln_invoice_widget._view_model.channel_view_model.channels = [
        mock_channel_1,
        mock_channel_2,
        mock_channel_3,
    ]
    create_ln_invoice_widget.asset_id = 'BTC'
    create_ln_invoice_widget.node_info.rgb_htlc_min_msat = 3000000  # 3,000,000 msat

    # Mock error label
    create_ln_invoice_widget.msat_error_label = MagicMock()

    # Test case: Valid MSAT value within bounds
    create_ln_invoice_widget.amt_msat_value = 5000  # 5,000 msat
    assert create_ln_invoice_widget.msat_value_is_valid() is True
    create_ln_invoice_widget.msat_error_label.hide.assert_called()

    # Test case: MSAT value below minimum bound
    create_ln_invoice_widget.amt_msat_value = 2000  # 2,000 msat
    assert create_ln_invoice_widget.msat_value_is_valid() is False
    create_ln_invoice_widget.msat_error_label.setText.assert_called_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_lower_bound_limit', None,
        ).format(create_ln_invoice_widget.node_info.rgb_htlc_min_msat // 1000),
    )
    create_ln_invoice_widget.msat_error_label.show.assert_called()

    # Test case: MSAT value exceeds maximum inbound balance
    create_ln_invoice_widget.amt_msat_value = 12000  # 12,000 msat
    assert create_ln_invoice_widget.msat_value_is_valid() is False
    create_ln_invoice_widget.msat_error_label.setText.assert_called_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_uper_bound_limit', None,
        ).format(10000),  # max_inbound_balance // 1000
    )
    create_ln_invoice_widget.msat_error_label.show.assert_called()

    # Test case: No usable or ready channels
    mock_channel_1.is_usable = False
    mock_channel_2.is_usable = False
    create_ln_invoice_widget.amt_msat_value = 5000  # 5,000 msat
    assert create_ln_invoice_widget.msat_value_is_valid() is False
    create_ln_invoice_widget.msat_error_label.setText.assert_called_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'msat_uper_bound_limit', None,
        ).format(0),
    )
    create_ln_invoice_widget.msat_error_label.show.assert_called()

    # Test case: Valid MSAT value again
    mock_channel_1.is_usable = True
    create_ln_invoice_widget.amt_msat_value = 7000  # 7,000 msat
    assert create_ln_invoice_widget.msat_value_is_valid() is True
    create_ln_invoice_widget.msat_error_label.hide.assert_called()


def test_handle_bitcoin_layout(create_ln_invoice_widget):
    """Test the handle_bitcoin_layout method."""
    create_ln_invoice_widget.asset_id = None  # Default value
    create_ln_invoice_widget.asset_name_label = MagicMock()
    create_ln_invoice_widget.asset_name_value = MagicMock()
    create_ln_invoice_widget.msat_amount_label = MagicMock()
    create_ln_invoice_widget.msat_amount_value = MagicMock()
    create_ln_invoice_widget.msat_error_label = MagicMock()
    create_ln_invoice_widget.asset_balance_validation_label = MagicMock()
    create_ln_invoice_widget.amount_label = MagicMock()
    create_ln_invoice_widget.amount_input = MagicMock()
    create_ln_invoice_widget._view_model = MagicMock()
    create_ln_invoice_widget.hide_create_ln_invoice_loader = MagicMock()
    # Test when asset_id is 'BITCOIN'
    create_ln_invoice_widget.asset_id = 'BITCOIN'
    create_ln_invoice_widget.handle_bitcoin_layout()

    # Verify UI elements are hidden for BITCOIN asset
    create_ln_invoice_widget.asset_name_label.hide.assert_called_once()
    create_ln_invoice_widget.asset_name_value.hide.assert_called_once()
    create_ln_invoice_widget.msat_amount_label.hide.assert_called_once()
    create_ln_invoice_widget.msat_amount_value.hide.assert_called_once()
    create_ln_invoice_widget.msat_error_label.hide.assert_called_once()
    create_ln_invoice_widget.asset_balance_validation_label.hide.assert_called_once()
    create_ln_invoice_widget.hide_create_ln_invoice_loader.assert_called_once()

    # Test when asset_id is not 'BITCOIN'
    create_ln_invoice_widget.asset_id = 'OTHER_ASSET'
    create_ln_invoice_widget.handle_bitcoin_layout()

    # Ensure that the available channels function is called
    create_ln_invoice_widget._view_model.channel_view_model.available_channels.assert_called_once()

    # Verify that channel_loaded connects to the correct functions
    create_ln_invoice_widget._view_model.channel_view_model.channel_loaded.connect.assert_any_call(
        create_ln_invoice_widget.get_max_asset_remote_balance,
    )
    create_ln_invoice_widget._view_model.channel_view_model.channel_loaded.connect.assert_any_call(
        create_ln_invoice_widget.hide_create_ln_invoice_loader,
    )

    # Verify the labels and placeholders are set for non-BITCOIN assets
    create_ln_invoice_widget.amount_label.setText.assert_called_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount', None,
        ),
    )
    create_ln_invoice_widget.amount_input.setPlaceholderText.assert_called_with(
        QCoreApplication.translate(
            IRIS_WALLET_TRANSLATIONS_CONTEXT, 'asset_amount', None,
        ),
    )


def test_on_close(create_ln_invoice_widget):
    """Test the on_close function."""

    # Mock page navigation methods
    create_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page = MagicMock()
    create_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page = MagicMock()

    # Test case when asset_type is CFA (should navigate to collectibles_asset_page)
    # Assuming AssetType.CFA.value is 'CFA'
    create_ln_invoice_widget.asset_type = 'CFA'
    create_ln_invoice_widget.on_close()

    # Check that collectibles_asset_page is called and fungibles_asset_page is not
    create_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_called_once()
    create_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_not_called()

    # Reset mocks to clear previous calls
    create_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.reset_mock()
    create_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.reset_mock()

    # Test case when asset_type is not CFA (should navigate to fungibles_asset_page)
    # Any asset type other than 'CFA'
    create_ln_invoice_widget.asset_type = 'OTHER_ASSET'
    create_ln_invoice_widget.on_close()

    # Check that fungibles_asset_page is called and collectibles_asset_page is not
    create_ln_invoice_widget._view_model.page_navigation.fungibles_asset_page.assert_called_once()
    create_ln_invoice_widget._view_model.page_navigation.collectibles_asset_page.assert_not_called()


def test_handle_button_enable(create_ln_invoice_widget):
    """Test the handle_button_enable function."""

    # Mock validation methods
    create_ln_invoice_widget.is_amount_valid = MagicMock(return_value=True)
    create_ln_invoice_widget.is_expiry_valid = MagicMock(return_value=True)
    create_ln_invoice_widget.is_msat_valid = MagicMock(return_value=True)
    create_ln_invoice_widget.is_amount_within_limit = MagicMock(
        return_value=True,
    )
    create_ln_invoice_widget.create_button = MagicMock()

    # Test case when amount and expiry are valid, and msat is valid
    create_ln_invoice_widget.is_amount_valid.return_value = True
    create_ln_invoice_widget.is_expiry_valid.return_value = True
    create_ln_invoice_widget.is_msat_valid.return_value = True
    create_ln_invoice_widget.is_amount_within_limit.return_value = True
    create_ln_invoice_widget.handle_button_enable()
    create_ln_invoice_widget.create_button.setDisabled.assert_called_with(
        False,
    )  # Button should be enabled

    # Reset mocks to clear previous calls
    create_ln_invoice_widget.create_button.setDisabled.reset_mock()

    # Test case when amount or expiry is invalid (button should be disabled)
    create_ln_invoice_widget.is_amount_valid.return_value = False
    create_ln_invoice_widget.handle_button_enable()
    create_ln_invoice_widget.create_button.setDisabled.assert_called_with(
        True,
    )  # Button should be disabled

    # Reset mocks to clear previous calls
    create_ln_invoice_widget.create_button.setDisabled.reset_mock()

    # Test case when asset_id is BITCOIN (button should still respect amount and expiry validation)
    create_ln_invoice_widget.asset_id = AssetType.BITCOIN.value
    create_ln_invoice_widget.is_amount_valid.return_value = True  # Valid amount
    create_ln_invoice_widget.is_expiry_valid.return_value = True  # Valid expiry
    create_ln_invoice_widget.handle_button_enable()
    create_ln_invoice_widget.create_button.setDisabled.assert_called_with(
        False,
    )  # Button should be enabled for BITCOIN with valid inputs

    # Reset mocks to clear previous calls
    create_ln_invoice_widget.create_button.setDisabled.reset_mock()

    # **Specific Test Case for msat invalid:**
    # Here is the core test where msat is invalid, and the method should disable the button and return early
    create_ln_invoice_widget.is_msat_valid.return_value = False  # Simulating invalid msat
    # Set asset_id to something other than BITCOIN
    create_ln_invoice_widget.asset_id = 'OTHER'
    create_ln_invoice_widget.handle_button_enable()

    # The button should be disabled and no other checks should have been executed.
    create_ln_invoice_widget.create_button.setDisabled.assert_called_with(
        True,
    )  # Button should be disabled due to invalid msat

    # Reset mocks to clear previous calls
    create_ln_invoice_widget.create_button.setDisabled.reset_mock()

    # Test case when amount is out of limit (button should be disabled)
    create_ln_invoice_widget.is_amount_within_limit.return_value = False
    create_ln_invoice_widget.handle_button_enable()
    create_ln_invoice_widget.create_button.setDisabled.assert_called_with(
        True,
    )  # Button should be disabled due to amount limit


def test_msat_value_change(create_ln_invoice_widget):
    """Test the msat_value_change function."""

    # Mock the relevant components
    create_ln_invoice_widget.msat_amount_value = MagicMock()
    create_ln_invoice_widget.msat_error_label = MagicMock()
    create_ln_invoice_widget.handle_button_enable = MagicMock()
    create_ln_invoice_widget.is_msat_valid = MagicMock()

    # Mock the channel_view_model and its channels attribute
    create_ln_invoice_widget._view_model.channel_view_model = MagicMock()
    create_ln_invoice_widget._view_model.channel_view_model.channels = []

    # Test case where there are no channels (should return immediately without any further action)
    # Valid MSAT value
    create_ln_invoice_widget.msat_amount_value.text.return_value = '10000000'
    create_ln_invoice_widget.msat_value_change()

    # Ensure handle_button_enable is not called since the channels list is empty
    create_ln_invoice_widget.handle_button_enable.assert_not_called()

    # Reset mocks for the next case
    create_ln_invoice_widget.msat_error_label.hide.reset_mock()
    create_ln_invoice_widget.msat_error_label.show.reset_mock()
    create_ln_invoice_widget.handle_button_enable.reset_mock()

    # Test case where asset_id is BITCOIN (no MSAT validation needed, error label hidden)
    create_ln_invoice_widget.asset_id = AssetType.BITCOIN.value
    # Valid MSAT value
    create_ln_invoice_widget.msat_amount_value.text.return_value = '10000000'
    create_ln_invoice_widget.msat_value_change()

    # Ensure the error label is hidden for Bitcoin
    create_ln_invoice_widget.msat_error_label.hide.assert_called_once()

    # Reset mocks for the next case
    create_ln_invoice_widget.msat_error_label.hide.reset_mock()
    create_ln_invoice_widget.msat_error_label.show.reset_mock()

    # Test case where MSAT field is empty (error label should hide)
    create_ln_invoice_widget.asset_id = 'OTHER'
    create_ln_invoice_widget.msat_amount_value.text.return_value = ''  # Empty MSAT value

    # Mock some channels for non-Bitcoin test cases
    mock_channel = MagicMock()
    mock_channel.asset_id = 'OTHER'
    mock_channel.is_usable = True
    mock_channel.ready = True
    mock_channel.inbound_balance_msat = 10000000
    create_ln_invoice_widget._view_model.channel_view_model.channels = [
        mock_channel,
    ]

    create_ln_invoice_widget.msat_value_change()

    # Ensure the error label is hidden for empty value
    create_ln_invoice_widget.msat_error_label.hide.assert_called_once()

    # Reset mocks for the next case
    create_ln_invoice_widget.msat_error_label.hide.reset_mock()
    create_ln_invoice_widget.msat_error_label.show.reset_mock()

    # Test case where MSAT value is below the minimum valid value (should show error label)
    # Invalid MSAT value
    create_ln_invoice_widget.msat_amount_value.text.return_value = '1000000'
    create_ln_invoice_widget.is_msat_valid.return_value = False  # Simulate invalid MSAT
    create_ln_invoice_widget.msat_value_change()

    # Ensure the error label is shown for invalid MSAT
    create_ln_invoice_widget.msat_error_label.show.assert_called_once()


def test_is_amount_within_limit(create_ln_invoice_widget):
    """Test the is_amount_within_limit method."""

    # Create the widget instance
    widget = create_ln_invoice_widget
    widget.amount_input.text = MagicMock()

    # Test case where max_asset_local_amount is None (should return True)
    widget.max_asset_local_amount = None  # Set max_asset_local_amount to None
    widget.amount_input.text.return_value = '5000'  # Simulate entering amount 5000
    result = widget.is_amount_within_limit()  # Call the method
    # The method should return True since max_asset_local_amount is None
    assert result is True

    # Test case where amount is less than max_asset_local_amount (should return True)
    widget.max_asset_local_amount = 10000  # Set max_asset_local_amount to 10000
    widget.amount_input.text.return_value = '5000'  # Simulate entering amount 5000
    result = widget.is_amount_within_limit()  # Call the method
    assert result is True  # The method should return True since 5000 <= 10000

    # Test case where amount is equal to max_asset_local_amount (should return True)
    widget.amount_input.text.return_value = '10000'  # Simulate entering amount 10000
    result = widget.is_amount_within_limit()  # Call the method
    assert result is True  # The method should return True since 10000 == 10000

    # Test case where amount is greater than max_asset_local_amount (should return False)
    widget.amount_input.text.return_value = '15000'  # Simulate entering amount 15000
    result = widget.is_amount_within_limit()  # Call the method
    assert result is False  # The method should return False since 15000 > 10000
