import os

# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    DEBUG = False

    DATADIRECTORY = r'//npo/coos/LNO_Validation/Validation_Data/_data/ATS 2.0'
    KULIMDATADIRECTORY = r'//npo/coos/LNO_Validation/Kulim/ATS 2.0 Data'
    PICKLEDIRECTORY = r'//npo/coos/LNO_Validation/Validation_Data/_data/ATS 2.0_pickle'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    REPOSITORYFILTER = 'dut'
    PRODUCTFILTERS = ["dut"]
    ASSEMBLYFILTERS = ['pba', 'dash', 'base']
    REWORKFILTERS = ['rework']
    SUBMISSIONFILTERS = ['serial_number']
    RUNIDFILTERS = ['runid', 'status', 'technician', 'test_station']
    TESTCATEGORYFILTERS = ['test_category']
    CAPTUREFILTERS = ['temperature', 'temperature_setpoint', 'nominal_power', 'voltage', 'slew', 'waveform', 'temp',
                      'capture']
    WAVEFORMFILTERS = ['testpoint', "scope_channel"]

    REPOSITORYOPERATORS = ['eq', 'ne']
    PRODUCTOPERATORS = ['eq', 'ne']
    ASSEMBLYOPERATORS = ['eq', 'ne']
    REWORKOPERATORS = ['eq', 'lt', 'gt', 'ne']
    SUBMISSIONOPERATORS = ['eq', 'lt', 'gt', 'ne']
    RUNIDOPERATORS = ['eq', 'lt', 'gt', 'ne']
    TESTCATEGORYOPERATORS = ['eq', 'ne']
    SUBCATEGORYOPERATORS = ['eq', 'ne']
    CAPTUREOPERATORS = ['eq', 'lt', 'gt', 'ne']
    WAVEFORMOPERATORS = ['eq', 'lt', 'gt', 'ne']
    # LOGGING CONFIG
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    # BABEL Config
    LANGUAGES = {
        "en": "English",
    }
    MONGO_URI = os.environ.get("MONGO_URI")

    basedir = os.path.abspath(os.path.dirname(__file__))


class DeploymentConfig(Config):
    OR_DIRECTORY_HEAD = os.environ.get("OR_ATS_DIRECTORY") or r'F:\ATS DATABASE'
    KM_DIRECTORY_HEAD = os.environ.get("KM_ATS_DIRECTORY") or r'F:\ATS DATABASE'


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True

    # MONGODB SETUP
    MONGO_URI = "mongodb://localhost:27017"  # Must setup in standalone docker
    redis_port = 6379
    REDIS_URL = 'redis://localhost'
    OR_DIRECTORY_HEAD = r'F:\ATS DATABASE'
    KM_DIRECTORY_HEAD = r'F:\ATS DATABASE'
