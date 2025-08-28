import pytest
from mediaichemy.media.single.speech import Speech, SpeechParameters
from tests._mocks.files import expected_outputs


@pytest.mark.asyncio
async def test_speech_creation():
    speech_params = SpeechParameters(
        narration_text='Once upon a time in a land far, far away...',
        voice_name='en_US-amy-medium'
    )
    speech = Speech(params=speech_params)

    speech_file, cost = await speech.create()

    assert speech_file.hash == expected_outputs.speech.hash
