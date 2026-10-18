
def find_most_freq_20_words(texts):
    counts = {}
    for text in texts.split():
        if text in counts :
            counts[text] += 1
        else :
            counts[text] = 1
    return sorted(counts.items(), key = lambda x: x[1], reverse = True)[:20]


def find_most_freq_20_words_v2(texts):
    counts = {}
    for text in texts.split():
        counts[text] =counts.get(text, 0) + 1
    return sorted(counts.items(), key = lambda x: (-x[1], x[0]))[:20]



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