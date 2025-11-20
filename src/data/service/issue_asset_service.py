# pylint:disable=too-few-public-methods
# This class is intentionally designed as a data container (DTO / model).
# It stores structured data only and does not require additional public methods.
"""Service class for issue asset in case of more then two api call"""
from __future__ import annotations

import mimetypes
import os

from src.data.repository.rgb_repository import RgbRepository
from src.model.rgb_model import IssueAssetCfaRequestModel
from src.model.rgb_model import IssueAssetCfaRequestModelWithDigest
from src.model.rgb_model import IssueAssetResponseModel
from src.model.rgb_model import PostAssetMediaModelResponseModel
from src.utils.custom_exception import CommonException
from src.utils.error_message import ERROR_IMAGE_PATH_NOT_EXITS
from src.utils.handle_exception import handle_exceptions


class IssueAssetService:
    """
    Service class for issue asset
    """
    @staticmethod
    def issue_asset_cfa(new_asset_detail: IssueAssetCfaRequestModel) -> IssueAssetResponseModel | None:
        """This function issue cfa asset"""
        try:
            if not os.path.exists(new_asset_detail.file_path):
                raise CommonException(ERROR_IMAGE_PATH_NOT_EXITS)
            # Guess the MIME type of the file
            mime_type, _ = mimetypes.guess_type(new_asset_detail.file_path)

            # Read the file into memory
            with open(new_asset_detail.file_path, 'rb') as file:
                file_data = file.read()  # Read the file data into memory

            # Prepare the files parameter
            files = {
                'file': (
                    new_asset_detail.file_path,
                    file_data, mime_type,
                ),
            }
            # Send the POST request
            response: PostAssetMediaModelResponseModel = RgbRepository.post_asset_media(
                files=files,
            )

            issued_asset: IssueAssetResponseModel = RgbRepository.issue_asset_cfa(
                IssueAssetCfaRequestModelWithDigest(
                    amounts=new_asset_detail.amounts,
                    ticker=new_asset_detail.ticker,
                    name=new_asset_detail.name,
                    file_digest=response.digest,
                ),
            )
            return issued_asset
        except Exception as exc:
            return handle_exceptions(exc)
