import requests
import json
from datetime import datetime as datetime
from datetime import timedelta
import urllib.request as req

if __name__ == "__main__":
    INTERVAL = 6  # minutes
    BASE_URL = "https://api.data.gov.sg/v1/environment/air-temperature"
    PARAMS = {
        "date_time": ""
    }
    STATION_ID = "S43"  # corresponding to the given latitude and longitude
    OUT_FILENAME = "../dataset/air_temp_{}/air_temp_data.txt".format(STATION_ID)
    epoch = "2021-07-01-07:00:00"

    # Adding information about user agent
    opener = req.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    req.install_opener(opener)

    epoch = datetime.strptime(epoch, "%Y-%m-%d-%H:%M:%S")
    delta = timedelta(minutes=INTERVAL)
    new_dt = epoch

    today = datetime.now()

    with open(OUT_FILENAME, 'w') as outfile:
        outfile.write("timestamp,sensor_id,temperature\n")
        while new_dt <= today:
            # print(new_dt)
            new_dt_fmt = datetime.strftime(new_dt, "%Y-%m-%dT%H:%M:%S")
            print(new_dt_fmt)
            PARAMS["date_time"] = new_dt_fmt

            response = requests.get(BASE_URL, params=PARAMS)
            res_txt = response.text
            res_json = json.loads(res_txt)

            readings = res_json["items"][0]["readings"]
            for reading in readings:
                if reading["station_id"] in ["S43"]:
                    outfile.write("{},{},{}\n".format(new_dt_fmt.replace(":", "-").replace("T", "-"), STATION_ID,
                                                      reading["value"]))
                    outfile.flush()
            new_dt = new_dt + delta
