from pathlib import Path

from .extractable import ExtractableFn
from .archives import Tar as TarArchive, Zip as ZipArchive
from .downloader import download_if_missing


class DataSet:
    file_path: str = "<unknown>"
    file_type: ExtractableFn = ZipArchive

    @classmethod
    def download(cls, output_directory: str | Path) -> None:
        download_if_missing(
            archive_name=cls.file_path, output_directory=output_directory
        )


class MitBihAtrialFibrillationDataSet(DataSet):
    file_name = "mit-bih-atrial-fibrillation.tar"
    file_type = TarArchive
