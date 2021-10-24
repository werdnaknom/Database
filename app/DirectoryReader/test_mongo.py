import pymongo
from dotenv import load_dotenv
import os
from bson.son import SON
import pprint


def count_runids_per_product(db):
    print(db["RUNID"].find(filter={"project": "Island Rapids"}).count())
    print(db["RUNID"].count_documents(filter={"project": "Island Rapids"}))


def find_runids_with_status_aborted(db):
    print([x for x in db["RUNID"].find({"status.status": "Aborted"}, {"status.status": 1})])


def find_distinct_status_conditions(db):
    print([x for x in db["RUNID"].distinct("status.status")])


def count_runids_by_status(db):
    pipeline = [
        {"$unwind": "$status.status"},
        {"$group": {"_id": "$status.status", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    result = db["RUNID"].aggregate(pipeline)
    pprint.pprint(list(result))


def count_runids_by_product_and_status(db):
    pipeline = [
        {"$unwind": "$project"},
        {"$match": {"project": "$project"}},
        # {"$group": {"_id": "$project"}},
        # {"$unwind": "$status.status"},
        # {"$group": {"_id": "$status.status", "count": {"$sum": 1}}},
        # {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    result = db["RUNID"].aggregate(pipeline)
    pprint.pprint(list(result))


def lookup_runids_from_project(db):
    pipeline = [{"$lookup": {"from": "RUNID",
                             "localField": "name",
                             "foreignField": "project",
                             "as": "related_runids"}},
                {"$group":
                     {"_id": "$related_runids.runid",
                      "status": {"$push": "$related_runids.status.status"}},
                 }
                ]
    result = db["PROJECT"].aggregate(pipeline)
    pprint.pprint(list(result))


def lookup_complete_runids_from_project(db):
    pipeline = [{"$lookup": {"from": "RUNID",
                             "localField": "name",
                             "foreignField": "project",
                             "as": "related_runids"}},
                {"$addFields": {"Status": {
                    "$arrayElemAt": [
                        {"$filter": {
                            "input": "$related_runids",
                            "as": "runid",
                            "cond": {
                                "$eq": ["$$runid.status.status", "Complete"]
                            }
                        }}, 0
                    ]
                }}

                }
                ]
    result = db["PROJECT"].aggregate(pipeline)
    for r in result:
        print(r["Status"]["project"], r["Status"]["status"]["status"])
    pprint.pprint(list(result))


def group_runids_by_project(db):
    pipeline = [
        {"$group": {
            "_id": "$project",
            "runid_count": {"$sum": 1},
            "runid_status": {"$push": "$status.status"}
        }}
    ]
    result = db["RUNID"].aggregate(pipeline)
    pprint.pprint(list(result))


def count_captures_by_runid(db):
    pipeline = [
        {"$group": {
            "_id": "$runid",
            "capture_count": {"$sum": 1},
        }}
    ]
    result = db["DATACAPTURE"].aggregate(pipeline)
    pprint.pprint(list(result))


def find_probes_from_runid(db, runid):
    pipeline = [
        {"$match": {"runid": runid}},
        {"$project": {"system_info.probes": 1}},
    ]
    result = db["RUNID"].aggregate(pipeline)
    pprint.pprint(list(result))


if __name__ == "__main__":
    load_dotenv()
    mongo_uri = os.environ.get("MONGO_URI")
    print(mongo_uri)
    client = pymongo.MongoClient(mongo_uri)
    db = client["ATS2"]
    col = db["PBA"]

    '''
    count_runids_per_product(db)
    find_runids_with_status_aborted(db)
    find_distinct_status_conditions(db)
    count_runids_by_status(db)
    #count_runids_by_product_and_status(db)
    lookup_runids_from_project(db)
    lookup_complete_runids_from_project(db)
    group_runids_by_project(db)
    count_captures_by_runid(db)
    '''
    find_probes_from_runid(db, runid=1014)
