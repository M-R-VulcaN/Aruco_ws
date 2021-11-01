import pandas as pd
import ast

def string_to_list(row):
    try:
        return ast.literal_eval(row.replace('\n ', ' ').replace('  ', ' ').replace(' ', ',').replace('[,','['))
        
    # except:
    #     import pdb
    #     pdb.set_trace()        
    #     return None
    except Exception as e: 
        print(e)
        new_row = ['Nan'] *255
        import pdb
        pdb.set_trace()        
        return new_row
   

def fix_df(df):
    print('fixing df')

    df = df.dropna(subset=['pcap_data'])
    channel_length = len(string_to_list(df.pcapData.iloc[0]))
    res = df.apply(lambda row: string_to_list(row['pcap_data']), axis=1)
    df[[ 'channel_'+str(i) for i in range(channel_length) ]] = pd.DataFrame(res.tolist(), index= res.index)
    df = df.drop(columns=['pcap_data'])
    print('done!')

    return df

def read_csv(file_path, fix=False, write_fixed=False, output_file_path = 'dataset_fixed.csv'):
    df = pd.read_csv(file_path)
    
    if fix:
        df = fix_df(df)
    if write_fixed:
        df.to_csv(output_file_path, index=False)
    return df

def main(pcapdata_csv_file_path = 'pcapdata.csv', output_file_path = 'dataset_fixed.csv'):
    df = read_csv(pcapdata_csv_file_path, fix=True, write_fixed=True, output_file_path=output_file_path )

if __name__ == '__main__':
    main()
