import pytest

from mediaichemy.media.multi import (VideoFromImage,
                                     VideoFromImageParameters)
from tests._mocks.files import expected_outputs
from tests import assertions


@pytest.mark.asyncio
async def test_video_from_image_creation(mock_downloader, mock_runware_client):
    video_from_img_params = VideoFromImageParameters(
        video_prompt='',
        duration=12
    )
    video_from_img = VideoFromImage(params=video_from_img_params)
    video_file, cost = await video_from_img.create()

    assertions.all_durations_equal([video_file,
                                    expected_outputs.video_from_image])
