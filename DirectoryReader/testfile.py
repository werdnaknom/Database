import typing as t
from pathlib import Path
import os
import time
from multiprocessing import Pool, cpu_count, Process, Queue
import logging
from PIL import Image
import io

import matplotlib.pyplot as plt
from dotenv import load_dotenv
import time
from dataclasses import dataclass
import pymongo

from read_runid_files import create_runid_comment_entity, create_runid_power_entity, create_runid_status_entity, \
    create_runid_testrun_entity, create_runid_system_info_entity
from read_capture_files import create_capture_settings_entity, create_capture_environment_entity, \
    create_capture_linkpartner_entity, create_capture_dut_entity
from Entities.Entities import *
from Entities.Helpers.path_translator import PathTranslator
from Entities.WaveformFunctions.waveform_analysis import WaveformAnalysis
from DirectoryReader.repo import Repo

from DirectoryPlotting.RunidPlotter import plot_runid_aux2main

START_LENGTH = 1
PROJECT = START_LENGTH + 1
PBA = START_LENGTH + 2
REWORK = START_LENGTH + 3
SERIAL = START_LENGTH + 4
RUNID = START_LENGTH + 5
TESTDIR = START_LENGTH + 6
TEST = START_LENGTH + 7
CAPTURE = START_LENGTH + 8
AUX_TO_MAIN = START_LENGTH + 8
ETHAGENT = START_LENGTH + 8
LEGACY_SCRIPT = START_LENGTH + 8
SYSTEM_SCRIPT = START_LENGTH + 9


class Lumberjack(logging.getLoggerClass()):
    # TODO: LOGGING
    pass


class AddFromDirectory():
    def __init__(self, dir: Path, repo: Repo):
        self.dir = dir
        self.repo = repo

    @classmethod
    def get_name_from_directory(cls, dir: Path):
        name = dir.name
        return name

    def get_parents(self) -> t.List[Path]:
        parents = [x for x in self.dir.parents]
        return parents

    def get_name(self):
        name = self.get_name_from_directory(dir=self.dir)
        return name

    def add(self):
        raise NotImplementedError

    def _get_dir_from_parents(self, parents: t.List[Path], current: int, destination: int):
        dir = parents[(current - destination) - 1]
        return dir

    def get_project_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=PROJECT)
        return AddProjectFromDirectory.get_name_from_directory(dir=dir)

    def get_pba_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=PBA)
        return AddPBAfromDirectory.get_name_from_directory(dir=dir)

    def get_rework_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=REWORK)
        return AddReworkfromDirectory.get_name_from_directory(dir=dir)

    def get_serial_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=SERIAL)
        return AddSerialFromDirectory.get_name_from_directory(dir=dir)

    def get_runid_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=RUNID)
        return AddRunidFromDirectory.get_name_from_directory(dir=dir)

    def get_testcategory_from_parents(self, parents: t.List[Path], current: int):
        dir = self._get_dir_from_parents(parents, current=current, destination=TEST)
        return AddAutomationTestFromDirectory.get_name_from_directory(dir=dir)


class AddProjectFromDirectory(AddFromDirectory):
    def add(self):
        project_entity = ProjectEntity(name=self.get_name())
        self.repo.insert_project(project_entity)


class AddPBAfromDirectory(AddFromDirectory):
    def add(self):
        project = self.dir.parent.name
        pba_entity = PBAEntity(part_number=self.get_name(), project=project)
        self.repo.insert_pba(pba_entity)


class AddReworkfromDirectory(AddFromDirectory):
    @classmethod
    def get_name_from_directory(cls, dir: Path) -> int:
        name = int(dir.name)
        return name

    def add(self):
        pba = self.dir.parent.name
        rework_entity = ReworkEntity(pba=pba, rework=self.get_name())
        self.repo.insert_rework(rework_entity)


class AddSerialFromDirectory(AddFromDirectory):
    def add(self):
        parents = self.get_parents()
        pba = self.get_pba_from_parents(parents=parents, current=SERIAL)
        rework = self.get_rework_from_parents(parents=parents, current=SERIAL)

        serial_entity = SubmissionEntity(submission=self.get_name(), rework=rework, pba=pba, )
        self.repo.insert_serialnumber(serial_entity)


class AddRunidFromDirectory(AddFromDirectory):
    @classmethod
    def get_name_from_directory(cls, dir: Path):
        # name_fmt = "{location}-{runid}"
        # location = cls.get_data_location(dir=dir)
        runid = int(dir.name)
        # return name_fmt.format(location=location, runid=runid)
        return runid

    @classmethod
    def get_data_location(cls, dir: Path) -> str:
        return "OR"

    def add(self):
        parents = self.get_parents()
        project = self.get_project_from_parents(parents=parents, current=RUNID)
        pba = self.get_pba_from_parents(parents=parents, current=RUNID)
        rework = self.get_rework_from_parents(parents=parents, current=RUNID)
        serial = self.get_serial_from_parents(parents=parents, current=RUNID)

        try:
            for file in self.dir.iterdir():
                if file.is_file():
                    if "Comments.txt" in file.name:
                        comments = create_runid_comment_entity(comment_file_path=file)
                    elif "dut.csv" in file.name:
                        pass
                    elif "dut.txt" in file.name:
                        pass
                    elif "logfile.txt" in file.name:
                        pass
                    elif "lp.csv" in file.name:
                        pass
                    elif "lp.txt" in file.name:
                        pass
                    elif "power.csv" in file.name:
                        pass
                    elif "power.json" in file.name:
                        pass
                    elif "settings.xml" in file.name:
                        pass
                    elif "status.json" in file.name:
                        status = create_runid_status_entity(status_file_path=file)
                    elif "steps.xml" in file.name:
                        pass
                    elif "System Info.json" in file.name:
                        system = create_runid_system_info_entity(system_info_path=file)
                    elif "testrun.json" in file.name:
                        testrun = create_runid_testrun_entity(testrun_file_path=file)

            # power_csv = self.dir.glob("power*.csv")
            # for power in power_csv:
            #    print(power)
            power_csv = self.dir.joinpath("power.csv")
            power_json = self.dir.joinpath("power.json")
            power_entity = create_runid_power_entity(csv_path=power_csv, json_path=power_json)

            runid = RunidEntity(runid=self.get_name(),
                                location=self.get_data_location(dir=self.dir),
                                comments=comments,
                                project=project,
                                pba=pba,
                                rework=rework,
                                serial=serial,
                                status=status,
                                system_info=system,
                                testrun=testrun,
                                power=power_entity)
            self.repo.insert_runid(runid)

        except (UnboundLocalError, FileNotFoundError) as e:
            print(project, pba, rework, serial, self.get_name(), "Failed with error:", e, "The file location is: ",
                  self.dir)

    def plot_runid_aux2main(self) -> plt.Figure:
        runid = self.get_name()
        # waveforms = self.repo.db[WaveformEntity.get_type()].find({"runid": self.get_name()}).count_documents()
        wfm_count = self.repo.db[WaveformEntity.get_type()].count_documents({"runid": self.get_name()})
        if wfm_count > 0:
            waveforms = self.repo.db[WaveformEntity.get_type()].find({"runid": self.get_name()})
            print(runid, "===", waveforms)
            fig, ax = plt.subplots()
            for wfm in waveforms:
                wfm_ent = WaveformEntity.from_dict(wfm)
                ax.plot(wfm_ent.x_axis_in_milliseconds(), wfm_ent.y_axis())

            return fig

    def save_runid_aux2main(self, fig: plt.Figure, testname="aux2main") -> Path:
        runid = self.get_name()
        figname = "{runid}_{test}.png".format(runid=runid, test=testname)
        save_path = Path(r"F:\Output DATABASE").joinpath(figname)
        fig.savefig(save_path)
        return save_path

    def create_image_buffer(self, fig: plt.Figure, format: str = "png"):
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format=format)
        return img_buf

    def clear_figure(self, fig: plt.Figure):
        fig.clf()
        plt.close(fig)
        plt.clf()
        plt.cla()

    def insert_runid_image(self, path: Path, buffer: io.BytesIO, image_name: str):
        pt = PathTranslator(path_name=image_name, path_str=str(path.resolve()))
        im = ImageEntity(name=image_name, image_base64=buffer.getvalue(), image_str=pt.path_str)
        col = self.repo.db['Images']
        print(image_name)
        im_dict = im.to_dict()
        inserted_id = col.insert_one(im.to_dict()).inserted_id
        return inserted_id


class AddWaveformCaptureFromDirectory(AddFromDirectory):
    @classmethod
    def get_name_from_directory(cls, dir: Path) -> int:
        name = int(dir.name)
        return name

    def add(self):
        capture = self.get_name()
        capture_settings = create_capture_settings_entity(self.dir.joinpath("capture.json"))
        environment = create_capture_environment_entity(self.dir.joinpath("temperature power settings.json"))
        runid = self.get_runid_from_parents(parents=self.get_parents(), current=AUX_TO_MAIN)
        test_category = self.dir.parent.name
        capture_path = PathTranslator(path_str=str(self.dir.joinpath("capture.png").resolve()),
                                      path_name="capture_image")
        aux2main = WaveformCaptureEntity(capture=capture, capture_settings=capture_settings, environment=environment,
                                         runid=runid, test_category=test_category, capture_image=capture_path)
        self.repo.insert_capture(aux2main)

        waveforms = AddAllWaveformsFromDirectory(dir=self.dir, repo=self.repo)
        waveforms.add()

        return aux2main

    def plot_capture(self, capture: WaveformCaptureEntity) -> plt.Figure:
        """
        Do I actually care about this? Just use the scope capture.
        :param capture:
        :return:
        """
        col = self.repo.db[WaveformEntity.get_type()]
        found = col.find(capture.get_filter())
        fig, ax = plt.subplots()
        for f in found:
            wfm = WaveformEntity.from_mongo(adict=f)
            ax.plot(wfm.x_axis_in_milliseconds(), wfm.y_axis())

        return fig


class AddAllWaveformsFromDirectory(AddFromDirectory):

    def add(self):
        CHANNEL_BINARY_FMT = "CH{}.bin"
        capture_settings = create_capture_settings_entity(self.dir.joinpath("capture.json"))
        if not capture_settings:
            return None
        name_files = capture_settings.waveform_names
        parents = self.get_parents()
        runid = self.get_runid_from_parents(parents=parents, current=CAPTURE)

        test_category = self.get_testcategory_from_parents(parents=parents, current=CAPTURE)
        capture = int(self.dir.name)

        # processes = []
        for i, testpoint_name in enumerate(name_files):
            index = i + 1
            bin_file = self.dir.joinpath(CHANNEL_BINARY_FMT.format(index))

            pt = PathTranslator(path_str=str(bin_file.resolve()), path_name=testpoint_name)
            '''
            p = Process(target=multiprocessing_waveform,
                        args=(index, runid, capture, test_category, testpoint_name, pt))
            processes.append(p)
            p.start()
            '''
            exists_ = self.repo.check_waveform(runid=runid, testpoint=testpoint_name, scope_channel=index,
                                               capture=capture,
                                               test_category=test_category)
            if not exists_:
                wfm = multiprocessing_waveform(channel=index, name=testpoint_name, pt=pt, capture=capture,
                                               runid=runid, test_category=test_category)
                self.repo.insert_waveform(wfm)

            '''
            '''
        for proc in processes:
            proc.join()


def multiprocessing_waveform(channel: int, runid: int, capture: int, test_category: str, name: str, pt: PathTranslator):
    wfm_analysis = WaveformAnalysis()
    wf_y = wfm_analysis.read_binary_waveform(pt.path, compressed=False)
    wf_x = wfm_analysis.create_waveform_x_coords(x_increment=8.0000000000000001674e-08, length=wf_y.size)
    downsample = wfm_analysis.min_max_downsample_2d(wf_x=wf_x, wf_y=wf_y, size=500)
    wfm = WaveformEntity(testpoint=name, runid=runid, capture=capture, test_category=test_category,
                         units="UNITSNEEDTOBEFOUND", location=pt.path_str, scope_channel=channel, downsample=downsample)

    # TODO:: Have the waveform creation task do this itself!
    target = wfm_analysis.find_cutoff_target_by_percentile(wf=wf_y)
    ss_index = wfm.steady_state_index(expected_voltage=target * 0.9)
    wfm.steady_state_mean = round(wf_y[ss_index].mean(), 2)
    wfm.set_steady_state_index(index=0)
    wfm.max = round(wf_y.max(), 2)
    wfm.min = round(wf_y.min(), 2)
    wfm.steady_state_max = round(wf_y[ss_index:].max(), 2)
    wfm.steady_state_min = round(wf_y[ss_index:].min(), 2)
    wfm.steady_state_pk2pk = wfm.steady_state_max - wfm.steady_state_min
    return wfm


class AddEthAgentCaptureFromDirectory(AddFromDirectory):
    @classmethod
    def get_name_from_directory(cls, dir: Path) -> int:
        name = int(dir.name)
        return name

    def add(self):
        capture = self.get_name()
        runid = self.get_runid_from_parents(parents=self.get_parents(), current=ETHAGENT)
        test_category = self.dir.parent.name
        environment = create_capture_environment_entity(self.dir.joinpath("temperature power settings.json"))
        lp = create_capture_linkpartner_entity(self.dir.joinpath("Link Partner.json"))
        dut = create_capture_dut_entity(self.dir.joinpath("DUT.json"))

        ethagent = EthAgentCaptureEntity(capture=capture, runid=runid, test_category=test_category,
                                         environment=environment, lp=lp, dut=dut)

        self.repo.insert_capture(ethagent)


class AddScriptCaptureFromDirectory(AddFromDirectory):

    @classmethod
    def get_name_from_directory(cls, dir: Path) -> int:
        name = int(dir.name)
        return name

    def check_if_system_device_names(self) -> bool:
        dir_name = self.dir.name
        if dir_name.isdigit():
            return False
        else:
            return True

    def add(self, system: str = None, depth: int = None):
        dir_name = self.dir.name  # can't use get_name function because it could be system or legacy
        if not system:
            if self.check_if_system_device_names():  #
                for capture_dur in self.dir.iterdir():
                    if capture_dur.is_dir():
                        ad = AddScriptCaptureFromDirectory(dir=capture_dur, repo=self.repo)
                        ad.add(system=dir_name, depth=SYSTEM_SCRIPT)
            else:
                self.add(system="Legacy Script", depth=LEGACY_SCRIPT)

        else:
            capture = self.get_name()
            runid = self.get_runid_from_parents(parents=self.get_parents(), current=depth)
            test_category = "Scripts"
            text_files = {}
            for file in self.dir.iterdir():
                if file.is_file():
                    text_files[file.name] = str(file.resolve())

            script = ScriptCaptureEntity(capture=capture, runid=runid, system=system, text_files=text_files,
                                         test_category=test_category)

            self.repo.insert_capture(script)

        '''
        capture = self.get_name()
        

        script = ScriptCaptureEntity(capture=capture, runid=runid, system=system,
                                     test_category=test_category,
                                     text_files=text_files, environment=environment)
        self.repo.insert_capture(script)
        '''


class AddAutomationTestFromDirectory(AddFromDirectory):
    def add(self):
        autotest = AutomationTestEntity(name=self.get_name())
        self.repo.insert_automationtest(autotest)


@dataclass
class read_directory():
    dir: Path
    _name: str = "BaseClass"

    def return_entity(self):
        if self._name == "Project":
            return ProjectEntity(name=self.dir.name)
        elif self._name == "PBA":
            return PBAEntity(part_number=self.dir.name, project=self.dir.parent.name)
        elif self._name == "REWORK":
            return ReworkEntity(pba=self.dir.parent.name, rework=int(self.dir.name))
        elif self._name == "SERIAL":
            # parents = list(self.dir.parents)
            parents = [x for x in self.dir.parents]
            pba = parents[REWORK - PBA].name
            return SubmissionEntity(submission=self.dir.name, rework=int(self.dir.parent.name),
                                    pba=pba)
        elif self._name == "RUNID":
            return RunidEntity(runid=int(self.dir.name),
                               comments="",
                               status="",
                               system_info="",
                               testrun="")

        elif self._name == "AutomationTest":
            return AutomationTestEntity(name=self.dir.name)


def create_aux2main_multiprocessing(dir_str: str, repo: Repo):
    path = Path(dir_str)
    print("starting", dir)
    ad = AddWaveformCaptureFromDirectory(dir=path, repo=repo)
    ad.add()


if __name__ == "__main__":
    # timing_desc = input("What timing is this?")
    # print(timing_desc, "Starting")
    timing_desc = "Just running"
    start_time = time.time()
    load_dotenv()

    repo = Repo()

    dir = os.environ.get("OR_ATS_DIRECTORY")
    p = Path(dir)
    '''
    print(p.exists())
    for dir in p.iterdir():
        print(dir)
        print(dir.parent)
        parents = list(dir.parents)
        print(parents)
    '''
    processes = []

    for d in p.rglob("*"):
        if d.is_dir():
            list = d.parents
            parent_len = len(list)
            if parent_len == PROJECT:
                ad = AddProjectFromDirectory(dir=d, repo=repo)
                ad.add()
                # project = read_directory(dir=d, _name="Project")
                # print("PROJECT", project.return_entity())
            elif parent_len == PBA:
                ad = AddPBAfromDirectory(dir=d, repo=repo)
                ad.add()
                # x = read_directory(dir=d, _name="PBA")
                # print("PBA: ", x.return_entity())
            elif parent_len == REWORK:
                ad = AddReworkfromDirectory(dir=d, repo=repo)
                ad.add()
                # x = read_directory(dir=d, _name="REWORK")
                # print("REWORK: ", x.return_entity())
            elif parent_len == SERIAL:
                ad = AddSerialFromDirectory(dir=d, repo=repo)
                ad.add()
                # x = read_directory(dir=d, _name="SERIAL")
                # print("SERIAL :", x.return_entity())
            elif parent_len == RUNID:
                ad = AddRunidFromDirectory(dir=d, repo=repo)
                runid = ad.add()
                # x = read_directory(dir=d, _name="RUNID")
                # print("RUNID :", x.return_entity())
                runid_img = "{runid}_aux2main".format(runid=ad.get_name())
                print(runid_img)
                count = repo.db['Images'].count_documents({"name": runid_img})
                if count == 0:
                    fig = ad.plot_runid_aux2main()
                    if fig:
                        save_path = ad.save_runid_aux2main(fig=fig, testname="aux2main")
                        save_buffer = ad.create_image_buffer(fig=fig, format="png")
                        ad.insert_runid_image(path=save_path, buffer=save_buffer,
                                              image_name=runid_img)
                        ad.clear_figure(fig)


            elif parent_len == TESTDIR:
                pass
            elif parent_len == TEST:
                ad = AddAutomationTestFromDirectory(dir=d, repo=repo)
                ad.add()
                # x = read_directory(dir=d, _name="AutomationTest")
                # print("TESTCATEGORY :", x.return_entity())
            elif parent_len == CAPTURE:
                parent_name = d.parent.name
                if parent_name == "Scripts":
                    ad = AddScriptCaptureFromDirectory(dir=d, repo=repo)
                    ad.add()
                elif parent_name == "Aux To Main":
                    ''' MULTIPROCESSING '''
                    ''' Alway fails with threadlock error?
                    p = Process(target=create_aux2main_multiprocessing, args=(str(d.resolve()), repo))
                    processes.append(p)
                    p.start()
                    '''
                    ad = AddWaveformCaptureFromDirectory(dir=d, repo=repo)
                    entity = ad.add()
                elif parent_name == "EthAgent":
                    ad = AddEthAgentCaptureFromDirectory(dir=d, repo=repo)
                    ad.add()

            else:
                pass

    for proc in processes:
        proc.join()
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("ELAPSED: ", elapsed_time)
    ''' Write Elapsed Time'''
    with open(r"F:\timing_database.txt", "a") as f:
        f.write("{} \t\t\t\telapsed: {:.0f} seconds\n".format(timing_desc, elapsed_time))
