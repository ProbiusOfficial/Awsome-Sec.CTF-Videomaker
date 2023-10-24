import markdown
import re
import json

# 定义Markdown数据
markdown_data = """
| 昵称                                                         | 方向     | 主要课程内容 | 备注        |
| ------------------------------------------------------------ | -------- | ------------ | ----------- |
| [软趴趴の锅边糊](https://space.bilibili.com/475175714/)      | 全栈     |              |             |
| [燕无歇莫问归期](https://space.bilibili.com/387503419/)      | 全栈     |              |             |
| [Nyr4ki](https://space.bilibili.com/388609258)               | WEB      |              |             |
| [国资社畜](https://space.bilibili.com/400157779)             | PWN      |              |             |
| [芥燃斯基](https://space.bilibili.com/479430036)             | PWN      |              |             |
| [Deregistered](https://space.bilibili.com/8538817)           | PWN      |              |             |
| [-Protocol-](https://space.bilibili.com/40691233)            | PWN      |              |             |
| [rod3r1ck](https://space.bilibili.com/3461577038629345)      | PWN      |              |             |
| [Rotten](https://space.bilibili.com/3493278529882882/)       | PWN      |              |             |
| [Mz1不是黑帽子](https://space.bilibili.com/184432814/)       | RE       |              |             |
| [吾爱破解论坛](https://space.bilibili.com/544451485)         | RE       |              |             |
| [r0ysue](https://space.bilibili.com/31025974)                | RE       |              |             |
| [风二西](https://space.bilibili.com/317479700)               | Crypto   |              |             |
| [Alice-Bob](https://space.bilibili.com/552018206/)           | 密码学   |              |             |
| [陈橘mo](https://space.bilibili.com/12949995)                | MISC     |              |             |
| [树木今天吃什么](https://space.bilibili.com/483370591)       | MISC     |              |             |
| [Byxs20](https://space.bilibili.com/183379727)               | MISC     |              |             |
| [GeekHour](https://space.bilibili.com/102438649)             | 基础教程 |              |             |
| [r00t_1](https://space.bilibili.com/317711147)               | awd      |              |             |
| [Aynakeya](https://space.bilibili.com/10003632)              | PWN      |              |             |
| [水番正文](https://space.bilibili.com/39892350)              | RE       |              |             |
| [米利特瑞先生](https://space.bilibili.com/95382392)          | CTF安全研究         |              |           |
| [Soryu_Asuka_Rang](https://space.bilibili.com/390157099)     | 电子数据取证     |              |           |
|                                                              |          |              |             |

"""

# 将Markdown数据分成三个部分：个人向、战队官号、平台官号
sections = re.split(r'###\s+', markdown_data)

# 创建一个空的JSON对象
ctf_json = {
    "CTF_Person": {},
    "CTF_TEAM": {},
    "CTF_Platform": {}
}

# 处理个人向部分
def process_section(section):
    lines = section.strip().split('\n')
    header = lines[0].strip()
    table = '\n'.join(lines[2:])
    table_html = markdown.markdown(table, extensions=['tables'])
    table_lines = table_html.split('\n')
    for line in table_lines:
        if '|' in line:
            columns = [col.strip() for col in line.split('|')]
            if len(columns) >= 4:
                name = columns[1]
                direction = columns[2]
                bilibili_uid = re.search(r'\((https://space.bilibili.com/(\d+))\)', columns[1])
                if bilibili_uid:
                    uid = bilibili_uid.group(2)
                    ctf_json["CTF_Person"][uid] = {
                        "Bilibili_UID": uid,
                        "name": name,
                        "ContentDirection": direction,
                        "Content": []
                    }

# 处理战队官号和平台官号部分
for section in sections[1:]:
    lines = section.strip().split('\n')
    header = lines[0].strip()
    table = '\n'.join(lines[2:])
    table_html = markdown.markdown(table, extensions=['tables'])
    table_lines = table_html.split('\n')
    for line in table_lines:
        if '|' in line:
            columns = [col.strip() for col in line.split('|')]
            if len(columns) >= 4:
                name = columns[1]
                direction = columns[2]
                bilibili_uid = re.search(r'\((https://space.bilibili.com/(\d+))\)', columns[1])
                if bilibili_uid:
                    uid = bilibili_uid.group(2)
                    if header.startswith("战队官号"):
                        ctf_json["CTF_TEAM"][uid] = {
                            "Bilibili_UID": uid,
                            "name": name,
                            "ContentDirection": direction,
                            "Content": []
                        }
                    elif header.startswith("平台官号"):
                        ctf_json["CTF_Platform"][uid] = {
                            "Bilibili_UID": uid,
                            "name": name,
                            "ContentDirection": direction,
                            "Content": []
                        }

# 将JSON对象转换为JSON字符串
ctf_json_str = json.dumps(ctf_json, ensure_ascii=False, indent=4)

# 打印JSON字符串
print(ctf_json_str)
