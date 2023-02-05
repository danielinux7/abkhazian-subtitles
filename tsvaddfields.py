import pandas as pd

df = pd.read_csv('caption.tsv', sep='\t', quoting=3, names=['start','end','source','target','gender'])
df['start_sec'] = round(pd.to_timedelta(df['start']).dt.total_seconds(),3)
df['end_sec'] = round(pd.to_timedelta(df['end']).dt.total_seconds(),3)
df['duration'] = round(df['end_sec'] - df['start_sec'],3) 
temp = []
for i in df.index:
 if i < len(df)-1:
  temp.append(round(df['start_sec'][i+1] - df['end_sec'][i],3))
 else:
  temp.append(5)
df['extra'] = temp
df['clip'] = [ str(i+1) for i in range(0, (len(df.index)), 1) ]
df['length'] = [ len(str(df['source'][i])) for i in range(0, (len(df.index)), 1) ]
df.to_csv('caption-edited.tsv', sep='\t', quoting=3, index=False, columns = ['clip','start','end','start_sec','end_sec','duration','extra','source','target','gender','length'])
