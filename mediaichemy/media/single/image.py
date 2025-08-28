from ..media import SingleMedia
from ..parameters import ImageParameters


class Image(SingleMedia):
    def __init__(self,
                 params: ImageParameters = ImageParameters()):
        super().__init__(params=params)

    async def create(self):
        return await self.studio.create_image(self.output_dir)
