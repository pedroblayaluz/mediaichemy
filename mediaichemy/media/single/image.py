from mediaichemy.media.single.single import SingleMedia
from mediaichemy.media.parameters import ImageParameters


class Image(SingleMedia):
    params_class = ImageParameters

    def __init__(self,
                 params: ImageParameters):
        super().__init__(params=params)

    async def create(self):
        return await self.studio.create_image(self.output_dir)
