import requests
import json


data = {"pipeline_name":{"num_blocks":10,"current_block_index":5}}
s = json.dumps(data)


r = requests.post("http://127.0.0.1:5000", data=data)

# END
