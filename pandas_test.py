# test the task with pandas
import pandas as pd
import time


for i in [1,2,4,6,8,10]:
    start_time = time.time()
    filename=f'~/replicate_data/SCOPUS_DATA_{i}x.csv'
    df = pd.read_csv(filename)
    df = df[['year','Title','Scopus ASJC Code (Sub-subject Area)','Publisher','Citation Count']]
    df.rename(columns={'Title': 'Journal'}, inplace=True)
    df.rename(columns={'year': 'Year'}, inplace=True)
    df.rename(columns={'Scopus ASJC Code (Sub-subject Area)': 'ASJC Code'}, inplace=True)
    # group, aggregate, and fine the most cited journals
    agg_df = df.groupby(['Year', 'Journal','ASJC Code','Publisher']).agg(Total_Citations=pd.NamedAgg(column='Citation Count', aggfunc='sum')).reset_index().sort_values(['Year','Total_Citations'], ascending=[True, False])
    most_cited_journals=agg_df.drop_duplicates(subset=['Year'],keep='first')
    print(most_cited_journals)
    subject_code_df=pd.read_csv('~/Downloads/archive/ASJC_code.csv')
    subject_code_df.rename(columns={'Description': 'Subject Area'}, inplace=True)
    subject_code_df=subject_code_df[['ASJC Code', 'Subject Area']]
    most_cited_journals=most_cited_journals.merge(subject_code_df,on='ASJC Code',how='left')
    end_time=time.time()
    runtime=end_time - start_time
    print(f"Runtime for {filename}:{runtime} seconds")
    print(most_cited_journals[['Year', 'Journal', 'Publisher', 'Subject Area']])