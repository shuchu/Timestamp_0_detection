import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
sns.set_style('darkgrid')

def moving_average(ts, val, n):
    ma_arr = np.array([])
    ma=0
    for i in range(0,n-1):
        ma_arr = np.append(ma_arr, 0)
    for i in range(n,len(ts)+1):
        ma_arr = np.append(ma_arr, (sum(val[i-n:i])/n))
    return ma_arr

if __name__ == '__main__':
    df = pd.read_csv('sensor_data_06302020.csv')
    df['val_1'].fillna(0, inplace=True)
    ts = np.array(df[['timestamp']])
    val = np.array(df[['val_1']])
    ans = pd.DataFrame(np.concatenate((ts, val), axis=1))
    ans.columns = ['Timestamp','Value 1']
    ans.reset_index(inplace=True)
    ans['Moving average (5)'] = moving_average(ts, val, 5)
    ans['Moving average (6)'] = moving_average(ts, val, 6)
    ans['Moving average (8)'] = moving_average(ts, val, 8)
    ans['Moving average (10)'] = moving_average(ts, val, 10)
    
    ans.to_csv('Moving Average Timestamp.csv')
    
    #Data Visualization
    plt.figure(figsize=(20,10))
    sns.lineplot(x='index', y='Value 1', data=ans)
    plt.ylim(0,50000)
    plt.show()
    plt.figure(figsize=(20,10))
    sns.lineplot(x='index', y='Moving average (5)', data=ans)
    plt.ylim(0,50000)
    plt.show()
    plt.figure(figsize=(20,10))
    sns.lineplot(x='index', y='Moving average (6)', data=ans)
    plt.ylim(0,50000)
    plt.show()
    plt.figure(figsize=(20,10))
    sns.lineplot(x='index', y='Moving average (8)', data=ans)
    plt.ylim(0,50000)
    plt.show()
    plt.figure(figsize=(20,10))
    sns.lineplot(x='index', y='Moving average (10)', data=ans)
    plt.ylim(0,50000)
    plt.show()
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(ans['index'], ans['Value 1'])
    ax.plot(ans['index'], ans['Moving average (5)'])
    ax.plot(ans['index'], ans['Moving average (6)'])
    ax.plot(ans['index'], ans['Moving average (8)'])
    ax.plot(ans['index'], ans['Moving average (10)'])
    ax.set_ylim([0, 50000])

    plt.show()
    fig, ax = plt.subplots(2,3,figsize=(20, 10))

    ax[0,0].plot(ans['index'], ans['Value 1'])
    ax[0,0].set_ylim([0, 50000])
    ax[0,0].set_xlabel('Index')
    ax[0,0].set_ylabel('Value 1')


    ax[0,1].plot(ans['index'], ans['Moving average (5)'])
    ax[0,1].set_ylim([0, 50000])
    ax[0,1].set_xlabel('Index')
    ax[0,1].set_ylabel('Moving average (5)')


    ax[0,2].plot(ans['index'], ans['Moving average (6)'])
    ax[0,2].set_ylim([0, 50000])
    ax[0,2].set_xlabel('Index')
    ax[0,2].set_ylabel('Moving average (6)')


    ax[1,0].plot(ans['index'], ans['Moving average (8)'])
    ax[1,0].set_ylim([0, 50000])
    ax[1,0].set_xlabel('Index')
    ax[1,0].set_ylabel('Moving average (8)')


    ax[1,1].plot(ans['index'], ans['Moving average (10)'])
    ax[1,1].set_ylim([0, 50000])
    ax[1,1].set_xlabel('Index')
    ax[1,1].set_ylabel('Moving average (10)')

    fig.delaxes(ax[1][2])

    plt.show()