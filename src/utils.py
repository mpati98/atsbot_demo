import time
import json

def write_json(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
    # Writing to sample.json
    with open(time.strftime("%Y%m%d-%H%M%S") + ".json", "w+") as outfile:
        outfile.write(json_object)