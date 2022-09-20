import pandas as pd

df = pd.read_csv('caption.tsv', sep='\t', quoting=3, names=['start','end','sentence'])
df['start_sec'] = round(pd.to_timedelta(df['start']).dt.total_seconds(),3)
df['end_sec'] = round(pd.to_timedelta(df['end']).dt.total_seconds(),3)
df['duration'] = round(df['end_sec'] - df['start_sec'],3)
df['clip'] = [ str(i+1)+'.wav' for i in range(0, (len(df.index)), 1) ]
df.to_csv('caption.tsv', sep='\t', quoting=3, index=False, columns = ['clip','start_sec','duration','sentence'])
