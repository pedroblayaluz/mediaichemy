# tests/test_media.py
import pytest
from mediaichemy.media.single.image import Image, ImageParameters
from tests._mocks.files import expected_outputs


@pytest.mark.asyncio
async def test_image_creation(mock_downloader, mock_runware_client):
    image_params = ImageParameters(
        image_prompt=''
    )
    image = Image(params=image_params)

    image_file, cost = await image.create()

    assert image_file.hash == expected_outputs.image.hash
