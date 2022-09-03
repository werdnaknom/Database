from app.api_upload import bp


# from Entities.Entities.entities import Entities


@bp.route("/add_project")
def add_project():
    pass
    # e = Entities()
    # return e.__repr__()


@bp.route("/add_pba")
def add_pba():
    return "<h1>pba</h1>"


@bp.route("/add_rework")
def add_rework():
    return "<h1>rework</h1>"


@bp.route("/add_serialnumber")
def add_serialnumber():
    return "<h1>serialnumber</h1>"


@bp.route("/add_runid")
def add_runid():
    return "<h1>runid</h1>"


@bp.route("/add_testcategory")
def add_testcategory():
    return "<h1>TestCategory</h1>"


@bp.route("/add_capture")
def add_capture():
    return "<h1>Capture</h1>"


@bp.route("/add_waveform")
def add_waveform():
    return "<h1>Waveform</h1>"
