import typing as t
import os

import pymongo
from PIL import Image
import io
import matplotlib.pyplot as plt

from Entities.Entities import *


class Repo():
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")
        print(mongo_uri)
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client['ATS2']
        print(self.db)

    def _insert_entity(self, entity):
        # TODO:: Update to find the actual _id instead of just count found.
        # TODO:: Then return the found _ID
        col = self.db[entity.get_type()]
        found = col.count_documents({"_id": entity.get_id()})
        # found = list(col.find({"_id": entity.get_id()}, {"_id":1}))
        # if found:
        #   return found
        if not found:
            # print("NOT FOUND, INSERTING", entity.to_dict())
            r = col.insert_one(document=entity.to_mongo())
            print("INSERTED {} at {}".format(entity.descriptor, r.inserted_id))
            # return r.inserted_ids

    def insert_error(self, error, traceback):
        col = self.db["ERROR"]
        #found = col.count_documents({"_id"})
        found = False
        if not found:
            r = col.insert_one(document={

            })
            print("INSERTED {} at {}".format("ERROR", r.inserted_id))

    def insert_project(self, project: ProjectEntity):
        return self._insert_entity(entity=project)


    def insert_pba(self, pba: PBAEntity):
        return self._insert_entity(entity=pba)

    def insert_rework(self, rework: ReworkEntity):
        return self._insert_entity(entity=rework)

    def insert_serialnumber(self, serial: SubmissionEntity):
        return self._insert_entity(entity=serial)

    def insert_runid(self, runid: RunidEntity):
        return self._insert_entity(entity=runid)

    def insert_automationtest(self, test: AutomationTestEntity):
        return self._insert_entity(entity=test)

    def insert_capture(self, capture):
        return self._insert_entity(entity=capture)

    def insert_waveform(self, waveform):
        # ds_x = waveform.downsample[0].tolist()
        # ds_y = waveform.downsample[1].tolist()
        # waveform.downsample = [ds_x, ds_y]
        return self._insert_entity(entity=waveform)

    def get_runid_by_id(self, id):
        cursor = self.db[RunidEntity.get_type()].find_one({"_id": id})
        return cursor

    def _insert_image_from_path(self, path: str):
        im = Image.open(path)
        image_bytes = io.BytesIO()
        im.save(image_bytes, format('PNG'))

        image_entity = {
            'data': image_bytes.getvalue()
        }
        image_id = self._insert_entity(image_entity)
        return image_id

    def get_unique_runids(self) -> t.List[str]:
        return self.db[RunidEntity.get_type()].distinct("_id")

    def _read_image_from_db(self, id):
        image = self.db['images'].find_one({})
        pil_img = Image.open(io.BytesIO(image['data']))
        plt.imshow(pil_img)
        plt.show()

    def insert_waveform_image(self, wfm_image):

        pass

    def insert_runid_image(self, runid_image):
        pass

    def get_runid_waveforms(self, runid: int, test_category: str, testpoint_name: str = None) -> t.List[dict]:
        search_filter = {"runid": runid,
                         "test_category": test_category}
        if testpoint_name:
            search_filter["testpoint"] = testpoint_name
        cursor = self.db[WaveformEntity.get_type()].find(search_filter)
        return list(cursor)

    def does_runid_image_exist(self, runid) -> bool:
        return False

    def insert_rework_image(self, rwk_image):
        pass

    def insert_serial_image(self, serial_image):
        pass

    def insert_pba_image(self, pba_image):
        pass

    def insert_project_image(self, project_image):
        pass

    def check_waveform(self, runid, capture, testpoint, scope_channel, test_category):
        id = WaveformEntity.format_id(testpoint=testpoint, runid=runid, capture=capture, scope_channel=scope_channel,
                                      test_category=test_category)
        result = self.db[WaveformEntity.get_type()].count_documents({"_id": id})
        if result > 0:
            return True
        else:
            return False

    def waveform_characteristics(self, runid: int, test_category: str, testpoint_name: str):
        pipeline = [
            {"$match": {"runid": runid,
                        "test_category": test_category,
                        "testpoint": testpoint_name}},
            {"$group": {"_id": "$testpoint",
                        "steady_state_min": {"$min": "$steady_state_min"},
                        "steady_state_mean": {"$avg": "$steady_state_mean"},
                        "steady_state_max": {"$max": "$steady_state_max"},
                        "steady_state_pk2pk": {"$max": "$steady_state_pk2pk"},
                        "max_value": {"$max": "$max"},
                        "min_value": {"$min": "$min"},
                        }}
        ]

        cursor = self.db[WaveformEntity.get_type()].aggregate(pipeline=pipeline)
        return cursor

    def get_runid_test_categories(self, runid: int) -> t.List[str]:
        cursor = self.db[WaveformCaptureEntity.get_type()].distinct("test_category", {"runid": runid})
        return cursor

    def count_waveforms_by_runid(self, runid: int) -> int:
        cursor = self.db[WaveformEntity.get_type()].count_documents({"runid": runid})
        return cursor

