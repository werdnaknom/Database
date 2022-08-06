from pathlib import Path
from config import DirectoryConfiguration
import datetime

from UpdateFromDirectory.update_from_directory import UpdateFromDirectory, UpdateFromDirectoryKULIM, \
    UpdateFromDirectoryOREGON


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
    for project_path in directory.find_all_projects():
        print(project_path.name, project_path.)


def main():
    OREGON = UpdateFromDirectoryOREGON()
    KULIM = UpdateFromDirectoryKULIM()

    projects(directory=OREGON)
    projects(directory=KULIM)


if __name__ == "__main__":
    main()
