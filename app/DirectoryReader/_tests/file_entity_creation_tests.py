import tkinter
from pathlib import Path
from unittest import mock

from Entities.basicTestCase.basic_test_case import BasicTestCase

from app.DirectoryReader.read_runid_files import *

import numpy as np


class TestFileEntityCreationFromDirectory(BasicTestCase):
    logger_name = "FileEntityFromDict_Logger"

    def test_create_runid_comment_entity(self):
        mock_read = "This board is not in the database"
        fakepath = Path("Comments.txt")

        with mock.patch('builtins.open', mock.mock_open(read_data=mock_read)):
            ce = create_runid_comment_entity(comment_file_path=fakepath)

        self.assertIsInstance(ce, CommentsFileEntity)
        self.assertEqual(ce.comments, {"Test Setup Comment": mock_read})
        print(ce)

    def test_create_runid_comment_entity_empty_input(self):
        mock_read = ""
        fakepath = Path("Comments.txt")

        with mock.patch('builtins.open', mock.mock_open(read_data=mock_read)):
            ce = create_runid_comment_entity(comment_file_path=fakepath)

        self.assertIsInstance(ce, CommentsFileEntity)
        self.assertEqual(ce.comments, {"Test Setup Comment": mock_read})
        print(ce)

    def test_create_runid_power_entity(self):
        # fakecsv = Path(r"F:\ATS DATABASE\Maclaren Summit\M23728-001\0\07CG10\2381").joinpath("power.csv")
        # fakejson = Path(r"F:\ATS DATABASE\Maclaren Summit\M23728-001\0\07CG10\2381").joinpath("power.json")
        fakecsv = Path("files_used_for_tests/power.csv")
        fakejson = Path("files_used_for_tests/power.json")
        power_entity = create_runid_power_entity(csv_path=fakecsv, json_path=fakejson)

        #print(power_entity.dataframe.groupby("DUT Power State")["Total Power"].agg(['max', "mean"]).round(3).to_dict('index'))
        #{'Off': {'max': 0.125, 'mean': 0.124}}

        '''
        self.assertListEqual(power_entity.dataframe.columns.to_list(),
                             ['Time', 'Temperature Setpoint', 'Temperature', 'PCIE-12 Main Volts Setpoint',
                              'PCIE-12 Main Volts', 'PCIE-12 Main Current', 'PCIE-12 Main Power', 'PCIE-12 Main Slew',
                              'PCIE-12 Main State', 'PCIE 3.3 Main Volts Setpoint', 'PCIE 3.3 Main Volts',
                              'PCIE 3.3 Main Current', 'PCIE 3.3 Main Power', 'PCIE 3.3 Main Slew',
                              'PCIE 3.3 Main State', 'PCIE 3.3 Aux Volts Setpoint', 'PCIE 3.3 Aux Volts',
                              'PCIE 3.3 Aux Current', 'PCIE 3.3 Aux Power', 'PCIE 3.3 Aux Slew', 'PCIE 3.3 Aux State',
                              'Total Power', 'DUT Power State'])

        self.assertListEqual(power_entity.dataframe.dtypes.to_list(),
                             [np.dtype('<M8[ns]'), 'float', 'float', 'float', 'float', 'float', 'float', 'int',
                              pd.CategoricalDtype(categories=["On"]), 'float', 'float', 'float', 'float', 'int',
                              pd.CategoricalDtype(categories=["On"]), 'float', 'float', 'float', 'float', 'int',
                              pd.CategoricalDtype(categories=["On"]), 'float', pd.CategoricalDtype(categories=["Off"])])
        '''

    def test_create_runid_power_no_json(self):
        self.fail()

    def test_create_runid_power_no_csv(self):
        self.fail()

    def test_create_runid_multiple_power(self):
        self.fail()

    def test_create_runid_status_entity(self):
        mock_read = '{"Status":"Aborted","Time":"4/9/2021 10:05 AM","Info":"Test was aborted by user after 0 Hours 0 Minutes 55 Seconds","Runtime":{"Total Seconds":55,"Hours":0,"Minutes":0,"Seconds":55}}'
        fakepath = Path("status.json")

        with mock.patch('builtins.open', mock.mock_open(read_data=mock_read)):
            se = create_runid_status_entity(status_file_path=fakepath)

        self.assertEqual(se.status, "Aborted")
        self.assertEqual(se.time, "4/9/2021 10:05 AM")
        self.assertEqual(se.info, "Test was aborted by user after 0 Hours 0 Minutes 55 Seconds")
        self.assertEqual(se.runtime_seconds, 55)
        self.assertEqual(se.runtime_hours, 0)
        self.assertEqual(se.runtime_minutes, 0)
        self.assertEqual(se.runtime_total_seconds, 55)

    def test_create_runid_status_entity_empty(self):
        self.fail()

    def test_create_runid_system_info_entity(self):
        fakepath = Path("files_used_for_tests/System Info.json")

        sie = create_runid_system_info_entity(system_info_path=fakepath)
        # sie = create_runid_system_info_entity(system_info_path=path)

        print(sie)

        for i, probe in enumerate(sie.probes):
            self.assertIsInstance(probe, ProbesFileEntity)
            self.assertEqual(probe.channel, i + 1)
            self.assertEqual(probe.cal_status, "D")
            self.assertEqual(probe.deguass, True)
            self.assertIn(probe.part_number, ["TDP1000", "TCP0030A"])
            self.assertIsInstance(probe.serial_number, str)
        self.assertEqual(sie.ats_version, "ATS 2.0 Alpha 25_19E77")
        self.assertEqual(sie.power_supply_serial_number, "")
        self.assertEqual(sie.scope_serial_number, "")

    def test_create_runid_system_info_entity_empty(self):
        self.fail()

    def test_create_runid_testrun_entity(self):
        fakepath = Path("files_used_for_tests/testrun.json")

        tre = create_runid_testrun_entity(testrun_file_path=fakepath)
        print(tre)
        self.assertIsInstance(tre, TestRunFileEntity)
