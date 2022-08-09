import typing as t
from pathlib import Path
import logging
import config

logger = logging.Logger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class UpdateFromDirectory():

    def __init__(self, base_directory: str):
        self.base_path = Path(base_directory)

    def query_directory(self, project: str = None, pba: str = None, rework: str = None,
                        serial: str = None, runid: str = None, test: str = None, capture: str = None,
                        hostname: str = None):
        pass

    def split_all(self, match_pattern: str) -> t.Iterable[Path]:
        return self.base_path.glob(match_pattern)

    def find_all_projects(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_PROJECT.format(project="*")
        logger.info(f"Searching with glob: {pattern}")

        return self.split_all(match_pattern=pattern)

    def find_all_pbas(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_PBA.format(project="*", pba="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_reworks(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_REWORK.format(project="*", pba="*", rework="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_serial_numbers(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_SERIAL.format(project="*", pba="*", rework="*",
                                                                      serial_number="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_runids(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_RUNID.format(project="*", pba="*", rework="*",
                                                                     serial_number="*", runid="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_tests(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_TEST.format(project="*", pba="*", rework="*",
                                                                    serial_number="*", runid="*", test="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_captures(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_CAPTURE.format(project="*", pba="*", rework="*",
                                                                       serial_number="*", runid="*", test="*",
                                                                       capture="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)

    def find_all_hosts(self) -> t.Iterable[Path]:
        pattern = config.DirectoryConfiguration.DIR_FMT_SCRIPTS_HOST.format(project="*", pba="*", rework="*",
                                                                            serial_number="*", runid="*", test="Script",
                                                                            capture="*", host="*")
        logger.info(f"Searching with glob: {pattern}")
        return self.split_all(match_pattern=pattern)


class UpdateFromDirectoryOREGON(UpdateFromDirectory):
    def __init__(self):
        or_dir = config.DirectoryConfiguration.ATS2_OR
        super().__init__(base_directory=or_dir)


class UpdateFromDirectoryKULIM(UpdateFromDirectory):
    def __init__(self):
        km_dir = config.DirectoryConfiguration.ATS2_KM
        super().__init__(base_directory=km_dir)
