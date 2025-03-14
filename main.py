import enum
import re
import json
import random
import tabulate
from collections import defaultdict
from colorama import init, Fore

init()


def load_words(num_chars: int, path: str = "words.json"):
    with open(path, "r") as f:
        words = set(json.load(f)[str(num_chars)])
        print(f"num_chars: {num_chars}, words: {len(words)}")
        return words


def delete_word(words: set, word: str, path: str = "words.json"):
    words.remove(word)
    with open(path, "r+") as f:
        data = json.load(f)
        data[len(word)] = sorted(words)
        # 将文件指针移到文件开头，以便覆盖原有内容
        f.seek(0)
        # 清空文件剩余内容（如果新写入的数据比原数据短）
        f.truncate()
        # 将修改后的数据写回文件
        json.dump(data, f, indent=4)
    print(f"Deleted word: {word}")


def get_candidates(
    words: set,
    must_include: set = set(),
    must_exclude: set = set(),
    exact: dict = {},
    exact_not: dict = defaultdict(set),
    limit: int = 100,
) -> list:
    # 将集合转换为列表，以便后续可以使用 random.shuffle 函数
    results = set()
    for w in words:
        # 必须包含的字母
        flag = False
        for x in must_include:
            if x not in w:
                flag = True
                break
        if flag:
            continue

        # 必须排除的字母
        for x in must_exclude:
            if x in w:
                flag = True
                break
        if flag:
            continue

        # 精确位置的字母
        for i, x in exact.items():
            if w[i] != x:
                flag = True
                break
        if flag:
            continue

        # 错位的字母
        for i, xs in exact_not.items():
            if w[i] in xs:
                flag = True
                break
        if flag:
            continue

        results.add(w)

    results = list(results)
    random.shuffle(results)
    return results[:limit]


def init_table():
    raw = input("请输入单词字符数&最大猜测次数 N x M: ")
    chunks = re.split(r",|\s+", raw.strip())
    n, m = int(chunks[0]), int(chunks[1])
    return n, m


class State(enum.Enum):
    CORRECT = 1
    EXIST = 2
    NOT_EXIST = 3

    @classmethod
    def get_state(cls, w_char: str, code: str):
        if int(code) == State.CORRECT.value:
            return Fore.GREEN + w_char + Fore.RESET
        elif int(code) == State.EXIST.value:
            return Fore.YELLOW + w_char + Fore.RESET
        else:
            return Fore.LIGHTBLACK_EX + w_char + Fore.RESET


def print_table(main_table, candi_table):
    candi_str = tabulate.tabulate(candi_table, tablefmt="fancy_grid").split("\n")
    main_str = tabulate.tabulate(main_table, tablefmt="fancy_grid").split("\n")
    # 并排打印表格
    for row1, row2 in zip(main_str, candi_str):
        print(row1.ljust(len(max(row2, key=len))), row2)


def match_rule(
    raw_guess: str, must_include: set, must_exclude: set, exact: dict, exact_not: dict
):
    for i in range(0, len(raw_guess), 2):
        j = i // 2
        code = int(raw_guess[i + 1])
        if code == State.CORRECT.value:
            exact[j] = raw_guess[i]
            must_include.add(raw_guess[i])
        elif code == State.EXIST.value:
            exact_not[j].add(raw_guess[i])
            must_include.add(raw_guess[i])
        else:
            if raw_guess[j] in must_include:
                continue
            must_exclude.add(raw_guess[i])


def get_candi_table(candidates: list, min_rows: int):
    # 转换为 n 列的表格
    n_candi = len(candidates)
    n_tail = int(n_candi % m > 0)
    n_cols = n_candi // m + n_tail
    candi_table = [candidates[i : i + n_cols] for i in range(0, n_candi, n_cols)]
    candi_table = [
        [State.get_state(w_char, "3") for w_char in row] for row in candi_table
    ]
    if len(candi_table) < min_rows:
        candi_table += [[""] * n_cols] * (min_rows - len(candi_table))
    return candi_table


def start_game(words: set, n: int, m: int, limit: int = 100):
    main_table = [[" "] * n for _ in range(m)]
    must_include = set()
    must_exclude = set()
    exact = {}
    exact_not = defaultdict(set)
    # 候选清单
    candidates = get_candidates(words=words, limit=limit)
    candi_table = get_candi_table(candidates, min_rows=m)
    print_table(main_table, candi_table)

    # 开始
    current_guess = 0
    while current_guess < m:
        current_guess += 1
        guess = input("请输入猜测的单词: ")
        rule = rf"^x\s+[a-zA-Z]{{{n}}}$"
        if re.match(rule, guess):
            delete_word(words, guess[1:].strip())
            current_guess -= 1
            continue
        if len(guess) != n * 2:
            print("请输入长度为目标单词两倍的字符串！")
            continue
        # 获取候选词
        match_rule(guess, must_include, must_exclude, exact, exact_not)
        candidates = get_candidates(
            words=words,
            must_include=must_include,
            must_exclude=must_exclude,
            exact=exact,
            exact_not=exact_not,
            limit=100,
        )
        render_guess = [
            State.get_state(guess[i], guess[i + 1]) for i in range(0, len(guess), 2)
        ]
        main_table[current_guess - 1] = render_guess
        candi_table = get_candi_table(candidates, min_rows=m)
        print_table(main_table, candi_table)
        if all(int(v) == State.CORRECT.value for v in guess[1::2]):
            print("YOU WIN!!")
            break


if __name__ == "__main__":
    # 初始化
    n, m = init_table()
    words = load_words(n)
    start_game(words=words, n=n, m=m, limit=100)
