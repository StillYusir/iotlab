import linecache
import json


# # 返回文本中指定行
# def get_line_context(file_path, line_number):
#     origin = linecache.getline(file_path, line_number).strip()
#     print("原生字段:", origin)
#     return origin

# 可显示使用循环, 注意enumerate从0开始计数，而line_number从1开始
def getline(file_path, line_number):
    if line_number < 1:
        return ''
    for cur_line_number, line in enumerate(open(file_path, 'r', encoding='utf-8', errors='ignore')):
        if cur_line_number == line_number - 1:
            print("原生字段:", line)
            return line
    return ''


# def locate_str(origin, start, end,):
#     # 定位返回具体位置上的字符
#     ll = []
#     for s in origin:
#         ll.append(s)
#     print(ll[start:end])
#     return ll[start:end]


# 查找替换文本中的某一行
def find_and_replace(origin, start, end, new_str):
    # 定位具体字符位置
    ll = []
    for s in origin:
        ll.append(s)
    print(ll[start:end])

    # 替换
    ll[start:end] = new_str
    str1 = ''.join(ll)
    print("替换之后:", str1)
    # dict1 = json.loads(str1)  # dict
    # return dict1
    str2 = str1.encode("utf-8")
    dict1 = json.loads(str2)  # dict
    return dict1
    # return str2


# 删除文本中的某一行  《注：“非必要情况--勿用”》
def del_one_row(del_line, file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as old_file:
        with open(file_path, 'r+', encoding='utf-8', errors='ignore') as new_file:
            current_line = 0
            # 定位到需要删除的行
            while current_line < (del_line - 1):
                old_file.readline()
                current_line += 1
            # 当前光标在被删除行的行首，记录该位置
            seek_point = old_file.tell()
            # 设置光标位置
            new_file.seek(seek_point, 0)
            # 读需要删除的行，光标移到下一行行首
            old_file.readline()
            # 被删除行的下一行读给 next_line
            next_line = old_file.readline()
            # 连续覆盖剩余行，后面所有行上移一行
            while next_line:
                new_file.write(next_line)
                next_line = old_file.readline()
            # 写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉
            new_file.truncate()
        new_file.close()
    old_file.close()
    print("删除第{}行成功！".format(del_line))


# 追加一行
def write_one_row(new_str, file_path):
    with open(file_path, 'a+', encoding='utf-8', errors='ignore') as f:
        new_str = new_str.decode("utf-8")
        f.write(new_str)
        f.close()
    print("追加写入成功！")


# 返回总行数
def iter_count(file_path):
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


def deal_error_row(dic):
    with open("../static/static_pos_count.json", "r", encoding='utf-8') as f:
        temp = json.loads(f.read())
        val = temp['data']
        for key, value in val.items():
            if key == dic["JobType"]:
                val[key] = int(value) + 1

    jsontext = {"data": {}}
    jsontext["data"] = val
    jsondata = json.dumps(jsontext, indent=4, separators=(",", ":"), ensure_ascii=False)
    with open("../static/static_pos_count.json", "w", encoding="utf-8") as f:
        f.write(jsondata)
    print("处理成功！")


if __name__ == '__main__':
    file_path = "../static/static_combine_job.json"
    line_number = 43796
    start = 976
    end = 978
    new_str = ''

    # origin = get_line_context(file_path, line_number)
    origin = getline(file_path, line_number)
    dict1 = find_and_replace(origin=origin, start=start, end=end, new_str=new_str)

    deal_error_row(dict1)

    # write_one_row(str1, file_path)
    # del_one_row(line_number, file_path)

    # sum_lines = iter_count(file_path)
    # print(sum_lines)

    # locate_str(new_str, start=976, end=978)
