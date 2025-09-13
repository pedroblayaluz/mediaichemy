import pytest

from mediaichemy.media.multi import (NarrationWithBackground,
                                     NarrationWithBackgroundParameters)
from tests._mocks.files import expected_outputs
from tests import assertions


@pytest.mark.asyncio
async def test_narration_with_background_creation(mock_narration_synthesis):
    narration_w_bg_params = NarrationWithBackgroundParameters(
        narration_text='Once upon a time in a land far, far away...',
        narration_voice_name='en_US-amy-medium',
        background_youtube_urls=[
            "https://www.youtube.com/watch?v=aVM6Fbh4hc4"
        ]
    )
    narration_w_bg = NarrationWithBackground(params=narration_w_bg_params)
    narration_w_bg_file, cost = await narration_w_bg.create()

    assertions.all_durations_equal([narration_w_bg_file,
                                    expected_outputs.narration_with_background])
