
from mediaichemy.media.parameters import StorylineVideoParameters
from mediaichemy.media.parameters import NarratedVideoParameters
from mediaichemy.media.parameters import NarrationWithBackgroundParameters
from mediaichemy.media.multi.multi import MultiMedia


class NarrationWithBackground(MultiMedia):
    params_class = NarrationWithBackgroundParameters

    def __init__(self,
                 params: NarrationWithBackgroundParameters):
        super().__init__(params=params)

    async def create(self):
        narration = self.create_narration_with_background()
        return self.unpack(narration), None

    def create_narration_with_background(self):
        narration = self.studio.create_narration(self.output_dir)
        narration_with_background = self.studio.download_and_mix_youtube_audio(
            directory=self.output_dir,
            original_audio=narration
        )
        return narration_with_background


class NarratedVideo(NarrationWithBackground):
    params_class = NarratedVideoParameters

    def __init__(self,
                 params: NarratedVideoParameters):
        super().__init__(params=params)

    async def create(self):
        narrated_video, cost = await self.create_narrated_video()
        return self.unpack(narrated_video), cost

    async def create_narrated_video(self):
        narration_w_bg = self.create_narration_with_background()
        video, cost = await self.studio.create_image_video(directory=self.output_dir)
        self.studio.loop_to_duration(video=video,
                                     target_duration=narration_w_bg.get_duration())
        self.studio.add_audio_track_to_video(video=video, audio=narration_w_bg)
        narration_w_bg.delete()
        return video, cost


class StorylineVideo(NarratedVideo):
    params_class = StorylineVideoParameters

    def __init__(self,
                 params: StorylineVideoParameters):
        super().__init__(params=params)

    async def create(self):
        subtitled_videos, cost = await self.create_subtitled_video()
        return subtitled_videos, cost

    async def create_subtitled_video(self):
        narrated_video, cost = await self.create_narrated_video()
        subtitled_videos = self.studio.produce_subtitled_videos(narrated_video)
        narrated_video.delete()
        return subtitled_videos, cost
