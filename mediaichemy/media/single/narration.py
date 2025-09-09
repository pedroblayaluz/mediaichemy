from mediaichemy.media.single.single import SingleMedia
from mediaichemy.media.parameters import NarrationParameters


class Narration(SingleMedia):
    params_class = NarrationParameters

    def __init__(self,
                 params: NarrationParameters):
        super().__init__(params=params)

    async def create(self):
        cost = None
        return self.studio.create_narration(self.output_dir), cost
