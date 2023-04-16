import json
import csv

def json_to_tsv(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Extract keys from the first object in the array
    keys = data[0].keys()

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)

# Example usage
json_file = 'caption.json'
tsv_file = 'caption.tsv'
json_to_tsv(json_file, tsv_file)
