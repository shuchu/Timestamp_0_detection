import numpy as np
import pandas as pd
import matplotlib.dates as md
import matplotlib.pyplot as plt
%matplotlib inline

def moving_average(ts, val, n):
    ma_arr = np.array([])
    ma=0
    for i in range(0,n-1):
        ma_arr = np.append(ma_arr, 0)
    for i in range(n,len(ts)+1):
        ma_arr = np.append(ma_arr, (sum(val[i-n:i])/n))
    return ma_arr

def percentile_based_modification(val):
    lower_five_percent = np.percentile(val,5)
    top_five_percent = np.percentile(val,95)
    for i in range(0,len(val)):
        if val[i] <= lower_five_percent:
            val[i] = lower_five_percent
        elif val[i] >= top_five_percent:
            val[i] = top_five_percent
    return val

def simple_transformed_values(val1, val2):
    for i in range(0, len(val1)):
        if (val1[i] > 0 and val2[i] > 0):
            val1[i] = ((val1[i])/(val2[i]))
        elif (val1[i] == 0 and val2[i] == 0):
            val1[i] = (1.0)
        elif (val1[i] > 0 and val2[i] == 0):
            val1[i] = (0.0)
    return val1

def extract_ts_fea(ts_segment):
    """
    Extract feature vector from given time series segment.

    Example:
    ts_segment = np.array([1.0, 2.0, 3.0, 100.0, 12.21.,...,]
    fea = [0.1, 0.3, 0.4, 0.2, ..., 0.9]

    fea = extract_ts_fea(ts_segment)

    :param ts_segment: a numpy array,
    :return: a numpy array which is the extracted feature vector
    """
    pass


def fea_filter(fea):
    """
    Filter the input feature vector, to remove several frequence.

    Example:
    frequency = [10, 20, 30, 40, 50]
    fea = [0.1, 0.3, 0.4, 0.2, 0.9]
    filtered_fea = [0.1, 0.3, 0.4, 0.0, 0.0]

    :param fea: an numpy array
    :return: an numpy array
    """
    pass


def window_based_cp_detection(data, sub_window_size=250, threshold=0.2):
    """
    Detect the change points in data. Assume the input data is a time series without
    any missing values.

    :param data: numpy array, one single time series
    :return: list object with all change points
    """
    sub_window_size = sub_window_size
    threshold = threshold

    res = []
    for i in range(sub_window_size : (len(data) - sub_window_size) : 5):

        left_sub_window = np.array(data[i-sub_window_size:i])
        right_sub_window = np.array(data[i+1:i+sub_window_size])

        left_fea = extract_ts_fea(left_sub_window)
        right_fea = extract_ts_fea(right_sub_window)

        res.append([left_fea, right_fea])

    return res

if __name__ == '__main__':
    df = pd.read_csv('ad49000c2947aef7_july.csv')
    df['val_1'].fillna(0, inplace=True)
    df['val_2'].fillna(0, inplace=True)
    ts = np.array(df[['Timestamp']])
    val1 = percentile_based_modification(np.array(df[['val_1']]))
    val2 = percentile_based_modification(np.array(df[['val_2']]))
    val1 = np.flip(val1)
    val2 = np.flip(val2)
    ans = pd.DataFrame(np.concatenate((ts, val1, val2), axis=1))
    ans.columns = ['Timestamp','Value 1','Value 2']
    ans.reset_index(inplace=True)
    ans['Timestamp'] = pd.to_datetime(ans['Timestamp'], unit='ms')


    ans['Moving average (5) for value 1'] = moving_average(ts, val1, 5)
    ans['Moving average (5) for value 2'] = moving_average(ts, val2, 5)


    ans['Moving average (30) for value 1'] = moving_average(ts, val1, 30)
    ans['Moving average (30) for value 2'] = moving_average(ts, val2, 30)

    ans['Moving average (60) for value 1'] = moving_average(ts, val1, 60)
    ans['Moving average (60) for value 2'] = moving_average(ts, val2, 60)

    ans['Value 1 / Value 2 for moving average (5)'] = percentile_based_modification(simple_transformed_values(np.array(
        ans['Moving average (5) for value 1']), np.array(ans['Moving average (5) for value 2'])))

    ans['Value 1 / Value 2 for moving average (30)'] = percentile_based_modification(simple_transformed_values(np.array(
        ans['Moving average (30) for value 1']), np.array(ans['Moving average (30) for value 2'])))

    ans['Value 1 / Value 2 for moving average (60)'] = percentile_based_modification(simple_transformed_values(np.array(
        ans['Moving average (60) for value 1']), np.array(ans['Moving average (60) for value 2'])))
    
