from runware import IImageInference
from mediaichemy.file import ImageFile
from mediaichemy.ai.visual.visual import VisualAI, filter_params_for


class ImageAI(VisualAI):
    @filter_params_for(IImageInference.__init__)
    async def _create_image_inference(self, prompt, **kwargs) -> IImageInference:
        """Create IImageInference object with filtered parameters."""
        return IImageInference(
            positivePrompt=prompt,
            **kwargs
        )

    async def create(self,
                     prompt,
                     output_path,
                     **kwargs) -> ImageFile:
        client = await self._get_runware_client()
        kwargs = self._set_defaults(**kwargs)
        kwargs['model'] = kwargs.pop('image_model')
        inference_object = await self._create_image_inference(prompt, **kwargs)
        images = await client.imageInference(requestImage=inference_object)
        iimage = images[0]
        image = self.download(iimage.imageURL, output_path)
        return ImageFile(image), iimage.cost
