from dotenv import load_dotenv

import matplotlib.pyplot as plt

from DirectoryReader.repo import Repo
from Entities.Entities import RunidEntity, WaveformEntity

if __name__ == "__main__":
    TEST_CATEGORY = "Aux To Main"
    load_dotenv()
    repo = Repo()

    print("Starting Plotting of Images")
    runid_ids = repo.get_unique_runids()
    for runid_id in runid_ids:
        runid_entity = RunidEntity.from_mongo(adict=repo.get_runid_by_id(id=runid_id))
        # print(runid_entity)
        # plot_runid_aux2main()
        runid_wfm_count = repo.count_waveforms_by_runid(runid=runid_entity.runid)
        if runid_wfm_count == 0:
            print(runid_entity.runid, repo.get_runid_test_categories(runid=runid_entity.runid))
            continue
        for channel_index, testpoint_name in runid_entity.get_testpoint_dict().items():
            channel_index = int(channel_index)
            scope_channel = channel_index + 1
            probe_info = runid_entity.get_probe(probe_channel=scope_channel)
            print(probe_info)
            if testpoint_name == "":
                continue
            testpoint_waveforms = []
            wfm_list = repo.get_runid_waveforms(runid=runid_entity.runid,
                                                test_category=TEST_CATEGORY,
                                                testpoint_name=testpoint_name)
            chars = repo.waveform_characteristics(runid=runid_entity.runid,
                                                  test_category=TEST_CATEGORY,
                                                  testpoint_name=testpoint_name)
            result = list(chars)[0]

            fig, ax = plt.subplots()
            fig.suptitle(runid_entity.get_id())
            ax.set_title(testpoint_name + "OK")
            for wfm_dict in wfm_list:
                wfm = WaveformEntity.from_mongo(wfm_dict)
                testpoint_waveforms.append(wfm)
                ax.plot(wfm.x_axis_in_milliseconds(), wfm.y_axis())

            ax.axhline(y=result["steady_state_min"])
            ax.axhline(y=result["steady_state_max"])
            ax.axhline(y=result["steady_state_mean"])
            ax.set_xlabel("Time (ms)")
            if probe_info["units"] == "A":
                ax.set_ylabel("Ampere (A)")
            else:
                ax.set_ylabel("Voltage (V)")

            print(result)
            ymax = result["max_value"] * 1.1
            ymin = min(0, result["min_value"] * 1.1)  # multiply by 1.1 because it's a negative number
            print(ymin, ymax)
            ax.set_ylim(ymin, ymax)

            plt.show()
