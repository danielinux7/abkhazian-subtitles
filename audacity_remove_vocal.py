import json
import time
import pipeclient

f_data = open("caption.json")
data = json.load(f_data)
client = pipeclient.PipeClient()
for sub in data:
  start = str(sub["start_sec"]-.2);
  end = str(sub["end_sec"]+.2);
  command = "SelectTime: Start="+start+" End="+end;
  print(command);
  client.write(command, timer=True)
  reply = ''
  while reply == '':
    time.sleep(0.1)
    reply = client.read()
  print(reply)
  command = "VocalReductionAndIsolation: action=Remove strength=0.7 low-transition=80 high-transition=9000"
  client.write(command, timer=True)
  reply = ''
  while reply == '':
    time.sleep(0.1)
    reply = client.read()
  print(reply)
