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

def window(val):
    sub_window_size = 250
    threshold = 0.2
    res = []
    for i in range(sub_window_size, len(val1) - sub_window_size):
        left_sub_window = np.array(val[i-sub_window_size:i])
        right_sub_window = np.array(val[i+1:i+sub_window_size])
        left_sub_window_median = np.median(left_sub_window)
        right_sub_window_median = np.median(right_sub_window)
        err = np.fabs(left_sub_window_median - right_sub_window_median)

        #if err > (threshold * left_sub_window_median):
        res.append(err)
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
    