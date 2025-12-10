"""Unit tests for faucet service helper"""
from __future__ import annotations

from enum import Enum

import pytest

from src.data.service.helpers.faucet_service_helper import get_faucet_url
from src.model.enums.enums_model import NetworkEnumModel
from src.utils.constant import rgbMainnetFaucetURLs
from src.utils.constant import rgbRegtestFaucetURLs
from src.utils.constant import rgbTestnet4FaucetURLs
from src.utils.constant import rgbTestnetFaucetURLs
from src.utils.custom_exception import ServiceOperationException
from src.utils.error_message import ERROR_FAILED_TO_GET_FAUCET_URL
from src.utils.error_message import ERROR_INVALID_NETWORK_TYPE

# Test cases for get_faucet_url helper of service


def test_get_faucet_url():
    """Case 1 : Test all network"""
    response_net_regtest = get_faucet_url(NetworkEnumModel.REGTEST)
    response_net_testnet = get_faucet_url(NetworkEnumModel.TESTNET)
    response_net_testnet4 = get_faucet_url(NetworkEnumModel.TESTNET4)
    response_net_mainnet = get_faucet_url(NetworkEnumModel.MAINNET)
    assert response_net_mainnet == rgbMainnetFaucetURLs[0]
    assert response_net_testnet == rgbTestnetFaucetURLs[0]
    assert response_net_testnet4 == rgbTestnet4FaucetURLs[0]
    assert response_net_regtest == rgbRegtestFaucetURLs[0]


def test_get_faucet_url_when_invalid_argument():
    """Case 2 : Test when invalid argument to get_faucet_url helper"""
    with pytest.raises(ServiceOperationException, match=ERROR_FAILED_TO_GET_FAUCET_URL):
        get_faucet_url('random')


def test_get_faucet_url_when_invalid_network():
    """Case 3 : Test when invalid network to get_faucet_url helper"""
    class MockedNetworkEnumModel(str, Enum):
        """Mocked enum to test code"""
        RANDOM = 'random'
    with pytest.raises(ServiceOperationException, match=ERROR_INVALID_NETWORK_TYPE):
        get_faucet_url(MockedNetworkEnumModel.RANDOM)
