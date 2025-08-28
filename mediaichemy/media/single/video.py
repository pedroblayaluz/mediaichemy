from ..media import SingleMedia
from ..parameters import VideoParameters


class Video(SingleMedia):
    def __init__(self,
                 params: VideoParameters = VideoParameters()):
        super().__init__(params=params)

    async def create(self):
        return await self.studio.create_video(self.output_dir)
