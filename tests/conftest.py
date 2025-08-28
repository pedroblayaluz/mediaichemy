import random
import pytest

from mediaichemy.studio.media_sources import ai
from mediaichemy.file import HTTPDownloader

from tests._mocks.mockers import MockDownloader, MockRunwareClient, MockAgent
from tests._mocks.files import mocks as mock_files


@pytest.fixture(autouse=True)
def mock_downloader(monkeypatch):
    mock = MockDownloader()

    mock.add_mock_file("jpg", mock_files.image.path)
    mock.add_mock_file("mp4", mock_files.video.path)

    monkeypatch.setattr(HTTPDownloader, "download", mock.download)
    monkeypatch.setattr(ai.VisualAI, "download", staticmethod(mock.download))

    return mock


@pytest.fixture(autouse=True)
def mock_runware_client(monkeypatch):
    async def get_mock_client(*args, **kwargs):
        return MockRunwareClient()
    monkeypatch.setattr(ai.VisualAI, "_get_runware_client", get_mock_client)
    return get_mock_client


@pytest.fixture(autouse=True)
def mock_agent(monkeypatch):
    def get_mock_agent(*args, **kwargs):
        return MockAgent(**kwargs)
    monkeypatch.setattr(ai.ChatAI, "_get_openai_model", get_mock_agent)
    return get_mock_agent


@pytest.fixture(autouse=True)
def mock_media_directory(monkeypatch):
    from mediaichemy.media.media import Media

    @property
    def mock_directory(self):
        test_path = f"test_output/{self.name}/"
        return test_path

    monkeypatch.setattr(Media, 'directory', mock_directory)

    yield


@pytest.fixture(autouse=True)
def mock_random_start(monkeypatch):
    def mock_randint(a, b):
        return 10
    monkeypatch.setattr(random, "randint", mock_randint)
    return mock_randint


@pytest.fixture(autouse=True)
def mock_narration_synthesis(monkeypatch):

    def mock_synthesize(self, text, output_path, voice_name):
        mock_audio = mock_files.narration
        output = mock_audio.copy(output_path)
        return output

    monkeypatch.setattr(ai.VoiceAI, "synthesize_speech", mock_synthesize)
