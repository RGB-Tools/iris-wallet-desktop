"""Unit test for view unspent list view model"""
# Disable the redefined-outer-name warning as
# it's normal to pass mocked object in tests function
# pylint: disable=redefined-outer-name,unused-argument
from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.model.btc_model import UnspentsListResponseModel
from src.viewmodels.view_unspent_view_model import UnspentListViewModel


@pytest.fixture
def mock_page_navigation():
    """Fixture for creating a mock page navigation object."""
    return MagicMock()


@pytest.fixture
def unspent_list_view_model(mock_page_navigation):
    """Fixture for creating an instance of UnspentListViewModel with a mock page navigation object."""
    return UnspentListViewModel(mock_page_navigation)


@pytest.fixture
def mock_list_unspents_response():
    """Fixture for creating a mock list_unspents api."""
    mocked_unspent_list_response = {
        'unspents': [
            {
                'utxo': {
                    'outpoint': 'efed66f5309396ff43c8a09941c8103d9d5bbffd473ad9f13013ac89fb6b4671:0',
                    'btc_amount': 1000,
                    'colorable': True,
                },
                'rgb_allocations': [
                    {
                        'asset_id': 'rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
                        'assignment': {
                            'type': 'Fungible',
                            'value': 42,
                        },
                        'settled': False,
                    },
                ],
            },
        ],
    }
    mock_response_model = UnspentsListResponseModel(
        **mocked_unspent_list_response,
    )
    return mock_response_model


@patch('src.data.repository.btc_repository.BtcRepository.list_unspents')
@patch('src.utils.cache.Cache.get_cache_session')
def test_get_unspent_list_success(mock_cache, mock_list_unspents, unspent_list_view_model, mock_list_unspents_response):
    """Test get_unspent_list method when the API call succeeds."""
    # Create a mock function to connect to the signal
    list_loaded_mock = Mock()
    mock_loading_started = Mock()
    unspent_list_view_model.loading_started.connect(mock_loading_started)
    mock_loading_finished = Mock()
    unspent_list_view_model.loading_finished.connect(mock_loading_finished)
    unspent_list_view_model.list_loaded.connect(list_loaded_mock)

    mock_cache_session = Mock()
    mock_cache.return_value = mock_cache_session

    mock_list_unspents.return_value = mock_list_unspents_response
    unspent_list_view_model.get_unspent_list(is_hard_refresh=True)

    mock_cache.assert_called_once()
    mock_cache_session.invalidate_cache.assert_called_once()

    # Ensure that the cache fetch returns a valid tuple
    mock_cache_session.fetch_cache.return_value = (
        mock_list_unspents_response, True,
    )

    # Ensure that the worker's result is emitted correctly
    unspent_list_view_model.worker.result.emit(
        mock_cache_session.fetch_cache.return_value[0], True,
    )

    # Check if the unspent list is updated correctly
    assert unspent_list_view_model.unspent_list == mock_list_unspents_response.unspents
    list_loaded_mock.assert_called_once_with(True)
    mock_loading_finished.assert_called_once_with(False)
    mock_loading_started.assert_called_once_with(True)
