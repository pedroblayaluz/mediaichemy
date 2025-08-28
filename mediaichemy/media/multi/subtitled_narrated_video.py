
from mediaichemy.media.multi.narrated_video import NarratedVideo
from mediaichemy.media.parameters import SubtitledNarratedVideoParameters


class SubtitledNarratedVideo(NarratedVideo):
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
