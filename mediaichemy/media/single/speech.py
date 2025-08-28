from ..media import SingleMedia
from ..parameters import SpeechParameters


class Speech(SingleMedia):
    def __init__(self,
                 params: SpeechParameters = SpeechParameters()):
        super().__init__(params=params)

    async def create(self):
        cost = None
        return self.studio.create_speech(self.output_dir), cost
