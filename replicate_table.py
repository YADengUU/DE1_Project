import pandas as pd
import glob

combined_df = pd.read_csv("SCOPUS_DATA.csv")

for i in range(2, 12, 2):
    replicated_df = pd.concat([combined_df]*i, ignore_index=True)
    filename = f'replicate_data/SCOPUS_DATA_{i}x.csv'
    replicated_df.to_csv(filename, index=False)