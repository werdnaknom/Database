import numpy as np
import typing as t
from pathlib import Path
import json

import pandas as pd

from Entities.Entities import CommentsFileEntity, RunidPowerCSVFileEntity, StatusFileEntity, TestRunFileEntity, \
    SystemInfoFileEntity, ProbesFileEntity


def create_runid_comment_entity(comment_file_path: Path) -> CommentsFileEntity:
    with open(comment_file_path) as file:
        read = file.read()

    cfe = CommentsFileEntity(comments=read)
    return cfe


def create_runid_power_entity(csv_path: Path, json_path: Path) -> RunidPowerCSVFileEntity:
    with open(json_path, 'r') as file:
        read = file.read()
        json_headers = json.loads(read)

    column_headers = []
    column_datatypes = []
    for header in json_headers:
        col_header = header["Header"]
        if col_header:
            column_headers.append(header["Header"])
            column_datatypes.append(header["Type"])
    csv_df = pd.read_csv(csv_path, sep=",", names=column_headers, index_col=False)
    try:
        ''' CSV DF CLEANUP '''
        for datatype, col_header in zip(column_datatypes, column_headers):
            if datatype == "timestamp":
                csv_df[col_header] = pd.to_datetime(csv_df[col_header])
            elif datatype == "float":
                csv_df[col_header] = csv_df[col_header].astype(float)
            elif datatype == "integer":
                csv_df[col_header] = csv_df[col_header].astype(int)
            elif datatype == "string":
                csv_df[col_header] = pd.Categorical(csv_df[col_header])

        max_power = round(csv_df["Total Power"].max(), 2)

        if "DUT Power State" in csv_df.columns:
            power_states = csv_df.groupby("DUT Power State")["Total Power"].agg(['max', "mean"]).round(3).to_dict(
                'index')
        else:
            power_states = {"Power": csv_df["Total Power"].agg(['max', 'mean']).round(3).to_dict()}
    except KeyError as e:
        print(csv_path, " failed due to: ", e)
        power_states = {}
        max_power = 0

    rpcfe = RunidPowerCSVFileEntity(dataframe=power_states, max_power=max_power)
    return rpcfe


def create_runid_status_entity(status_file_path: Path) -> StatusFileEntity:
    with open(status_file_path, "r") as file:
        read = file.read()
        jdict = json.loads(read)

    status = jdict["Status"]
    time = jdict["Time"]
    info = jdict["Info"]
    runtime = jdict["Runtime"]

    rhours = runtime["Hours"]
    rmin = runtime["Minutes"]
    rsec = runtime["Seconds"]
    rtotal_sec = runtime["Total Seconds"]

    sfe = StatusFileEntity(status=status, time=time, info=info, runtime_hours=rhours, runtime_minutes=rmin,
                           runtime_seconds=rsec, runtime_total_seconds=rtotal_sec)
    return sfe


def create_runid_system_info_entity(system_info_path: Path) -> SystemInfoFileEntity:
    with open(system_info_path, 'r') as file:
        read = file.read()
        jdict = json.loads(read)

    probes_list = jdict["Probes"]
    probe_entities = []
    for probe in probes_list:
        channel = int(probe.get("Channel", "").strip()[-1])
        probe_part_number = probe.get("Type", "").strip()
        serial_number = probe.get("Serial Number", "").strip()
        probe_units = probe.get("Units", "").strip()
        cal_status = probe.get("Cal Status", "").strip()
        degauss = probe.get("Degauss Cycle State", "").strip()
        degauss = degauss == "PASS"
        dynamic_range = probe.get("Dynamic Range", 0)
        probe_entity = ProbesFileEntity(channel=channel, part_number=probe_part_number,
                                        serial_number=serial_number, units=probe_units,
                                        cal_status=cal_status, deguass=degauss, dynamic_range=dynamic_range)
        probe_entities.append(probe_entity)

    scope = jdict["Scope Serial Number"]
    power = jdict["Power Supply Serial Number"]
    ats_ver = jdict["ATS Version"]
    sife = SystemInfoFileEntity(probes=probe_entities, scope_serial_number=scope, power_supply_serial_number=power,
                                ats_version=ats_ver)
    return sife


def create_runid_testrun_entity(testrun_file_path: Path) -> TestRunFileEntity:
    with open(testrun_file_path, 'r') as file:
        read = file.read()
        jdict = json.loads(read)

    dut = jdict["DUT"]
    pba = jdict["PBA"]
    rework = jdict["Rework"]
    serial = jdict["Serial Number"]
    tech = jdict["Technician"]
    station = jdict["Test Station"]
    testpoint_list = jdict["Test Points"]
    testpoint_dict = {}
    for index, testpoint in enumerate(testpoint_list):
        testpoint_dict[str(index)] = testpoint
    test_config = jdict["Configuration"]
    board_id = jdict["Board ID"]

    trfe = TestRunFileEntity(dut=dut, pba=pba, rework=rework, serial_number=serial, technician=tech,
                             test_station=station,
                             configuration=test_config, board_id=board_id,
                             test_points=testpoint_dict)
    return trfe
