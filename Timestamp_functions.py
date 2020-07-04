import numpy as np
import pandas as pd
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

def first_0_position_array(val,ts):
    pos=np.array([])
    for i in range(0,len(val)):
        if sum(val[i:i+4])==0:
            pos = np.append(pos,i)
    starting_position_of_0 = remove_consecutive(pos)
    ts_begin = np.array(ts[list(map(int, starting_position_of_0))])
    return ts_begin, starting_position_of_0
    
def last_0_position_array(val,ts):
    pos_last=np.array([])
    for i in range(0,len(val)):
        if sum(val[i:i+4])==0:
            first1after0s = np.where(val[i:]!=0)[0][0]
            positionoflast0 = first1after0s + i
            pos_last = np.append(pos_last, positionoflast0)
        else:
            positionoflast0 = 0
    final_position_of_0 = np.unique(np.array(pos_last))
    ending_position_of_0 = remove_consecutive(final_position_of_0)
    ts_end = np.array(ts[list(map(int, ending_position_of_0))])
    return ts_end, ending_position_of_0  

ts_begin, starting_position_of_0 = first_0_position_array(np.array(df[['val_2']]), np.array(df[['timestamp']]))
ts_end, ending_position_of_0 = last_0_position_array(np.array(df[['val_2']]), np.array(df[['timestamp']]))
ts_dif = np.array([list(map(int, np.array([np.array(ending_position_of_0) - np.array(starting_position_of_0)]).T))]).T
ans = np.concatenate((ts_begin, ts_end, ts_dif), axis=1)