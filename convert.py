"""
转换格式
源数据：https://github.com/yooongchun/english-words/blob/master/words_dictionary.json
"""

import json
from collections import defaultdict

with open("words_dictionary.json", "r") as fp:
    data = json.load(fp)

result = defaultdict(set)
for word, info in data.items():
    result[len(word)].add(word)
result2 = {}
for k, v in result.items():
    result2[k] = sorted(v)
    print(k, len(v), str(result2[k][:10]) + "...")

with open("words.json", "w") as fp:
    json.dump(result2, fp, indent=4, ensure_ascii=False)
