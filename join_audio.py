import json;
from tqdm import tqdm;
from pydub import AudioSegment;
from os.path import exists
import re, os

m = re.compile('^[0-9]*_metadata.json$')
d = re.compile('^[0-9]*.json$')
for file in os.scandir('.'):
    if file.is_file() & bool(m.match(file.name)):
      f_meta = open(file.name)
for file in os.scandir('.'):
    if file.is_file() & bool(d.match(file.name)):
      f_data = open(file.name)
metadata = json.load(f_meta)
data = json.load(f_data)
for meta in metadata:  
  temp = []
  for sub in data:
    if(exists("../"+meta["charType"]+"/"+sub["clip"]) and ("extended" not in sub or sub["extended"]==False)):
      temp.append(sub)
  if len(temp) > 0:
    Sound_list = [];
    label = [];
    pad = AudioSegment.silent(duration=temp[0]["start_sec"]*1000);
    Sound_list.append(pad);
    for i, sub in tqdm(enumerate(temp)):
         clip = AudioSegment.from_file("../"+meta["charType"]+"/"+sub["clip"])
         if (i+1 < len(temp)): 
           pad = AudioSegment.silent(duration=((temp[i+1]["start_sec"]-(sub["start_sec"]+clip.duration_seconds))*1000)-1.7);
         Sound_list.append(clip);
         Sound_list.append(pad);
         label.append(str(sub["start_sec"])+"\t"+str(sub["end_sec"])+"\t"+sub["clip"]+". "+sub["target"]+"\n")
    Sound_list_2 = []
    i = 0;
    while (i < len(Sound_list)):
      if (i+100 >= len(Sound_list)):
          Sound_list_2.append(sum(Sound_list[i:len(Sound_list)]));
      else:
          Sound_list_2.append(sum(Sound_list[i:i+100]));
      print(i);
      i= i+100;
    final_sound = sum(Sound_list_2);
    final_sound.export("../audio_"+meta["charType"]+".m4a", format="mp4");
    l = open("../audio_"+meta["charType"]+".txt", "w");
    l.writelines(label);

  temp = []
  for sub in data:
    if(exists("../"+meta["charType"]+"/"+sub["clip"]) and "extended" in sub and sub["extended"]==True):
      temp.append(sub)
  if len(temp) > 0:
    Sound_list = [];
    label = [];
    pad = AudioSegment.silent(duration=temp[0]["start_sec"]*1000);
    Sound_list.append(pad);
    for i, sub in tqdm(enumerate(temp)):
         clip = AudioSegment.from_file("../"+meta["charType"]+"/"+sub["clip"])
         if (i+1 < len(temp)): 
           pad = AudioSegment.silent(duration=((temp[i+1]["start_sec"]-(sub["start_sec"]+clip.duration_seconds))*1000)-1.7);
         Sound_list.append(clip);
         Sound_list.append(pad);
         label.append(str(sub["start_sec"])+"\t"+str(sub["end_sec"])+"\t"+sub["clip"]+". "+sub["target"]+"\n")
    Sound_list_2 = []
    i = 0;
    while (i < len(Sound_list)):
      if (i+100 >= len(Sound_list)):
          Sound_list_2.append(sum(Sound_list[i:len(Sound_list)]));
      else:
          Sound_list_2.append(sum(Sound_list[i:i+100]));
      print(i);
      i= i+100;
    final_sound = sum(Sound_list_2);
    final_sound.export("../audio_"+meta["charType"]+"_extended.m4a", format="mp4");
    l = open("../audio_"+meta["charType"]+"_extended.txt", "w");
    l.writelines(label);
