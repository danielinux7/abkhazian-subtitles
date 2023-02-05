import json

def tsv2json(input_file,output_file):
 arr = []
 file = open(input_file, 'r')
 a = file.readline()
 
 # The first line consist of headings of the record
 # so we will store it in an array and move to
 # next line in input_file.
 titles = [t.strip() for t in a.split('\t')]
 for line in file:
  d = {}
  for t, f in zip(titles, line.split('\t')):

   # Convert each row into dictionary with keys as titles
   d[t] = f.strip()
   if t == "duration" or t == "start_sec" or t == "end_sec" or t == "extra":
     d[t] = float(f.strip())
   if t == "length":
     d[t] = int(f.strip())
  # we will use strip to remove '\n'.
  arr.append(d)
  
  # we will append all the individual dictionaires into list
  # and dump into file.
 with open(output_file, 'w', encoding='utf-8') as output_file:
  output_file.write(json.dumps(arr, indent=4, ensure_ascii=False))

# Driver Code
input_filename = 'caption-edited.tsv'
output_filename = 'caption.json'
tsv2json(input_filename,output_filename)
