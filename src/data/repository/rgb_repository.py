"""Module containing RgbRepository."""
from __future__ import annotations

from src.model.rgb_model import AssetBalanceResponseModel
from src.model.rgb_model import AssetIdModel
from src.model.rgb_model import CreateUtxosRequestModel
from src.model.rgb_model import CreateUtxosResponseModel
from src.model.rgb_model import DecodeRgbInvoiceRequestModel
from src.model.rgb_model import DecodeRgbInvoiceResponseModel
from src.model.rgb_model import FailTransferRequestModel
from src.model.rgb_model import FailTransferResponseModel
from src.model.rgb_model import FilterAssetRequestModel
from src.model.rgb_model import GetAssetMediaModelRequestModel
from src.model.rgb_model import GetAssetMediaModelResponseModel
from src.model.rgb_model import GetAssetResponseModel
from src.model.rgb_model import IssueAssetCfaRequestModelWithDigest
from src.model.rgb_model import IssueAssetNiaRequestModel
from src.model.rgb_model import IssueAssetResponseModel
from src.model.rgb_model import IssueAssetUdaRequestModel
from src.model.rgb_model import ListTransferAssetResponseModel
from src.model.rgb_model import ListTransfersRequestModel
from src.model.rgb_model import PostAssetMediaModelResponseModel
from src.model.rgb_model import RefreshRequestModel
from src.model.rgb_model import RefreshTransferResponseModel
from src.model.rgb_model import RgbInvoiceDataResponseModel
from src.model.rgb_model import RgbInvoiceRequestModel
from src.model.rgb_model import SendAssetRequestModel
from src.model.rgb_model import SendAssetResponseModel
from src.utils.custom_context import repository_custom_context
from src.utils.decorators.check_colorable_available import check_colorable_available
from src.utils.decorators.unlock_required import unlock_required
from src.utils.endpoints import ASSET_BALANCE_ENDPOINT
from src.utils.endpoints import CREATE_UTXO_ENDPOINT
from src.utils.endpoints import DECODE_RGB_INVOICE_ENDPOINT
from src.utils.endpoints import FAIL_TRANSFER_ENDPOINT
from src.utils.endpoints import GET_ASSET_MEDIA
from src.utils.endpoints import ISSUE_ASSET_ENDPOINT_CFA
from src.utils.endpoints import ISSUE_ASSET_ENDPOINT_NIA
from src.utils.endpoints import ISSUE_ASSET_ENDPOINT_UDA
from src.utils.endpoints import LIST_ASSETS_ENDPOINT
from src.utils.endpoints import LIST_TRANSFERS_ENDPOINT
from src.utils.endpoints import POST_ASSET_MEDIA
from src.utils.endpoints import REFRESH_TRANSFERS_ENDPOINT
from src.utils.endpoints import RGB_INVOICE_ENDPOINT
from src.utils.endpoints import SEND_ASSET_ENDPOINT
from src.utils.helpers import process_response
from src.utils.request import Request


class RgbRepository:
    """Repository for handling RGB-related operations."""

    @staticmethod
    @unlock_required
    def create_utxo(create_utxos: CreateUtxosRequestModel):
        """Create UTXOs."""
        payload = create_utxos.dict()
        with repository_custom_context():
            response = Request.post(CREATE_UTXO_ENDPOINT, payload)
            process_response(
                response, invalidate_cache=True,
                expect_json=False,
            )
            return CreateUtxosResponseModel(status=True)

    @staticmethod
    @unlock_required
    def get_asset_balance(
        asset_balance: AssetIdModel,
    ) -> AssetBalanceResponseModel:
        """Get asset balance."""
        payload = asset_balance.dict()
        with repository_custom_context():
            response = Request.post(ASSET_BALANCE_ENDPOINT, payload)
            data = process_response(response)
            return AssetBalanceResponseModel(**data)

    @staticmethod
    @unlock_required
    def decode_invoice(invoice: DecodeRgbInvoiceRequestModel):
        """Decode RGB invoice."""
        payload = invoice.dict()
        with repository_custom_context():
            response = Request.post(DECODE_RGB_INVOICE_ENDPOINT, payload)
            data = process_response(response)
            return DecodeRgbInvoiceResponseModel(**data)

    @staticmethod
    @unlock_required
    def list_transfers(asset_id: ListTransfersRequestModel):
        """List transfers."""
        payload = asset_id.dict()
        with repository_custom_context():
            response = Request.post(LIST_TRANSFERS_ENDPOINT, payload)
            data = process_response(response)
            return ListTransferAssetResponseModel(**data)

    @staticmethod
    @unlock_required
    def refresh_transfer():
        """Refresh transfers."""
        with repository_custom_context():
            payload = RefreshRequestModel().dict()
            response = Request.post(REFRESH_TRANSFERS_ENDPOINT, payload)
            process_response(
                response, invalidate_cache=False,
                expect_json=False,
            )
            return RefreshTransferResponseModel(status=True)

    @staticmethod
    @unlock_required
    @check_colorable_available()
    def rgb_invoice(invoice: RgbInvoiceRequestModel):
        """Get RGB invoice."""
        payload = invoice.dict()
        with repository_custom_context():
            response = Request.post(RGB_INVOICE_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return RgbInvoiceDataResponseModel(**data)

    @staticmethod
    @unlock_required
    @check_colorable_available()
    def send_asset(asset_detail: SendAssetRequestModel):
        """Send asset."""
        payload = asset_detail.dict()
        with repository_custom_context():
            response = Request.post(SEND_ASSET_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return SendAssetResponseModel(**data)

    @staticmethod
    @unlock_required
    def get_assets(filter_asset_request_model: FilterAssetRequestModel) -> GetAssetResponseModel:
        """Get assets."""
        payload = filter_asset_request_model.dict()
        with repository_custom_context():
            response = Request.post(LIST_ASSETS_ENDPOINT, body=payload)
            data = process_response(response, invalidate_cache=True)
            return GetAssetResponseModel(**data)

    @staticmethod
    @unlock_required
    @check_colorable_available()
    def issue_asset_nia(asset: IssueAssetNiaRequestModel) -> IssueAssetResponseModel:
        """Issue asset."""
        payload = asset.dict()
        with repository_custom_context():
            response = Request.post(ISSUE_ASSET_ENDPOINT_NIA, payload)
            data = process_response(response, invalidate_cache=True)
            asset_data = data['asset']
            return IssueAssetResponseModel(**asset_data)

    @staticmethod
    @unlock_required
    @check_colorable_available()
    def issue_asset_cfa(asset: IssueAssetCfaRequestModelWithDigest) -> IssueAssetResponseModel:
        """Issue asset."""
        payload = asset.dict()
        with repository_custom_context():
            response = Request.post(ISSUE_ASSET_ENDPOINT_CFA, payload)
            data = process_response(response, invalidate_cache=True)
            asset_data = data['asset']
            return IssueAssetResponseModel(**asset_data)

    @staticmethod
    @unlock_required
    @check_colorable_available()
    def issue_asset_uda(asset: IssueAssetUdaRequestModel) -> IssueAssetResponseModel:
        """Issue asset."""
        payload = asset.dict()
        with repository_custom_context():
            response = Request.post(ISSUE_ASSET_ENDPOINT_UDA, payload)
            data = process_response(response, invalidate_cache=True)
            asset_data = data['asset']
            return IssueAssetResponseModel(**asset_data)

    @staticmethod
    @unlock_required
    def get_asset_media_hex(digest: GetAssetMediaModelRequestModel) -> GetAssetMediaModelResponseModel:
        """Get asset media hex from digest"""
        payload = digest.dict()
        with repository_custom_context():
            response = Request.post(GET_ASSET_MEDIA, payload)
            data = process_response(response)
            return GetAssetMediaModelResponseModel(**data)

    @staticmethod
    @unlock_required
    def post_asset_media(files) -> PostAssetMediaModelResponseModel:
        """return digest for given image"""
        with repository_custom_context():
            response = Request.post(POST_ASSET_MEDIA, files=files)
            data = process_response(response)
            return PostAssetMediaModelResponseModel(**data)

    @staticmethod
    @unlock_required
    def fail_transfer(transfer: FailTransferRequestModel) -> FailTransferResponseModel:
        """Mark the specified transfer as failed."""
        payload = transfer.dict()
        with repository_custom_context():
            response = Request.post(FAIL_TRANSFER_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return FailTransferResponseModel(**data)
