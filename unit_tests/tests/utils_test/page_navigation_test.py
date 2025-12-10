# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument, protected-access
"""Unit tests for the PageNavigation class."""
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.model.rgb_model import RgbAssetPageLoadModel
from src.model.selection_page_model import SelectionPageModel
from src.model.success_model import SuccessPageModel
from src.model.transaction_detail_page_model import TransactionDetailPageModel
from src.utils.page_navigation import PageNavigation
from src.utils.page_navigation_events import PageNavigationEventManager
from src.views.main_window import MainWindow


@pytest.fixture
def mock_ui():
    """Mock the MainWindow UI."""
    mock_ui = MagicMock(spec=MainWindow)
    mock_ui.sidebar = MagicMock()
    mock_ui.stacked_widget = MagicMock()
    mock_ui.view_model = MagicMock()
    return mock_ui


@pytest.fixture
def mock_event_manager():
    """Mock the PageNavigationEventManager."""
    event_manager = MagicMock(spec=PageNavigationEventManager)
    event_manager.get_instance.return_value = event_manager
    return event_manager


@pytest.fixture
def page_navigation(mock_ui, mock_event_manager):
    """Create an instance of PageNavigation with mocked dependencies."""
    navigation = PageNavigation(mock_ui)
    # Mock all page widgets
    for page_name in navigation.pages:
        navigation.pages[page_name] = MagicMock(return_value=MagicMock())
    return navigation


def test_ln_endpoint_page(page_navigation):
    """Test ln_endpoint_page navigation."""
    originating_page = 'test_page'
    page_navigation.ln_endpoint_page(originating_page)

    assert page_navigation.current_stack['name'] == 'LnEndpoint'
    assert isinstance(page_navigation.current_stack['widget'], MagicMock)


def test_splash_screen_page(page_navigation):
    """Test splash_screen_page navigation."""
    page_navigation.splash_screen_page()

    assert page_navigation.current_stack['name'] == 'SplashScreenWidget'


def test_wallet_method_page(page_navigation):
    """Test wallet_method_page navigation."""
    params = MagicMock(spec=SelectionPageModel)
    page_navigation.wallet_method_page(params)

    assert page_navigation.current_stack['name'] == 'WalletOrTransferSelectionWidget'


def test_network_selection_page(page_navigation):
    """Test network_selection_page navigation."""
    originating_page = 'test_page'
    network = 'testnet'
    page_navigation.network_selection_page(originating_page, network)

    assert page_navigation.current_stack['name'] == 'NetworkSelectionWidget'


def test_wallet_connection_page(page_navigation):
    """Test wallet_connection_page navigation."""
    params = MagicMock(spec=SelectionPageModel)
    page_navigation.wallet_connection_page(params)

    assert page_navigation.current_stack['name'] == 'WalletConnectionTypePage'


def test_welcome_page(page_navigation):
    """Test welcome_page navigation."""
    page_navigation.welcome_page()

    assert page_navigation.current_stack['name'] == 'Welcome'


def test_term_and_condition_page(page_navigation):
    """Test term_and_condition_page navigation."""
    page_navigation.term_and_condition_page()

    assert page_navigation.current_stack['name'] == 'TermCondition'


def test_fungibles_asset_page(page_navigation):
    """Test fungibles_asset_page navigation."""
    page_navigation.fungibles_asset_page()

    assert page_navigation.current_stack['name'] == 'FungibleAssetWidget'


def test_collectibles_asset_page(page_navigation):
    """Test collectibles_asset_page navigation."""
    page_navigation.collectibles_asset_page()

    assert page_navigation.current_stack['name'] == 'CollectiblesAssetWidget'


def test_set_wallet_password_page(page_navigation):
    """Test set_wallet_password_page navigation."""
    params = MagicMock()
    page_navigation.set_wallet_password_page(params)

    assert page_navigation.current_stack['name'] == 'SetWalletPassword'


def test_enter_wallet_password_page(page_navigation):
    """Test enter_wallet_password_page navigation."""
    page_navigation.enter_wallet_password_page()

    assert page_navigation.current_stack['name'] == 'EnterWalletPassword'


def test_issue_nia_asset_page(page_navigation):
    """Test issue_nia_asset_page navigation."""
    page_navigation.issue_nia_asset_page()

    assert page_navigation.current_stack['name'] == 'IssueNIA'


def test_bitcoin_page(page_navigation):
    """Test bitcoin_page navigation."""
    page_navigation.bitcoin_page()

    assert page_navigation.current_stack['name'] == 'Bitcoin'


def test_issue_cfa_asset_page(page_navigation):
    """Test issue_cfa_asset_page navigation."""
    page_navigation.issue_cfa_asset_page()

    assert page_navigation.current_stack['name'] == 'IssueCFA'


def test_send_cfa_page(page_navigation):
    """Test send_cfa_page navigation."""
    page_navigation.send_cfa_page()

    assert page_navigation.current_stack['name'] == 'SendCFA'


def test_receive_cfa_page(page_navigation):
    """Test receive_cfa_page navigation."""
    params = MagicMock()
    page_navigation.receive_cfa_page(params)

    assert page_navigation.current_stack['name'] == 'ReceiveCFA'


def test_cfa_detail_page(page_navigation):
    """Test cfa_detail_page navigation."""
    params = MagicMock(spec=RgbAssetPageLoadModel)
    page_navigation.cfa_detail_page(params)

    assert page_navigation.current_stack['name'] == 'CFADetail'


def test_send_bitcoin_page(page_navigation):
    """Test send_bitcoin_page navigation."""
    page_navigation.send_bitcoin_page()

    assert page_navigation.current_stack['name'] == 'SendBitcoin'


def test_receive_bitcoin_page(page_navigation):
    """Test receive_bitcoin_page navigation."""
    page_navigation.receive_bitcoin_page()

    assert page_navigation.current_stack['name'] == 'ReceiveBitcoin'


def test_channel_management_page(page_navigation):
    """Test channel_management_page navigation."""
    page_navigation.channel_management_page()

    assert page_navigation.current_stack['name'] == 'ChannelManagement'


def test_create_channel_page(page_navigation):
    """Test create_channel_page navigation."""
    page_navigation.create_channel_page()

    assert page_navigation.current_stack['name'] == 'CreateChannel'


def test_view_unspent_list_page(page_navigation):
    """Test view_unspent_list_page navigation."""
    page_navigation.view_unspent_list_page()

    assert page_navigation.current_stack['name'] == 'ViewUnspentList'


def test_cfa_transaction_detail_page(page_navigation):
    """Test cfa_transaction_detail_page navigation."""
    params = MagicMock(spec=TransactionDetailPageModel)
    page_navigation.cfa_transaction_detail_page(params)

    assert page_navigation.current_stack['name'] == 'CFATransactionDetail'


def test_bitcoin_transaction_detail_page(page_navigation):
    """Test bitcoin_transaction_detail_page navigation."""
    params = MagicMock(spec=TransactionDetailPageModel)
    page_navigation.bitcoin_transaction_detail_page(params)

    assert page_navigation.current_stack['name'] == 'BitcoinTransactionDetail'


def test_backup_page(page_navigation):
    """Test backup_page navigation."""
    page_navigation.backup_page()

    assert page_navigation.current_stack['name'] == 'Backup'


def test_swap_page(page_navigation):
    """Test swap_page navigation."""
    page_navigation.swap_page()

    assert page_navigation.current_stack['name'] == 'Swap'


def test_settings_page(page_navigation):
    """Test settings_page navigation."""
    page_navigation.settings_page()

    assert page_navigation.current_stack['name'] == 'Settings'


def test_create_ln_invoice_page(page_navigation):
    """Test create_ln_invoice_page navigation."""
    params = MagicMock()
    asset_name = 'test_asset'
    asset_type = 'test_type'
    page_navigation.create_ln_invoice_page(params, asset_name, asset_type)

    assert page_navigation.current_stack['name'] == 'CreateLnInvoiceWidget'


def test_send_ln_invoice_page(page_navigation):
    """Test send_ln_invoice_page navigation."""
    asset_type = 'test_type'
    page_navigation.send_ln_invoice_page(asset_type)

    assert page_navigation.current_stack['name'] == 'SendLnInvoiceWidget'


def test_show_success_page(page_navigation):
    """Test show_success_page navigation."""
    params = MagicMock(spec=SuccessPageModel)
    page_navigation.show_success_page(params)

    assert page_navigation.current_stack['name'] == 'SuccessWidget'


def test_about_page(page_navigation):
    """Test about_page navigation."""
    page_navigation.about_page()

    assert page_navigation.current_stack['name'] == 'AboutWidget'


def test_faucets_page(page_navigation):
    """Test faucets_page navigation."""
    page_navigation.faucets_page()

    assert page_navigation.current_stack['name'] == 'FaucetsWidget'


def test_help_page(page_navigation):
    """Test help_page navigation."""
    page_navigation.help_page()

    assert page_navigation.current_stack['name'] == 'HelpWidget'


def test_sidebar(page_navigation, mock_ui):
    """Test sidebar method."""
    result = page_navigation.sidebar()
    assert result == mock_ui.sidebar


def test_error_report_dialog_box(page_navigation):
    """Test error_report_dialog_box method."""
    with patch('src.utils.page_navigation.ErrorReportDialog') as mock_dialog:
        mock_dialog_instance = MagicMock()
        mock_dialog.return_value = mock_dialog_instance

        # Call the method we're testing
        page_navigation.error_report_dialog_box()

        # Verify the dialog was created
        mock_dialog.assert_called_once()

        # Verify the dialog was shown
        mock_dialog_instance.exec.assert_called_once()
