"""
module to process the data collected from the public APIs and object detection
"""
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error
import sys
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
DEGREE = 3
MOVING_AVG_WINDOW = 10  #


def get_day_phase(time):
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


def test_baseline_model(X_train, Y_train, Y_test):
    print()



def fit_models(dframe):
    """
    # method to fit ML model(s) on the provided dataframe object
    :param dframe:
    :return:
    """
    print(dframe)
    # split data (80-20) into training and testing set
    training_len = int(len(dframe) * 0.80)
    train_df = dframe.iloc[:training_len]
    test_df = dframe.iloc[training_len:].reset_index()

    X_train = (train_df[['hour_norm', 'weekend']]).values
    Y_train = (train_df[['vehicle_count']]).values
    X_test = (test_df[['hour_norm', 'weekend']]).values
    Y_test = (test_df[['vehicle_count']]).values

    # polynomial feature transformation
    poly_features = PolynomialFeatures(degree=DEGREE, interaction_only=False)
    X_train_poly = poly_features.fit_transform(X=X_train)
    X_test_poly = poly_features.transform(X=X_test)

    # Baseline model -- returns mean of the data

    # traing models here
    model = LinearRegression()  # Linear
    # model = Ridge(alpha=0.5)
    # model = SVR()
    # model = RandomForestRegressor()
    # model = GradientBoostingRegressor()

    model.fit(X=X_train_poly, y=Y_train)
    # training evaluation
    r_score_train = model.score(X=X_train_poly, y=Y_train)
    rmse_train = np.sqrt(mean_squared_error(y_true=Y_train, y_pred=model.predict(X_train_poly)))
    print("Training Evaluation: R2-Score : {}, RMSE : {}\n".format(r_score_train, rmse_train))

    # test data evaluation
    r_score_test = model.score(X=X_test_poly, y=Y_test)
    rmse_test = np.sqrt(mean_squared_error(y_true=Y_test, y_pred=model.predict(X_test_poly)))
    print("Test Case Evaluation: R2-Score : {}, RMSE : {}\n".format(r_score_test, rmse_test))


if __name__ == "__main__":
    TRAFFIC_FILE = "../dataset/traffic_cam_1705/traffic_data.txt"
    TEMPERATURE_FILE = "../dataset/air_temp_S43/air_temp_data.txt"
    RAINFALL_FILE = "../dataset/rainfall_S43/rainfall_data.txt"

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
    df = pd.merge(df, traffic_df, on="timestamp")
    # print(len(df))

    # add derived attributes to dataframe
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d-%H-%M-%S")
    # add weekend or weekday attribute
    df['day_of_week'] = df['timestamp'].dt.weekday
    df['weekend'] = df['day_of_week'].apply(lambda x: 1.0 if x > 4 else 0)  # 0 - Monday, 6- Sunday
    # add "morning/noon/evening/night" attribute
    df['time'] = df['timestamp'].dt.time
    # df['day_phase'] = df['time'].apply(get_day_phase)
    df['hour'] = df['time'].apply(lambda x: x.hour)

    # pd.DataFrame.to_csv(df, "temp.txt")
    # moving avg
    df['vehicle_count'] = df['vehicle_count'].rolling(window=MOVING_AVG_WINDOW).mean()
    df = df.dropna()
    df['vehicle_count'] = df['vehicle_count'].astype("int32")

    # apply min-max normalization
    df['rain_norm'] = (df['rainfall'] - df['rainfall'].min()) / (df['rainfall'].max() - df['rainfall'].min())
    df['temp_norm'] = (df['temperature'] - df['temperature'].min()) / (
            df['temperature'].max() - df['temperature'].min())
    # df['traffic_norm'] = (df['vehicle_count'] - df['vehicle_count'].min()) / (
    #         df['vehicle_count'].max() - df['vehicle_count'].min())
    df['dow_norm'] = (df['day_of_week'] - df['day_of_week'].min()) / (
            df['day_of_week'].max() - df['day_of_week'].min())
    df['hour_norm'] = (df['hour'] - df['hour'].min()) / (
            df['hour'].max() - df['hour'].min())

    ax1 = plt.axes()
    df.plot(kind="line", y="vehicle_count", ax=ax1)
    # df.plot(kind="line", y="temp_norm", ax=ax1)
    # df.plot(kind="line", y="rain_norm", ax=ax1)

    # print(df)
    # df.plot(kind="bar", x="day_phase", y="vehicle_count")
    # df = df.groupby('hour')
    # df['vehicle_count'].sum().plot(kind="bar")

    # fit regression models
    df_sub = df[['timestamp', 'vehicle_count', 'hour_norm', 'weekend', 'rain_norm', 'temp_norm']]
    fit_models(df_sub)

    plt.show()
