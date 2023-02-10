import json
from os.path import exists
f = open('caption.json')
data = json.load(f)
temp = []
for sub in data:
  if(not exists(sub['clip'])):
    temp.append(sub)
data = temp;

with open('caption-left.json', 'w', encoding='utf-8') as output_file:
 output_file.write(json.dumps(data, indent=4, ensure_ascii=False))
 
