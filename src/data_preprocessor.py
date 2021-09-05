"""
module to preprocess the data collected from the public APIs and object detection
"""
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def decide_day_phase(time):
    """
    decides the phase of day (morning/noon/evening/night)
    :param time:
    :return:
    """
    DAY_PHASES = {
        0: "morning",  # 6am - 11 am
        1: "noon",  # 11am - 4 pm
        2: "evening",  # 4pm - 8 pm
        3: "night"  # 8 pm - 6 am
    }
    hour = time.hour
    if hour >= 6 and hour <= 10:  # till 10:59am
        return 0
    elif hour >= 11 and hour <= 15:
        return 1
    elif hour >= 16 and hour <= 19:
        return 2
    else:
        return 3


if __name__ == "__main__":
    TRAFFIC_FILE = "../dataset/traffic_cam_1705/traffic_data.txt"
    TEMPERATURE_FILE = "../dataset/air_temp_S43/air_temp_data.txt"
    RAINFALL_FILE = "../dataset/rainfall_S43/rainfall_data.txt"

    # processed after crawling
    processed_df = pd.DataFrame(data=None,
                                columns=["timestamp", "cam_id", "temp_device_id", "rain_device_id", "total_vehicles",
                                         "temperature", "rainfall", "day_of_week", "day_phase"])

    # read all the crawled data
    traffic_df = pd.read_csv(TRAFFIC_FILE)
    temperature_df = pd.read_csv(TEMPERATURE_FILE)
    rainfall_df = pd.read_csv(RAINFALL_FILE)

    # check data subsets
    # traffic_sub = traffic_df.head(1000)
    # temp_sub = temperature_df.head(1000)
    # rain_sub = rainfall_df.head(1000)

    # print("{}\n".format(traffic_sub))
    # print("{}\n".format(temp_sub))
    # print("{}\n".format(rain_sub))

    # df = pd.concat([temp_sub, rain_sub], axis=0, ignore_index=True)
    # print("{}\n".format(df))

    df = pd.merge(temperature_df, rainfall_df, on="timestamp")
    # print("{}\n".format(df))

    df = pd.merge(df, traffic_df, on="timestamp")
    # print("{}\n".format(df))
    # print(len(df))

    # add derived attributes to dataframe
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d-%H-%M-%S")
    # add weekend or weekday attribute
    df['day_of_week'] = df['timestamp'].dt.weekday
    df['weekend'] = df['day_of_week'].apply(lambda x: 1 if x > 4 else 0)  # 0 - Monday, 6- Sunday
    # add "morning/noon/evening/night" attribute
    df['time'] = df['timestamp'].dt.time
    # df['day_phase'] = df['time'].apply(decide_day_phase)
    df['hour'] = df['time'].apply(lambda x: x.hour)
    print(df)
    # pd.DataFrame.to_csv(df, "temp.txt")

    # plot columns
    # df['vehicle_count'].plot()
    # df.plot(kind="bar", x="day_phase", y="vehicle_count")
    df = df.groupby('hour')
    df['vehicle_count'].sum().plot(kind="bar")
    plt.show()
