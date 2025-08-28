from mediaichemy.media.multi.narration_with_background import NarrationWithBackground
from mediaichemy.media.parameters import NarratedVideoParameters


class NarratedVideo(NarrationWithBackground):
    def __init__(self,
                 params: NarratedVideoParameters = NarratedVideoParameters()):
        super().__init__(params=params)

    async def create(self):
        narrated_video, cost = await self.create_narrated_video()
        return self.unpack(narrated_video), cost

    async def create_narrated_video(self):
        narration_w_bg = self.create_narration_with_background()
        video, cost = await self.studio.create_video_from_image(directory=self.output_dir)
        self.studio.loop_to_duration(video=video,
                                     target_duration=narration_w_bg.get_duration())
        self.studio.add_audio_track_to_video(video=video, audio=narration_w_bg)
        narration_w_bg.delete()
        return video, cost
