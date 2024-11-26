from pathlib import Path
from .extractable import ExtractableFn
from .archives import Tar as TarArchive
from .downloader import download_if_missing, download


class DataSet:
    def __init__(self, file_path: str, file_type: ExtractableFn) -> None:
        self._file_path = file_path
        self._file_type = file_type

    @property
    def file_type(self) -> ExtractableFn:
        return self._file_type

    @property
    def file_path(self) -> str:
        return self._file_path

    def download(self, output_directory: str | Path) -> None:
        download(dataset=self, output_directory=output_directory)

    def download_if_missing(self, output_directory: str | Path) -> None:
        download_if_missing(dataset=self, output_directory=output_directory)



MitBihAtrialFibrillationDataSet = DataSet(
    file_path="mit-bih-atrial-fibrillation.tar", file_type=TarArchive
)
