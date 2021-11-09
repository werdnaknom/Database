import typing as t
import json
from pathlib import Path

from Entities.Entities.file_entities import CaptureSettingsEntity, CaptureEnvironmentFileEntity, \
    CapturePowerCSVFileEntity, PowerSupplyChannel, LPTrafficFileEntity, DUTTrafficFileEntity, Port


def create_capture_settings_entity(capture_settings_file_path: Path) -> CaptureSettingsEntity:
    try:
        with open(capture_settings_file_path, 'r') as file:
            read = file.read()
            jdict = json.loads(read)

        init_x = jdict["initial x"]
        x_incr = jdict["x increment"]
        compress = jdict['compress']
        names = jdict['names']

        cse = CaptureSettingsEntity(initial_x=init_x, compress=compress, x_increment=x_incr, waveform_names=names)

        return cse
    except FileNotFoundError as e:
        print("Attempted to create capture entity but failed to find the file: ", capture_settings_file_path, e)


def create_capture_environment_entity(environment_file_path: Path) -> CaptureEnvironmentFileEntity:
    try:
        with open(environment_file_path, 'r') as file:
            read = file.read()
            jdict = json.loads(read)

        setpoint = jdict['Chamber Setpoint']
        dut_on = jdict["DUT On"]
        channels = jdict['Power Supply Channels']
        psu_channels = {}
        for i, ch in enumerate(channels):
            channel_name = ch["Channel Name"]
            channel_on = ch["Channel On"]
            channel_group = ch["Group"]
            channel_setpoint = ch["Voltage Setpoint"]
            channel_slew = ch["Slew Rate"]
            channel_on_delay = ch["On Delay"]
            channel_off_delay = ch["Off Delay"]
            psc = PowerSupplyChannel(channel=i, channel_name=channel_name, channel_on=channel_on, group=channel_group,
                                     voltage_setpoint=channel_setpoint, slew_rate=channel_slew,
                                     on_delay=channel_on_delay,
                                     off_delay=channel_off_delay)
            psu_channels[str(psc.channel)] = psc
        efe = CaptureEnvironmentFileEntity(chamber_setpoint=setpoint, dut_on=dut_on, power_supply_channels=psu_channels)

        return efe
    except FileNotFoundError as e:
        print("Attempted to create environment entity but failed to find the file: ", environment_file_path, e)
        return ""


def create_capture_linkpartner_entity(lp_file_path: Path) -> LPTrafficFileEntity:
    try:
        with open(lp_file_path, 'r') as file:
            read = file.read()
            jdict = json.loads(read)

        ports: t.List[Port] = []

        for i, port in enumerate(jdict):
            slot = port["Slot"]
            bdf = slot["Bus Dev Func"]
            connection = slot["Connection"]
            crc = slot["CRC"]
            device_id = slot["Device ID"]
            etrack_id = slot["Etrack ID"]
            link = slot['Link']
            mac = slot['MAC Address']
            name = slot["Name"]
            packet_size = slot["Packet Size"]
            pattern = slot["Pattern"]
            rmac_addr = slot["Remote MAC Address"]
            rev_id = slot["Revision ID"]
            rx_bps = slot["RX Bits Per Second"]
            rx_error = slot["RX Errors"]
            rx_pkt = slot["RX Packets"]
            speed = slot["Speed"]
            state = slot["State"]
            slot_num = slot['Slot']
            sub_id = slot["Subsystem ID"]
            sub_vendor_id = slot["Subsystem Vendor ID"]
            tx_bps = slot["TX Bits Per Second"]
            tx_err = slot["TX Errors"]
            tx_pkt = slot["TX Packets"]
            vendor_id = slot["Vendor ID"]
            p = Port(port=i, bdf=bdf, connection=connection, crc=crc, device_id=device_id, etrack_id=etrack_id,
                     link=link, mac_addr=mac, device_name=name, packet_size=packet_size, pattern=pattern,
                     remote_mac_addr=rmac_addr, rev_id=rev_id, rx_bps=rx_bps, rx_errors=rx_error, rx_packets=rx_pkt,
                     tx_bps=tx_bps, tx_errors=tx_err, tx_packets=tx_pkt, slot=slot_num, speed=speed, state=state,
                     subsystem_id=sub_id, subsystem_vendor_id=sub_vendor_id, vendor_id=vendor_id, target_speed=speed)
            ports.append(p)

        lptfe = LPTrafficFileEntity(ports=ports)
        return lptfe
    except FileNotFoundError as e:
        print("Attempted to create environment entity but failed to find the file: ", lp_file_path, e)
        return ""


def create_capture_dut_entity(dut_file_path: Path) -> DUTTrafficFileEntity:
    try:
        with open(dut_file_path, 'r') as file:
            read = file.read()
            jdict = json.loads(read)

        ports: t.List[Port] = []

        for i, port in enumerate(jdict):
            slot = port["Slot"]
            bdf = slot["Bus Dev Func"]
            connection = slot["Connection"]
            crc = slot["CRC"]
            device_id = slot["Device ID"]
            etrack_id = slot["Etrack ID"]
            link = slot['Link']
            mac = slot['MAC Address']
            name = slot["Name"]
            packet_size = slot["Packet Size"]
            pattern = slot["Pattern"]
            rmac_addr = slot["Remote MAC Address"]
            rev_id = slot["Revision ID"]
            rx_bps = slot["RX Bits Per Second"]
            rx_error = slot["RX Errors"]
            rx_pkt = slot["RX Packets"]
            speed = slot["Speed"]
            state = slot["State"]
            slot_num = slot["Slot"]
            sub_id = slot["Subsystem ID"]
            sub_vendor_id = slot["Subsystem Vendor ID"]
            tx_bps = slot["TX Bits Per Second"]
            tx_err = slot["TX Errors"]
            tx_pkt = slot["TX Packets"]
            vendor_id = slot["Vendor ID"]
            p = Port(port=i, bdf=bdf, connection=connection, crc=crc, device_id=device_id, etrack_id=etrack_id,
                     link=link, mac_addr=mac, device_name=name, packet_size=packet_size, pattern=pattern,
                     remote_mac_addr=rmac_addr, rev_id=rev_id, rx_bps=rx_bps, rx_errors=rx_error, rx_packets=rx_pkt,
                     tx_bps=tx_bps, tx_errors=tx_err, tx_packets=tx_pkt, slot=slot_num, speed=speed, state=state,
                     subsystem_id=sub_id, subsystem_vendor_id=sub_vendor_id, vendor_id=vendor_id, target_speed=speed)
            ports.append(p)

        dtfe = DUTTrafficFileEntity(ports=ports)
        return dtfe
    except FileNotFoundError as e:
        print("Attempted to create environment entity but failed to find the file: ", dut_file_path, e)
        return ""
