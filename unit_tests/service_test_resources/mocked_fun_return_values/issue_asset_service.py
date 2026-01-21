"""Mocked data for the issue asset service test"""
from __future__ import annotations

import os

from src.model.rgb_model import IssueAssetCfaRequestModel
from src.model.rgb_model import IssueAssetResponseModel
from src.model.rgb_model import PostAssetMediaModelResponseModel
asset_image_path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'iris_logo.png',
    ),
)
asset_image_path_not_exits_image = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'not_exits_path.png',
    ),
)
mock_data_new_asset_issue: IssueAssetCfaRequestModel = IssueAssetCfaRequestModel(
    amounts=[1000],
    ticker='TTK',
    precision=0,
    name='The test token',
    file_path=asset_image_path,
)

mock_data_new_asset_issue_no_path_exits: IssueAssetCfaRequestModel = IssueAssetCfaRequestModel(
    amounts=[1000],
    ticker='TTK',
    precision=0,
    name='The test token',
    file_path=asset_image_path_not_exits_image,
)

mock_data_post_asset_api_res: PostAssetMediaModelResponseModel = PostAssetMediaModelResponseModel(
    digest='5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
)

example_data_of_issue_asset_api = {
    'asset_id': 'rgb:2dkSTbr-jFhznbPmo-TQafzswCN-av4gTsJjX-ttx6CNou5-M98k8Zd',
    'name': 'Collectible',
    'details': 'asset details',
    'precision': 0,
    'issued_supply': 777,
    'timestamp': 1691160565,
    'added_at': 1691161979,
    'balance': {
        'settled': 777000,
        'future': 777000,
        'spendable': 777000,
        'offchain_outbound': 444,
        'offchain_inbound': 0,
    },
    'media': {
        'file_path': '/path/to/media',
        'digest': '5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
        'mime': 'text/plain',
    },
}


mock_data_issue_cfa_asset_res: IssueAssetResponseModel = IssueAssetResponseModel(
    **example_data_of_issue_asset_api,
)
