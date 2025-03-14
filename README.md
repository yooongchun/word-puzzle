# 说明

单词解谜类游戏，快速搜索
基本操作是：游戏中给定 N 个字符可以猜测 M 次，每次用户输入之后游戏给出某个位置的某个字符是正确、错位（字符存在于单词中但是位置不对）、不存在（字符不存在于单词中）这三种状态，比如在一个 N=4，M=5的回合中：

<img width="122" alt="image" src="https://github.com/user-attachments/assets/e57039f0-221a-4336-a124-e41fc3f5477c" />

表示第一个 b和第四个 s 是猜测正确的，第二个 a单词内含有但是位置不对，第三个 d 该单词内没有。

# 玩法
首先调用`python convert.py` 将原始单词表转换为目标表。

接着运行程序 `python main.py`
每次输入的时候需要输入你猜测的单词以及游戏给出的状态，比如你猜测 `bads`，猜对的用 1 表示，位置猜错的用2 表示，不存在的用 3 表示，上述图片中的 case 可以表示为输入：`b1a2d3s1`

每次猜测之后程序会进行搜索给出备选答案。

<img width="434" alt="image" src="https://github.com/user-attachments/assets/2efd12ab-2e03-4146-bb9d-f0aa31aaebb7" />

# Have fun!!
