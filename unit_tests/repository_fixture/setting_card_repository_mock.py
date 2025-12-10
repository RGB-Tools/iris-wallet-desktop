"""This module contains the test fixtures for the setting card repository."""
from __future__ import annotations

import pytest


@pytest.fixture
def mock_set_default_fee_rate(mocker):
    """Mocked set_default_fee_rate function"""
    def _mock_set_default_fee_rate(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.set_default_fee_rate',
            return_value=value,
        )
    return _mock_set_default_fee_rate


@pytest.fixture
def mock_get_default_fee_rate(mocker):
    """Mocked get_default_fee_rate function"""
    def _mock_get_default_fee_rate(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_fee_rate',
            return_value=value,
        )
    return _mock_get_default_fee_rate


@pytest.fixture
def mock_set_default_expiry_time(mocker):
    """Mocked set_default_expiry_time function"""
    def _mock_set_default_expiry_time(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.set_default_expiry_time',
            return_value=value,
        )
    return _mock_set_default_expiry_time


@pytest.fixture
def mock_get_default_expiry_time(mocker):
    """Mocked get_default_expiry_time function"""
    def _mock_get_default_expiry_time(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_expiry_time',
            return_value=value,
        )
    return _mock_get_default_expiry_time


@pytest.fixture
def mock_set_default_min_confirmation(mocker):
    """Mocked set_default_min_confirmation function"""
    def _mock_set_default_min_confirmation(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.set_default_min_confirmation',
            return_value=value,
        )
    return _mock_set_default_min_confirmation


@pytest.fixture
def mock_get_default_min_confirmation(mocker):
    """Mocked get_default_min_confirmation function"""
    def _mock_get_default_min_confirmation(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_min_confirmation',
            return_value=value,
        )
    return _mock_get_default_min_confirmation


@pytest.fixture
def mock_set_default_endpoints(mocker):
    """Mocked set_default_endpoints function"""
    def _mock_set_default_endpoints(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.set_default_endpoints',
            return_value=value,
        )
    return _mock_set_default_endpoints


@pytest.fixture
def mock_get_default_endpoints(mocker):
    """Mocked get_default_endpoints function"""
    def _mock_get_default_endpoints(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_endpoints',
            return_value=value,
        )
    return _mock_get_default_endpoints


@pytest.fixture
def mock_check_indexer_url(mocker):
    """Mocked check_indexer_url function"""
    def _mock_check_indexer_url(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.check_indexer_url',
            return_value=value,
        )
    return _mock_check_indexer_url


@pytest.fixture
def mock_check_proxy_endpoint(mocker):
    """Mocked check_proxy_endpoint function"""
    def _mock_check_proxy_endpoint(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.check_proxy_endpoint',
            return_value=value,
        )
    return _mock_check_proxy_endpoint


@pytest.fixture
def mock_get_default_proxy_endpoint(mocker):
    """Mocked get_default_proxy_endpoint function"""
    def _mock_get_default_proxy_endpoint(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_proxy_endpoint',
            return_value=value,
        )
    return _mock_get_default_proxy_endpoint


@pytest.fixture
def mock_get_default_bitcoind_host(mocker):
    """Mocked get_default_bitcoind_host function"""
    def _mock_get_default_bitcoind_host(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_bitcoind_host',
            return_value=value,
        )
    return _mock_get_default_bitcoind_host


@pytest.fixture
def mock_get_default_bitcoind_port(mocker):
    """Mocked get_default_bitcoind_port function"""
    def _mock_get_default_bitcoind_port(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_bitcoind_port',
            return_value=value,
        )
    return _mock_get_default_bitcoind_port


@pytest.fixture
def mock_get_default_announce_address(mocker):
    """Mocked get_default_announce_address function"""
    def _mock_get_default_announce_address(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_announce_address',
            return_value=value,
        )
    return _mock_get_default_announce_address


@pytest.fixture
def mock_get_default_announce_alias(mocker):
    """Mocked get_default_announce_alias function"""
    def _mock_get_default_announce_alias(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_announce_alias',
            return_value=value,
        )
    return _mock_get_default_announce_alias


@pytest.fixture
def mock_get_default_indexer_url(mocker):
    """Mocked get_default_indexer_url function"""
    def _mock_get_default_indexer_url(value):
        return mocker.patch(
            'src.repository.setting_card_repository.SettingCardRepository.get_default_indexer_url',
            return_value=value,
        )
    return _mock_get_default_indexer_url
