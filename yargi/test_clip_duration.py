# Test clips length integrity
import json
from pydub import AudioSegment

f = open('caption.json')
srt = json.load(f)

count=0
allCount=0
for i, sub in enumerate(srt):
#  import pdb; pdb.set_trace()
  try:
    clip = AudioSegment.from_wav("clips/"+sub["clip"])
    if float(sub["duration"]) < clip.duration_seconds:
      print(sub["clip"]+": duration is "+ str(round(clip.duration_seconds,3))+", it should be "+sub["duration"])
      count+=1
    allCount+=1
    continue
  except Exception:
    pass

if count > 0:      
  print("Faild test: "+str(count)+" out of "+str(allCount)+" ("+str(round(count/allCount*100,2))+"%)")
else:
  print("Everything looks good!")
f.close()
