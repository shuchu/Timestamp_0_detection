import time, calendar, decimal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
sns.set_style('whitegrid')

df = pd.read_csv('sensor_data_06302020.csv')

df['val_2'].fillna(0, inplace=True)

def remove_consecutive(pos):
    remove_pos=[]
    for i in range(0,len(pos)-1):
        if pos[i+1]-pos[i]==1:
            remove_pos.append(pos[i+1])

    final_pos = []
    for i in pos:
        if i not in remove_pos:
            final_pos.append(i)
    return final_pos

x = np.array(df[['val_2']])
ts = np.array(df[['timestamp']])
pos_last=np.array([])
for i in range(0,len(x)):
    if sum(x[i:i+4])==0:
                
        first1after0s = np.where(x[i:]!=0)[0][0]

        positionoflast0 = first1after0s + i
        
        pos_last = np.append(pos_last, positionoflast0)
    else:
        positionoflast0 = 0
final_position_of_0 = np.unique(np.array(pos_last))

starting_position_of_0 = remove_consecutive(pos)
ending_position_of_0 = remove_consecutive(final_position_of_0)

ts_begin = np.array(ts[list(map(int, starting_position_of_0))])
ts_end = np.array(ts[list(map(int, ending_position_of_0))])
ts_dif = np.array([np.array(ending_position_of_0) - np.array(starting_position_of_0)]).T

ts_begin = np.array([list(map(int, ts_begin))]).T
ts_end = np.array([list(map(int, ts_end))]).T
ts_dif = np.array([list(map(int, ts_dif))]).T
ans = np.concatenate((ts_begin, ts_end, ts_dif), axis=1)

ans_df = pd.DataFrame(ans)
ans_df.columns = [['Start time','End time','Number of zeros']]
ans_df['Number of zeros'] = ans_df[['Number of zeros']].astype(int)
ans_df.to_csv('Timestamp assignment.csv')