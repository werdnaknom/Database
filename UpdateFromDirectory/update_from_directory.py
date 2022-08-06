import typing as t
from pathlib import Path

import config


class UpdateFromDirectory():

    def __init__(self, base_directory: str):
        self.base_path = Path(base_directory)

    def query_directory(self, project: str = None, pba: str = None, rework: str = None,
                        serial: str = None, runid: str = None, test: str = None, capture: str = None,
                        hostname: str = None):
        pass

    def find_all_projects(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_PROJECT.format(project="*")
        return self.base_path.glob(pattern)


class UpdateFromDirectoryOREGON(UpdateFromDirectory):
    def __init__(self):
        or_dir = config.DirectoryConfiguration.ATS2_OR
        super().__init__(base_directory=or_dir)


class UpdateFromDirectoryKULIM(UpdateFromDirectory):
    def __init__(self):
        km_dir = config.DirectoryConfiguration.ATS2_KM
        super().__init__(base_directory=km_dir)
