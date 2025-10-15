from mediaichemy.media.multi.multi import MultiMedia
from mediaichemy.media.parameters import ImageVideoParameters


class ImageVideo(MultiMedia):
    params_class = ImageVideoParameters

    def __init__(self,
                 params: ImageVideoParameters):
        super().__init__(params=params)

    async def create(self):
        video, cost = await self.studio.create_image_video(self.output_dir)
        return self.unpack(video), cost
