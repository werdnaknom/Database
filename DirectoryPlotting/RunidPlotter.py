from Entities.Entities import RunidEntity


def plot_runid_aux2main(repo, runid: RunidEntity):
    TESTNAME = "Aux To Main"
    # If runid doesn't exist, create a new one
    if repo.does_runid_image_exist(runid=runid.runid):
        runid_wfms = repo.get_runid_waveforms(runid=runid.runid,
                                              test_category=TESTNAME)
        print(len(runid_wfms), runid_wfms)

    exit()
