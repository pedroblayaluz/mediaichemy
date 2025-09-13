import pytest

from mediaichemy.media.multi import (SubtitledNarratedVideo,
                                     SubtitledNarratedVideoParameters)
from tests._mocks.files import expected_outputs
from tests import assertions


@pytest.mark.asyncio
async def test_subtitled_narrated_video_creation(mock_downloader, mock_runware_client, mock_agent):
    subtitled_video_params = SubtitledNarratedVideoParameters(
        narration_text='Once upon a time in a land far, far away...',
        narration_voice_name='en_US-amy-medium',
        background_youtube_urls=[
            "https://www.youtube.com/watch?v=aVM6Fbh4hc4"
        ],
        video_prompt=''
    )

    subtitled_video = SubtitledNarratedVideo(params=subtitled_video_params)
    subtitled_videos, cost = await subtitled_video.create()

    assertions.all_durations_equal(subtitled_videos
                                   + expected_outputs.subtitled_videos)
