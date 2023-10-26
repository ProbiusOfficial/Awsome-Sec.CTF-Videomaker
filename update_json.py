import json
import time
import requests

def fetch_and_clean_data_for_uid(uid):

    time.sleep(1)  

    base_url = "https://api.bilibili.com/x/space/wbi/arc/search?mid={}&tid={}"
    all_cleaned_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
    }

    for tid in [36, 188]:
        response = requests.get(base_url.format(uid, tid), headers=headers)
    
        print(f"Status code for UID {uid} with TID {tid}: {response.status_code}")
        print(f"Response content for UID {uid} with TID {tid}: {response.text[:500]}...") 
        
        data = response.json()
        vlist_data = data.get("data", {}).get("list", {}).get("vlist", [])
        for item in vlist_data:
            cleaned_item = {key: item[key] for key in ["play", "title", "bvid", "created"] if key in item}
            all_cleaned_data.append(cleaned_item)
    
    return all_cleaned_data

def update_data_json(filename="data.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    for main_category, sub_categories in data.items():
        if isinstance(sub_categories, dict):
            for sub_category, ups in sub_categories.items():
                for up_name, up_data in ups.items():
                    uid = up_data.get("UID")
                    if uid:
                        content_data = fetch_and_clean_data_for_uid(uid)
                        up_data["Content"] = content_data

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

update_data_json()