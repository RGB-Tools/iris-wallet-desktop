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
                title='Where can I learn more about RGB?',
                detail='Visit <a href="https://rgb.info" style="color: #03CA9B; text-decoration: none;">rgb.info</a> for resources and documentation.',
            ),
            HelpCardModel(
                title="Why do I see outgoing Bitcoin transactions that I didn't authorize?",
                detail='In the RGB protocol assets need to be assigned to a Bitcoin output, if you do not have available UTXOs to receive, issue, or send yourself change assets, the wallet will use the available bitcoin balance to generate new UTXOs. Such transactions are marked in the transaction list as "internal"',
            ),
            HelpCardModel(
                title='What is the minimum bitcoin balance needed to issue and receive RGB assets?',
                detail='To create a set of UTXOs needed to issue and receive assets the initial bitcoin balance needs to be at least 10,000 satoshis',
            ),
            HelpCardModel(
                title='Where can I send feedback or ask for support?',
                detail='For support and feedback there is a dedicated Telegram group:',
                links=[
                    'https://t.me/IrisWallet',
                ],
            ),
        ]
        network = SettingRepository.get_wallet_network()
        if network == NetworkEnumModel.REGTEST:
            card_content.append(
                HelpCardModel(
                    title='Where can I get REGTEST Bitcoins?',
                    detail='You can receive Regtest Bitcoin by using our Telegram bot. Click the link below to request funds:',
                    links=['https://t.me/rgb_lightning_bot'],
                ),
            )
        else:  # Default to Testnet
            card_content.append(
                HelpCardModel(
                    title='Where can I get TESTNET Bitcoins?',
                    detail='You can get Testnet Bitcoin by using one of the many available faucets. Below are a few linked examples, but you can always find more using a search engine:',
                    links=[
                        'https://testnet-faucet.mempool.co/',
                        'https://bitcoinfaucet.uo1.net/',
                        'https://coinfaucet.eu/en/btc-testnet/',
                        'https://testnet-faucet.com/btc-testnet/',
                    ],
                ),
            )
        return cls(card_content=card_content)
