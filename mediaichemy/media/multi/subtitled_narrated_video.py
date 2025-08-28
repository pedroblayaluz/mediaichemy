

from mediaichemy.media.media import MultiMedia
from ..parameters import NarratedVideoWithBackgroundParameters
from ..parameters import SpeechWithBackgroundParameters
from ..parameters import SubtitledNarratedVideoParameters


class SpeechWithBackground(MultiMedia):
    def __init__(self,
                 params: SpeechWithBackgroundParameters = SpeechWithBackgroundParameters()):
        super().__init__(params=params)

    async def create(self):
        speech = self.create_speech_with_background()
        return self.unpack(speech), None

    def create_speech_with_background(self):
        speech = self.studio.create_speech(self.output_dir)
        background = self.studio.download_youtube_mp3(self.output_dir)
        speech = self.studio.mix_audio_with_random_background_section(speech, background)
        return speech


class NarratedVideoWithBackground(SpeechWithBackground):
    def __init__(self,
                 params: NarratedVideoWithBackgroundParameters = NarratedVideoWithBackgroundParameters()):
        super().__init__(params=params)

    async def create(self):
        narrated_video, cost = await self.create_narrated_video()
        return self.unpack(narrated_video), cost

    async def create_narrated_video(self):
        speech_w_bg = self.create_speech_with_background()
        video, cost = await self.studio.create_video_from_image(directory=self.output_dir)
        self.studio.loop_to_duration(video=video,
                                     target_duration=speech_w_bg.get_duration())
        self.studio.add_audio_track_to_video(video=video, audio=speech_w_bg)
        speech_w_bg.delete()
        return video, cost


class SubtitledNarratedVideo(NarratedVideoWithBackground):
    def __init__(self,
                 params: SubtitledNarratedVideoParameters = SubtitledNarratedVideoParameters()):
        super().__init__(params=params)

    async def create(self):
        subtitled_videos, cost = await self.create_subtitled_video()
        return subtitled_videos, cost

    async def create_subtitled_video(self):
        narrated_video, cost = await self.create_narrated_video()
        subtitled_videos = self.studio.make_subtitled_videos(narrated_video)
        narrated_video.delete()
        return subtitled_videos, cost
