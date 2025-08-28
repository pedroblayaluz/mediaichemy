import shutil
from pathlib import Path
from types import SimpleNamespace


class MockRunwareClient:
    async def imageInference(self, requestImage=None, **kwargs):
        return [SimpleNamespace(imageURL="http://mock-url/image.jpg", cost=0.1)]

    async def videoInference(self, requestVideo=None, **kwargs):
        return [SimpleNamespace(videoURL="http://mock-url/video.mp4", cost=0.2)]


class MockAgent:
    def __init__(self, **kwargs):
        self.output_type = kwargs.get('output_type')

    async def run(self, prompt):
        if self.output_type:
            return self.output_type()
        return SimpleNamespace(output="Mock response text")


class MockDownloader:
    def __init__(self):
        self.mock_files = {}
        self.default_file = None

    def add_mock_file(self, extension, file_path):
        self.mock_files[extension.lower().lstrip('.')] = Path(file_path)
        if self.default_file is None:
            self.default_file = Path(file_path)

    def set_default(self, file_path):
        self.default_file = Path(file_path)

    def download(self, url, output_path):
        ext = Path(output_path).suffix.lower().lstrip('.')
        source_path = self.mock_files.get(ext, self.default_file)

        if source_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, output_path)
        else:
            Path(output_path).write_bytes(b"mock data")

        return output_path
