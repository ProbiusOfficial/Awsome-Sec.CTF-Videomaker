import json
from datetime import datetime
import pytz
from urllib.parse import urlparse

key_header = ["Name", "UID", "Category", "Content", "Notes"]
res = {}
res["GenerateTime"] = datetime.now().astimezone(pytz.utc).astimezone(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

with open("./README.md", "r") as f:
    data = f.read().split("\n## ")

data_CTF = [i.split("\n") for i in data[1].split("\n### ")]
data_Security = [i.split("\n") for i in data[2].split("\n### ")]

for i in [data_CTF, data_Security]:
    key_name_main = i[0][0]
    res[key_name_main] = {}
    for j in i[1:]:
        j = [_ for _ in j if _ != ""]
        key_name_sub = j.pop(0)
        res[key_name_main][key_name_sub] = {}
        for k in j[2:]:
            obj = [i.strip() for i in k.split("|")[1:-1] if k.split("|")[2].strip() != ""]
            if obj != []:
                obj = obj.pop(0)[1:-1].split("](") + obj
                obj[1] = urlparse(obj[1]).path.replace("/", "")
                res[key_name_main][key_name_sub][obj[0]] = {key: value for key, value in zip(key_header, obj)}

with open("./data.json", "w") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=4))
