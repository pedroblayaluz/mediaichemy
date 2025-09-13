import pytest

from mediaichemy.media.single.narration import (Narration,
                                                NarrationParameters)
from tests._mocks.files import expected_outputs


@pytest.mark.asyncio
async def test_narration_creation():
    narration_params = NarrationParameters(
        narration_text='Once upon a time in a land far, far away...',
        narration_voice_name='en_US-amy-medium'
    )
    narration = Narration(params=narration_params)

    narration_file, cost = await narration.create()

    assert narration_file.hash == expected_outputs.narration.hash
