import json
from pathlib import Path
import pandas as pd

from flask import jsonify, Response, request, send_file

from app.server_main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return "YAY!"

@bp.route('/list', methods=['GET'])
def list():
    json_request = request.get_json() or {}
    req = ListRequestObject.from_dict(json_request)

    pr = PickleRepository()
    uc_pr = ListUseCase(repo=pr)
    result_pr = uc_pr.execute(request_object=req)
    if result_pr.value:
        print(result_pr.value)
        result = result_pr
    else:
        print("DR!:", result_pr.value)
        dr = DirectoryRepository()
        uc_dr = ListUseCase(repo=dr)
        result_dr = uc_dr.execute(request_object=req)
        result = result_dr
        print(result_dr.value)
    return Response(json.dumps(result.value, cls=ProductEncoder), mimetype='application/json',
                    status=STATUS_CODES[result.type])
