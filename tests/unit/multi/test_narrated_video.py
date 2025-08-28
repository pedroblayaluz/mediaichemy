import pytest

from mediaichemy.media.multi import (NarratedVideo,
                                     NarratedVideoParameters)
from tests._mocks.files import expected_outputs
from tests import assertions


@pytest.mark.asyncio
async def test_narrated_video_creation(mock_downloader, mock_runware_client, mock_agent):
    narrated_video_params = NarratedVideoParameters(
        narration_text='Once upon a time in a land far, far away...',
        voice_name='en_US-amy-medium',
        youtube_urls=[
            "https://www.youtube.com/watch?v=NTj5EEM_SOY"
        ],
        video_prompt=''
    )

    narrated_video = NarratedVideo(params=narrated_video_params)
    narrated_video_file, cost = await narrated_video.create()

    assertions.all_durations_equal([narrated_video_file,
                                    expected_outputs.narrated_video])
