import numpy as np
import pandas as pd
def remove_consecutive(pos):
    remove_pos = []
    for i in range(0,len(pos)-1):
        if pos[i+1] - pos[i] == 1:
            remove_pos.append(pos[i+1])

    final_pos = []
    for i in pos:
        if i not in remove_pos:
            final_pos.append(i)
    return final_pos

def first_zero_position_array(val,ts):
    pos = np.array([])
    for i in range(0,len(val)):
        if sum(val[i:i+4]) == 0:
            pos = np.append(pos, i)
    starting_position_of_zero = remove_consecutive(pos)
    ts_begin = np.array(ts[list(map(int, starting_position_of_zero))])
    return ts_begin, starting_position_of_zero
    
def last_zero_position_array(val,ts):
    pos_last = np.array([])
    for i in range(0,len(val)):
        if sum(val[i:i+4]) == 0:
            first_one_after_zeros = np.where(val[i:]!=0)[0][0]
            position_of_last_zero = first_one_after_zeros + i
            pos_last = np.append(pos_last, position_of_last_zero)
        else:
            position_of_last_zero = 0
    final_position_of_zero = np.unique(np.array(pos_last))
    ending_position_of_zero = remove_consecutive(final_position_of_zero)
    ts_end = np.array(ts[list(map(int, ending_position_of_zero))])
    return ts_end, ending_position_of_zero  

if __name__ == '__main__':
    df = pd.read_csv('sensor_data_06302020.csv')
    df['val_2'].fillna(0, inplace=True)
    ts_begin, starting_position_of_zero = first_zero_position_array(np.array(df[['val_2']]), np.array(df[['timestamp']]))
    ts_end, ending_position_of_zero = last_zero_position_array(np.array(df[['val_2']]), np.array(df[['timestamp']]))
    ts_dif = np.array([list(map(int, np.array([np.array(ending_position_of_zero) - np.array(starting_position_of_zero)]).T))]).T
    ans = np.concatenate((ts_begin, ts_end, ts_dif), axis=1)
    print(ans)