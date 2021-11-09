from PIL import Image
from pymongo import MongoClient
import io
from pathlib import Path

import matplotlib.pyplot as plt
from Entities.WaveformFunctions.waveform_analysis import WaveformAnalysis

if __name__ == "__main__":
    ''' DATABASE '''
    client = MongoClient("mongodb://192.168.1.226:27017")
    db = client['ATS2']
    images = db['RUNID_IMAGES']
    ''' CREATE IMAGE and INSERT '''
    '''
    wfm_path = Path(r"F:\ATS DATABASE\Island Rapids\K87758-002\00\894DA0\987\Tests\Aux To Main\1\CH2.bin")

    wfm_analysis = WaveformAnalysis()

    wf_y = wfm_analysis.read_binary_waveform(wfm_path=wfm_path, compressed=False)

    downsample = wfm_analysis.min_max_downsample_1d(wf_y, 2000)


    fig, ax = plt.subplots()
    ax.plot(downsample)
    ax.set_title("Simple Plot")

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')

    image_dict = {
        "data": img_buf.getvalue()
    }
    image_id = images.insert_one(image_dict).inserted_id
    '''

    ''' READ IMAGE '''
    image = images.find_one()
    pil_image = Image.open(io.BytesIO(image['data']))
    pil_image.show()
