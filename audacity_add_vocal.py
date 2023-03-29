import json
import os
from os.path import exists
import time
import pipeclient

f_data = open("caption.json")
data = json.load(f_data)
client = pipeclient.PipeClient()
label = [];
client.write("NewMonoTrack:")
for sub in data:
  name = os.path.abspath(os.getcwd()) + "/" +sub["clip"];
  if(exists(name)):
    start = str(sub["start_sec"]);
    end = str(sub["start_sec"]+10);
    duration = str(sub["end_sec"]-sub["start_sec"]);
    client.write("Import2: Filename="+name)
    client.write("SelectTime: Start=0 End=10")
    client.write("NoiseReduction:")
    client.write('FilterCurve:f0="62.77682" f1="70.002037" f10="336.65327" f11="492.91565" f12="591.0509" f13="689.68267" f14="776.07428" f15="889.28813" f16="982.67802" f17="9948.9608" f18="11195.196" f19="12597.538" f2="73.252718" f20="14047.435" f21="16096.677" f3="83.938837" f4="97.946153" f5="119.59827" f6="152.81833" f7="195.26572" f8="221.72906" f9="256.39197" FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" v0="-41.952381" v1="-10.904762" v10="0.031745911" v11="-2.984127" v12="-1.3650789" v13="-0.015872955" v14="0.469841" v15="0.469841" v16="-0.015872955" v17="-0.015872955" v18="-0.031746864" v19="-0.031746864" v2="-5.2349215" v20="-1.7301588" v21="-41.885715" v3="-1.6888895" v4="0.13650751" v5="1.1746035" v6="2" v7="2" v8="1.3015871" v9="0.031745911"')
    client.write('Compressor:AttackTime="0.1" NoiseFloor="-40" Normalize="0" Ratio="2" ReleaseTime="1" Threshold="-18" UsePeak="0"')
    client.write("Normalize: PeakLevel=-6")
    if ("extended" in sub and sub["extended"]==True):
      client.write("SelectTime: Start=0 End="+duration)
      label.append(str(sub["start_sec"])+"\t"+str(sub["end_sec"])+"\t"+sub["clip"]+". "+sub["target"]+"\n")
    client.write("Copy:")
    client.write("SelectTracks: Track=0 Mode=Set")
    client.write("SelectTime: Start="+start+" End="+end)
    client.write("Paste:")
    client.write("SelectTracks: Track=1 Mode=Set")
    client.write("RemoveTracks:")
l = open("extended.txt", "w");
l.writelines(label);
