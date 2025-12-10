"""Unit test for main view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument,protected-access
from __future__ import annotations

from unittest.mock import MagicMock

from src.viewmodels.main_view_model import MainViewModel


def test_main_view_model_initialization():
    """Test if the MainViewModel initializes all page view models correctly."""

    # Mock the page navigation dependency
    mock_page_navigation = MagicMock()

    # Instantiate the MainViewModel
    view_model = MainViewModel(page_navigation=mock_page_navigation)

    # Assert that all view models are properly initialized
    assert view_model.welcome_view_model is not None
    assert view_model.terms_view_model is not None
    assert view_model.main_asset_view_model is not None
    assert view_model.issue_nia_asset_view_model is not None
    assert view_model.set_wallet_password_view_model is not None
    assert view_model.bitcoin_view_model is not None
    assert view_model.receive_bitcoin_view_model is not None
    assert view_model.send_bitcoin_view_model is not None
    assert view_model.channel_view_model is not None
    assert view_model.unspent_view_model is not None
    assert view_model.issue_cfa_asset_view_model is not None
    assert view_model.ln_endpoint_view_model is not None
    assert view_model.cfa_view_model is not None
    assert view_model.enter_wallet_password_view_model is not None
    assert view_model.receive_cfa_view_model is not None
    assert view_model.backup_view_model is not None
    assert view_model.setting_view_model is not None
    assert view_model.ln_offchain_view_model is not None
    assert view_model.splash_view_model is not None
    assert view_model.restore_view_model is not None
    assert view_model.wallet_transfer_selection_view_model is not None
    assert view_model.faucets_view_model is not None
    assert view_model.estimate_fee_view_model is not None

    # Verify page_navigation is properly set
    assert view_model.page_navigation == mock_page_navigation

    # Verify splash_view_model is passed to wallet_transfer_selection_view_model
    assert view_model.wallet_transfer_selection_view_model.splash_view_model == view_model.splash_view_model

    # Verify all view models are initialized with page_navigation
    assert view_model.welcome_view_model._page_navigation == mock_page_navigation
    assert view_model.terms_view_model._page_navigation == mock_page_navigation
    assert view_model.main_asset_view_model._page_navigation == mock_page_navigation
    assert view_model.issue_nia_asset_view_model._page_navigation == mock_page_navigation
    assert view_model.set_wallet_password_view_model._page_navigation == mock_page_navigation
    assert view_model.bitcoin_view_model._page_navigation == mock_page_navigation
    assert view_model.receive_bitcoin_view_model._page_navigation == mock_page_navigation
    assert view_model.send_bitcoin_view_model._page_navigation == mock_page_navigation
    assert view_model.channel_view_model._page_navigation == mock_page_navigation
    assert view_model.unspent_view_model._page_navigation == mock_page_navigation
    assert view_model.issue_cfa_asset_view_model._page_navigation == mock_page_navigation
    assert view_model.ln_endpoint_view_model._page_navigation == mock_page_navigation
    assert view_model.cfa_view_model._page_navigation == mock_page_navigation
    assert view_model.enter_wallet_password_view_model._page_navigation == mock_page_navigation
    assert view_model.receive_cfa_view_model._page_navigation == mock_page_navigation
    assert view_model.backup_view_model._page_navigation == mock_page_navigation
    assert view_model.setting_view_model._page_navigation == mock_page_navigation
    assert view_model.ln_offchain_view_model._page_navigation == mock_page_navigation
    assert view_model.splash_view_model._page_navigation == mock_page_navigation
    assert view_model.restore_view_model._page_navigation == mock_page_navigation
    assert view_model.wallet_transfer_selection_view_model._page_navigation == mock_page_navigation
    assert view_model.faucets_view_model._page_navigation == mock_page_navigation
