# pylint: disable=line-too-long, too-few-public-methods
"""This module contains the HelpCardContentModel class,
which represents the all models for help card content model.
"""
from __future__ import annotations

from pydantic import BaseModel
from pydantic import HttpUrl

from src.data.repository.setting_repository import SettingRepository
from src.model.enums.enums_model import NetworkEnumModel


class HelpCardModel(BaseModel):
    """Model for a single help card."""
    title: str
    detail: str
    links: list[HttpUrl] | None = None


class HelpCardContentModel(BaseModel):
    """Content for the help cards."""
    card_content: list[HelpCardModel]

    @classmethod
    def create_default(cls):
        """Factory method to create a default instance of HelpCardContentModel"""
        card_content = [
            HelpCardModel(
                title='where_can_i_learn_more_about_rgb',
                detail='learn_about_rgb',
            ),
            HelpCardModel(
                title='why_do_i_see_outgoing_bitcoin_transactions_that_i_did_not_authorize',
                detail='outgoing_transaction_without_authorize_detail',
            ),
            HelpCardModel(
                title='what_is_the_minimum_bitcoin_balance_needed_to_issue_and_receive_rgb_assets',
                detail='minimum_bitcoin_balance_needed_to_issue_and_receive_rgb_asset',
            ),
            HelpCardModel(
                title='where_can_i_send_feedback_or_ask_for_support',
                detail='support_and_feedback',
                links=[
                    'https://t.me/IrisWallet',
                ],
            ),
        ]
        network = SettingRepository.get_wallet_network()
        if network == NetworkEnumModel.REGTEST:
            card_content.append(
                HelpCardModel(
                    title='where_can_i_get_regtest_bitcoins',
                    detail='get_regtest_bitcoin',
                    links=['https://t.me/rgb_lightning_bot'],
                ),
            )
        else:  # Default to Testnet
            card_content.append(
                HelpCardModel(
                    title='where_can_i_get_testnet_bitcoins',
                    detail='get_testnet_bitcoin',
                    links=[
                        'https://testnet-faucet.mempool.co/',
                        'https://bitcoinfaucet.uo1.net/',
                        'https://coinfaucet.eu/en/btc-testnet/',
                        'https://testnet-faucet.com/btc-testnet/',
                    ],
                ),
            )
        return cls(card_content=card_content)
