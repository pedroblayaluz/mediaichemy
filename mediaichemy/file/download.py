import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from . import utils
from logging import getLogger
logger = getLogger(__name__)


class HTTPDownloader:
    """
    HTTP downloader with urllib3 Retry. Session-building is extracted for clarity.
    """

    def __init__(self, *, max_retries: int = 5, backoff_factor: float = 0.5, timeout: int = 20):
        self.timeout = timeout
        # keep retry config as instance attributes so _build_session is simple
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        """Create a requests.Session configured with urllib3 Retry + HTTPAdapter."""
        session = requests.Session()
        retry = Retry(
            total=self._max_retries,
            backoff_factor=self._backoff_factor,
            status_forcelist=[422, 429, 500, 502, 503, 504],
            allowed_methods={"GET"},
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def download(self, url: str, destination: str) -> str:
        """
        Download the URL to destination (streaming write). Returns the destination path.
        Ensures destination directory exists.
        """
        logger.info(f"Downloading {url} to {destination}")
        dest_dir = os.path.dirname(destination) or "."
        utils.ensure_dir(dest_dir)

        resp = self.session.get(url, stream=True, timeout=self.timeout)
        resp.raise_for_status()

        with open(destination, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    fh.write(chunk)
        logger.debug(f"Finished downloading {url} to {destination}")
        return destination
