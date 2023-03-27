import json
import time
import pipeclient

f_data = open("caption.json")
data = json.load(f_data)
client = pipeclient.PipeClient()
for sub in data:
  start = str(sub["start_sec"]);
  end = str(sub["end_sec"]);
  command = "SelectTime: Start="+start+" End="+end;
  print(command);
  client.write(command, timer=True)
  reply = ''
  while reply == '':
    time.sleep(0.1)
    reply = client.read()
  print(reply)
  command = "VocalReductionAndIsolation: action=RemoveToMono strength=0.5 low-transition=120 high-transition=9000"
  client.write(command, timer=True)
  reply = ''
  while reply == '':
    time.sleep(0.1)
    reply = client.read()
  print(reply)
