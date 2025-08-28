import pytest

from mediaichemy.media.single.video import (Video,
                                            VideoParameters)
from tests._mocks.files import expected_outputs


@pytest.mark.asyncio
async def test_video_creation(mock_downloader, mock_runware_client):
    video_params = VideoParameters(
        video_prompt=''
    )
    video = Video(params=video_params)
    video_file, cost = await video.create()
    assert video_file.hash == expected_outputs.video.hash
