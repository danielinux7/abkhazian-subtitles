# Test clips length integrity
import pandas as pd
from pydub import AudioSegment

df = pd.read_csv('dub.tsv', sep='\t', quoting=3)

count=0
allCount=0
for row in df.iterrows():
  try:
    clip = AudioSegment.from_wav("clips/"+row[1]["clip"])
    if float(row[1]["duration"]) < clip.duration_seconds:
      print(row[1]["clip"]+": duration is "+ str(round(clip.duration_seconds,3))+", it should be "+str(row[1]["duration"]))
      count+=1
    allCount+=1
    continue
  except Exception:
    pass

if count > 0:      
  print("Faild test: "+str(count)+" out of "+str(allCount)+" ("+str(round(count/allCount*100,2))+"%)")
else:
  print("Everything looks good!")
