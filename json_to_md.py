import json
import re

def extract_top_videos(content_data):
    # Sort videos by play count and take the top 3
    top_3_videos = sorted(content_data, key=lambda x: x['play'], reverse=True)[:3]
    
    # Sort videos by created date and take the latest 5
    latest_5_videos = sorted(content_data, key=lambda x: x['created'], reverse=True)[:5]
    
    return top_3_videos, latest_5_videos

def format_videos_to_md(top_3_videos, latest_5_videos):
    md_content = "Top 3:<br />"
    for video in top_3_videos:
        md_content += f"[播放量 {video['play']} | {video['title']}](https://www.bilibili.com/video/{video['bvid']})<br />"
    
    md_content += "最近更新：<br />"
    for video in latest_5_videos:
        md_content += f"[{video['title']}](https://www.bilibili.com/video/{video['bvid']})<br />"
    
    print (md_content)
    md_content = md_content.replace("|", "\|")
    return md_content

def update_markdown_with_data(data, markdown_template):
    md_lines = markdown_template.split("\n")
    new_md_lines = []
    
    for line in md_lines:
        if "https://space.bilibili.com/" in line:
            up_uid = re.search(r"https://space.bilibili.com/(\d+)", line)
            if up_uid:
                up_uid = up_uid.group(1)
                print(f"Found UID in README.md: {up_uid}")  # Debug 

                matched = False
                for main_category, sub_categories in data.items():
                    if isinstance(sub_categories, dict): 
                        for sub_category, ups in sub_categories.items():
                            if isinstance(ups, dict): 
                                for up_name, up_data in ups.items():
                                   
                                    if up_data.get("UID") == up_uid:
                                        matched = True
                                        print(f"Found matching UID in data.json: {up_uid}")  
                                        top_3, latest_5 = extract_top_videos(up_data["Content"])
                                        content_md = format_videos_to_md(top_3, latest_5)
                                        columns = line.split("|")
                                        if len(columns) > 3:  
                                            columns[3] = f"{columns[3].strip()} {content_md}"  
                                            line = "|".join(columns)
                                        break  
                                if matched:
                                    break  
                            if matched:
                                break  
                            
                if not matched:
                    print(f"No matching UID in data.json for: {up_uid}")  # Debug 

        new_md_lines.append(line)
    return "\n".join(new_md_lines)



def main():
    with open("data.json", "r", encoding="utf-8") as file:
        data_content = json.load(file)

    with open("README.md", "r", encoding="utf-8") as md_file:
        markdown_content = md_file.read()

    updated_md = update_markdown_with_data(data_content, markdown_content)

    with open("README.md", "w", encoding="utf-8") as md_file:
        md_file.write(updated_md)

if __name__ == "__main__":
    main()
