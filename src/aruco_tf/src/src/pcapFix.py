import pandas as pd
import ast

def string_to_list(row):
    try:
        return ast.literal_eval(row.replace('\n ', ' ').replace('  ', ' ').replace(' ', ',').replace('[,','['))
    except:
        import pdb
        pdb.set_trace()        
        return None
   

def fix_df(df):
    print('fixing df')
    df = df.dropna(subset=['pcapData'])
    channel_length = len(string_to_list(df.pcapData.iloc[0]))
    res = df.apply(lambda row: string_to_list(row['pcapData']), axis=1)
    df[[ 'channel_'+str(i) for i in range(channel_length) ]] = pd.DataFrame(res.tolist(), index= res.index)
    df = df.drop(columns=['pcapData'])
    print('done!')
    return df

def read_csv(file_path, fix=False, write_fixed=False):
    df = pd.read_csv(file_path)
    if fix:
        df = fix_df(df)
    if write_fixed:
        # df.to_csv(file_path + '_fixed.csv', index=False)
        df.to_csv('pcap_data_sorted.csv', index=False)
    return df

file_path = 'pcap_data.csv'
df = read_csv(file_path, fix=True, write_fixed=True)