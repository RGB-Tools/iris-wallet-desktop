"""
End-to-End tests for wallet functionality
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from e2e_tests.test.features.main_features import MainFeatures
from e2e_tests.test.pageobjects.main_page_objects import MainPageObjects
from e2e_tests.test.utilities.base_operation import BaseOperations


@dataclass
class WalletTestSetup:
    """
    Data class for setting up wallet test environment.
    """
    first_page_features: MainFeatures
    second_page_features: MainFeatures
    first_page_objects: MainPageObjects
    second_page_objects: MainPageObjects
    first_page_operations: BaseOperations
    second_page_operations: BaseOperations
    wallet_mode: str  # Wallet mode is now stored


class TransferType(str, Enum):
    """
    Enum model for transfer type.
    """
    BITCOIN = 'bitcoin'
    LIGHTNING = 'lightning'
