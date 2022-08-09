from pathlib import Path

import config
from config import DirectoryConfiguration
import datetime
import logging
import requests

from UpdateFromDirectory.update_from_directory import UpdateFromDirectory, UpdateFromDirectoryKULIM, \
    UpdateFromDirectoryOREGON

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.Logger(__name__)


def find_scripts():
    OR_DIR = Path(DirectoryConfiguration.ATS2_KM)
    test = DirectoryConfiguration.DIR_FMT_TEST.format(project="*", pba="*", rework="*", serial_number="*", runid="*",
                                                      test="Scripts")
    latest_time = 0
    latest = None
    for x in OR_DIR.glob(test):
        ctime = x.lstat().st_ctime
        if ctime > latest_time:
            latest_time = ctime
            latest = x

    print(datetime.datetime.fromtimestamp(latest_time))
    print(latest)


def projects(directory: UpdateFromDirectory):
    for path in directory.find_all_projects():
        logger.warning(f"ADDING PROJECT: {path}")
        url = config.Config.WEBSITE_URL + "/api/add_project"
        r = requests.post(url, json={"name": path.name,
                                     "path": str(path.resolve())})
        print(r.text, r.status_code)


def pbas(directory: UpdateFromDirectory):
    for path in directory.find_all_pbas():
        logger.warning(f"ADDING PBA: {path}")


def reworks(directory: UpdateFromDirectory):
    for path in directory.find_all_reworks():
        logger.warning(f"ADDING REWORK: {path}")


def serial_numberss(directory: UpdateFromDirectory):
    for path in directory.find_all_serial_numbers():
        logger.warning(f"ADDING SERIAL NUMBER: {path}")


def runids(directory: UpdateFromDirectory):
    for path in directory.find_all_runids():
        logger.warning(f"ADDING RUNID: {path}")


def tests(directory: UpdateFromDirectory):
    for path in directory.find_all_tests():
        logger.warning(f"ADDING TESTS: {path}")


def captures(directory: UpdateFromDirectory):
    for path in directory.find_all_captures():
        logger.warning(f"ADDING CAPTURES: {path}")


def hosts(directory: UpdateFromDirectory):
    for path in directory.find_all_hosts():
        logger.warning(f"ADDING HOSTS: {path}")


def main():
    OREGON = UpdateFromDirectoryOREGON()
    # KULIM = UpdateFromDirectoryKULIM()
    directories = [OREGON]

    for directory in directories:
        projects(directory=directory)
        '''
        pbas(directory=directory)
        reworks(directory=directory)
        serial_numberss(directory=directory)
        runids(directory=directory)
        tests(directory=directory)
        captures(directory=directory)
        hosts(directory=directory)
        '''


if __name__ == "__main__":
    main()
