from mediaichemy.media.multi.multi import MultiMedia
from mediaichemy.media.parameters import NarrationWithBackgroundParameters


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
