# tests/test_media.py
import pytest
from mediaichemy.media.multi import subtitled_narrated_video as snv


@pytest.mark.asyncio
async def test_speech_with_background_creation(mock_speech_synthesis):
    speech_w_bg_params = snv.SpeechWithBackgroundParameters(
        narration_text='Once upon a time in a land far, far away...',
        voice_name='en_US-amy-medium',
        youtube_urls=[
            "https://www.youtube.com/watch?v=NTj5EEM_SOY"
        ]
    )
    speech_w_bg = snv.SpeechWithBackground(params=speech_w_bg_params)
    speech_w_bg_file, cost = await speech_w_bg.create()

    assert speech_w_bg_file.exists()


@pytest.mark.asyncio
async def test_narrated_video_creation(mock_downloader, mock_runware_client, mock_agent):
    narrated_video_params = snv.NarratedVideoWithBackgroundParameters(
        narration_text='Once upon a time in a land far, far away...',
        voice_name='en_US-amy-medium',
        youtube_urls=[
            "https://www.youtube.com/watch?v=NTj5EEM_SOY"
        ],
        video_prompt=''
    )

    narrated_video = snv.NarratedVideoWithBackground(params=narrated_video_params)
    narrated_video_file, cost = await narrated_video.create()

    assert narrated_video_file.exists()


@pytest.mark.asyncio
async def test_subtitled_video_creation(mock_downloader, mock_runware_client, mock_agent):
    subtitled_video_params = snv.SubtitledNarratedVideoParameters(
        narration_text='Once upon a time in a land far, far away...',
        voice_name='en_US-amy-medium',
        youtube_urls=[
            "https://www.youtube.com/watch?v=NTj5EEM_SOY"
        ],
        video_prompt=''
    )

    subtitled_video = snv.SubtitledNarratedVideo(params=subtitled_video_params)
    subtitled_videos, cost = await subtitled_video.create()

    for i in range(len(subtitled_videos)):
        assert subtitled_videos[i].exists()
