"""
module to featch taffic data for 5 yeras (twice a day)
"""
import requests
import json
from datetime import datetime as datetime
from datetime import timedelta
import urllib.request as req

if __name__ == "__main__":
    INTERVALS = [600, 840]  # minutes
    BASE_URL = "https://api.data.gov.sg/v1/transport/traffic-images"
    OUT_DIR = "../dataset"
    PARAMS = {
        "date_time": ""
    }
    CAMERA_ID = "1705"  # corresponding to a specific latitude and longitude
    epoch = "2021-01-06-08:00:00"

    # Adding information about user agent
    opener = req.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)

    epoch = datetime.strptime(epoch, "%Y-%m-%d-%H:%M:%S")
    index = 0
    new_dt = epoch

    today = datetime.now()
    while new_dt <= today:
        # print(new_dt)
        new_dt_fmt = datetime.strftime(new_dt, "%Y-%m-%dT%H:%M:%S")
        PARAMS["date_time"] = new_dt_fmt

        response = requests.get(BASE_URL, params=PARAMS)
        res_txt = response.text
        res_json = json.loads(res_txt)

        cameras = res_json["items"][0]["cameras"]
        for cam in cameras:
            if cam["camera_id"] in [CAMERA_ID]:
                # cam_dump = json.dumps(cam, indent=2)
                # print(cam_dump)
                filename = "{}/cam_{}_5yrs/{}.jpg".format(OUT_DIR, cam["camera_id"],
                                                     new_dt_fmt.replace(":", "-").replace("T", "-"))
                print(filename)
                req.urlretrieve(cam['image'], filename)
                # break
        delta = timedelta(minutes=INTERVALS[index])
        index = (index + 1) % 2
        new_dt = new_dt + delta
