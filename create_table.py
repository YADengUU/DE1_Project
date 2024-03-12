import pandas as pd
import glob

# pattern to match the files, the files should be in the current directory
file_pattern = "/home/ubuntu/CS_201*.csv"
file_list = glob.glob(file_pattern)

# initialize an empty dataframe
combined_df = pd.DataFrame()

# loop through teh files
for file in file_list:
    temp_df = pd.read_csv(file)
    year = int(file.split('_')[1].split('.')[0])
    temp_df['Year'] = year
    combined_df = pd.concat([combined_df,temp_df], ignore_index=True)

combined_df.to_csv("SCOPUS_DATA.csv", index=False)