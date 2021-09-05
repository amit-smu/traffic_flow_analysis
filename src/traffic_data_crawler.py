import requests
import json
from datetime import datetime as datetime
from datetime import timedelta
import urllib.request as req

if __name__ == "__main__":
    INTERVAL = 6  # minutes
    BASE_URL = "https://api.data.gov.sg/v1/transport/traffic-images"
    PARAMS = {
        "date_time": ""
    }
    CAMERA_ID = "1006"  # corresponding to the given latitude and longitude
    epoch = "2021-08-06-23:12:00"

    # Adding information about user agent
    opener = req.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)

    epoch = datetime.strptime(epoch, "%Y-%m-%d-%H:%M:%S")
    delta = timedelta(minutes=INTERVAL)
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
            if cam["camera_id"] in ["1006", "1705"]:
                # cam_dump = json.dumps(cam, indent=2)
                # print(cam_dump)
                filename = "../dataset/cam_{}/{}.jpg".format(cam["camera_id"],
                                                             new_dt_fmt.replace(":", "-").replace("T", "-"))
                print(filename)
                req.urlretrieve(cam['image'], filename)
                # break

        new_dt = new_dt + delta