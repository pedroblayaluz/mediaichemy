import os
from runware import Runware, IImageInference, IVideoInference
import inspect
from functools import wraps
from abc import ABC, abstractmethod
from mediaichemy.file import VideoFile, ImageFile, HTTPDownloader


def filter_params_for(target_func):
    """Decorator that filters kwargs to only include parameters that target_func accepts."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            sig = inspect.signature(target_func)

            filtered_kwargs = {
                k: v for k, v in kwargs.items()
                if k in sig.parameters
            }
            return await func(self, *args, **filtered_kwargs)
        return wrapper
    return decorator


class VisualAI(ABC):
    def __init__(self, runware_api_key: str = os.getenv("RUNWARE_API_KEY", "")):
        self.runware_api_key = runware_api_key

    @abstractmethod
    async def create(self,
                     prompt: str,
                     output_path: str,
                     **kwargs):
        pass

    async def _get_runware_client(self):
        runware_client = Runware(api_key=self.runware_api_key)
        await runware_client.connect()
        return runware_client

    def _set_defaults(self, **kwargs):
        kwargs.setdefault('includeCost', True)
        kwargs.setdefault('numberResults', 1)
        return kwargs

    @staticmethod
    def download(url, output_path):
        HTTPDownloader().download(url, output_path)


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


class VideoAI(VisualAI):
    @filter_params_for(IVideoInference.__init__)
    async def _create_video_inference(self, prompt, **kwargs) -> IVideoInference:
        print(kwargs)
        """Create IVideoInference object with filtered parameters."""
        return IVideoInference(
            positivePrompt=prompt,
            **kwargs
        )

    async def create(self,
                     prompt,
                     output_path,
                     **kwargs) -> VideoFile:
        client = await self._get_runware_client()
        kwargs = self._set_defaults(**kwargs)
        kwargs['model'] = kwargs.pop('video_model')
        inference_object = await self._create_video_inference(prompt, **kwargs)
        videos = await client.videoInference(requestVideo=inference_object)
        ivideo = videos[0]
        video = self.download(ivideo.videoURL, output_path)
        return VideoFile(video), ivideo.cost


class VideoFromImageAI(VisualAI):
    async def create(self,
                     prompt,
                     image_output_path,
                     video_output_path,
                     **kwargs) -> VideoFile:
        image_ai = ImageAI(runware_api_key=self.runware_api_key)
        image, image_cost = await image_ai.create(
            prompt=prompt,
            output_path=image_output_path,
            **kwargs
        )

        video_ai = VideoAI(runware_api_key=self.runware_api_key)
        video, video_cost = await video_ai.create(
            prompt=prompt,
            output_path=video_output_path,
            frameImages=[image.to_iframe_image()],
            **kwargs
        )
        image.delete()
        total_cost = image_cost + video_cost
        return video, total_cost
