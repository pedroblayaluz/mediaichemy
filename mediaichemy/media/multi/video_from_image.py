from mediaichemy.media.multi.multi import MultiMedia
from mediaichemy.media.parameters import VideoFromImageParameters


class VideoFromImage(MultiMedia):
    params_class = VideoFromImageParameters

    def __init__(self,
                 params: VideoFromImageParameters):
        super().__init__(params=params)

    async def create(self):
        video_from_image, cost = await self.studio.create_video_from_image(self.output_dir)
        return self.unpack(video_from_image), cost
