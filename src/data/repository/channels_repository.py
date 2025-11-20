"""Module containing ChannelRepository."""
from __future__ import annotations

from src.model.channels_model import ChannelsListResponseModel
from src.model.channels_model import CloseChannelRequestModel
from src.model.channels_model import CloseChannelResponseModel
from src.model.channels_model import OpenChannelResponseModel
from src.model.channels_model import OpenChannelsRequestModel
from src.utils.custom_context import repository_custom_context
from src.utils.decorators.unlock_required import unlock_required
from src.utils.endpoints import CLOSE_CHANNEL_ENDPOINT
from src.utils.endpoints import LIST_CHANNELS_ENDPOINT
from src.utils.endpoints import OPEN_CHANNEL_ENDPOINT
from src.utils.helpers import process_response
from src.utils.request import Request


class ChannelRepository:
    """Repository for handling channel operations."""

    @staticmethod
    @unlock_required
    def close_channel(channel: CloseChannelRequestModel) -> CloseChannelResponseModel:
        """Close a channel."""
        payload = channel.dict()
        with repository_custom_context():
            response = Request.post(CLOSE_CHANNEL_ENDPOINT, payload)
            process_response(
                response, invalidate_cache=True,
                expect_json=False,
            )
            return CloseChannelResponseModel(status=True)

    @staticmethod
    @unlock_required
    def open_channel(channel: OpenChannelsRequestModel) -> OpenChannelResponseModel:
        """Open a channel."""
        payload = channel.dict()
        with repository_custom_context():
            response = Request.post(OPEN_CHANNEL_ENDPOINT, payload)
            data = process_response(response, invalidate_cache=True)
            return OpenChannelResponseModel(**data)

    @staticmethod
    @unlock_required
    def list_channel() -> ChannelsListResponseModel:
        """List channels."""
        with repository_custom_context():
            response = Request.get(LIST_CHANNELS_ENDPOINT)
            data = process_response(response)
            return ChannelsListResponseModel(**data)
