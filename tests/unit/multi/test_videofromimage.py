# tests/test_media.py
import pytest
from mediaichemy.media.multi.video_from_image import VideoFromImage, VideoFromImageParameters
from tests._mocks.files import expected_outputs


@pytest.mark.asyncio
async def test_video_from_image_creation(mock_downloader, mock_runware_client):
    video_from_img_params = VideoFromImageParameters(
        video_prompt='',
        duration=12
    )
    video_from_img = VideoFromImage(params=video_from_img_params)
    video_file, cost = await video_from_img.create()
    assert video_file.hash == expected_outputs.video_from_image.hash
