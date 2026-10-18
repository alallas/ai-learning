
import re
import sys
from pathlib import Path


def normalize_text(texts):
    # 先统一小写，再把所有标点替换成空格，保留字母和数字

    # re.sub(pattern, repl, string)
    # 1. pattern：要匹配的模式，通常是正则表达式。
    # （\s是空格）
    # 2. repl：替换成什么内容。
    # 3. string：要处理的原字符串。
    return re.sub(r"[^a-z0-9\s]", " ", texts.lower())


def find_most_freq_20_words(texts):
    counts = {}
    for text in normalize_text(texts).split():
        if text in counts:
            counts[text] += 1
        else:
            counts[text] = 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20]


def find_most_freq_20_words_v2(texts):
    counts = {}
    for text in normalize_text(texts).split():
        counts[text] = counts.get(text, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:20]


def count_words_from_file(file_path):
    # 打开文件，执行完：后面的内容就会关闭文件。
    # 可以手写f = open()， text = f.read()， f.close()
    # 但是用with更好，这就是 Python 里常见的“打开文件并读取内容”的标准写法。
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return find_most_freq_20_words_v2(text)


# 下面这一行表示：
# __name__ 是 Python 里每个脚本都有的一个特殊变量
# 当你直接运行这个文件，比如：python wordcount.py test_eng.txt
# 那么 __name__ 的值就是 "__main__"，所以这段代码就会执行。

# 如果这个文件被别的文件导入，比如：import wordcount
# 那么 __name__ 就不是 "__main__"，这段代码就不会执行。

if __name__ == "__main__":


    # sys.argv 是 Python 运行时接收到的参数列表
    # 运行 python wordcount.py test_eng.txt
    # 那么 sys.argv 大概是：['wordcount.py', 'test_eng.txt']
    # 长度是 2，所以这行判断通过。
    # 如果你没传参数，或者传了多个参数，长度就不是 2，就会打印用法说明，并退出程序：sys.exit(1)，这里的 1 表示“退出码为 1”，通常表示出错。



    if len(sys.argv) != 2:
        print("用法：python wordcount.py <txt文件的相对路径>")
        print("例如：python wordcount.py test_eng.txt")
        print("或：python wordcount.py day3/test_eng.txt")
        sys.exit(1)


    # 拿到你传入的第一个参数，例如 test_eng.txt，转成 Path 对象，方便处理文件路径
    # 判断这个路径对应的文件是否真的存在。如果不存在，就打印错误信息，并退出

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"文件不存在：{file_path}")
        sys.exit(1)

    # 执行文本统计
    result = count_words_from_file(file_path)
    print(result)


# sorted(counts.items(), key=lambda x: x[1], reverse=True)[:20]的解释：
# 假设统计结果是：
# counts = {'apple': 5, 'banana': 3, 'orange': 8}

# ① counts.items() —— 把字典变成 (键, 值) 元组的集合：
# [('apple', 5), ('banana', 3), ('orange', 8)]

# ② key=lambda x: x[1] —— 告诉 sorted 按什么排序：
# lambda x: x[1] 是一个匿名函数：对每个元素 x，取它的第 2 个分量（索引从 0 开始，x[0] 是词，x[1] 是次数）
# 也就是"按频次排序"，而不是按词的名字排序

# ③ reverse=True —— 降序排列（默认是升序，所以要反转）：
# [('orange', 8), ('apple', 5), ('banana', 3)]

# ④ [:20] —— 切片，取排序后列表的前 20 个元素。不足 20 个就全取，不会报错。
# 各部分的等价写法

# lambda 部分也可以写得更直白：
# def get_count(pair):      # pair 就是 ('orange', 8) 这样的元组
#     return pair[1]        # 返回 8
# sorted(counts.items(), key=get_count, reverse=True)[:20]
# lambda 只是把这个函数压缩成了一行。

# 一个小坑
# 如果想让次数相同时按词的字典序排列，可以这样：
# sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:20]
# -x[1] 表示按次数降序，x[0] 表示次数相同时按词升序（不再需要 reverse=True）。
# 同理，如果 counts 里存的不是 (词, 次数) 而是别的结构，只需把 x[1] 换成对应的下标或字段名即可。