# CS50’s Introduction to AI with Python

## 课程简介

- 所属大学：Harvard
- 先修要求：基本概率论 + Python基础
- 编程语言：Python
- 课程难度：🌟🌟🌟
- 预计学时：A month

一门非常基础的AI入门课，让人眼前一亮的是12个设计精巧的编程作业，都会用学到的AI知识去实现一个简易的游戏AI，比如用强化学习训练一个Nim游戏的AI，用alpha-beta剪枝去扫雷等等，非常适合新手入门或者大佬休闲。

## 课程资源

- 课程网站：https://cs50.harvard.edu/ai/2020/
- 课程视频：https://cs50.harvard.edu/ai/2020/
- 课程教材：无
- 课程作业：https://cs50.harvard.edu/ai/2020/，12个精巧的编程作业
- 实验参考：[PKUFlyingPig/cs50_ai - GitHub](https://github.com/PKUFlyingPig/cs50_ai)

## 实验记录

- [degress](./Lecture-0-Search/degrees/) 不同的演员通过主演的电影建立关系，求两个演员中的最短关系
    - 通过 **bfs 搜索** source 到 target 最短路径，找到 target 后，通过 node 的 parent 自下而上恢复出最短路径
- [tic tac toe](./Lecture-0-Search/tictactoe/) 3*3 的三子棋，赢得比赛
    - 核心是 **Adversarial Search 对抗性搜索**，即 minimax。
    - 已知 state，可以得到可以进行的 actions，当做一步 action 时，对 action 进行评分，如果我们是 X，希望全局评分最高，但是 O 也会做最优决策（希望全局评分最低）
    - 当 X 做出行动时 `result(board, action)`，要去预测 O 的最优行为 `min_value(result(board, action))`，O 会基于 X 行动后的结果 `result(board, action)`，去预测 X 的最优行为 `max_value(result(board, action))`，因此算法实现上用「递归」实现
    - X 会根据当前 state 得到多个可能的 action，每个 action 会站在 O 的最优行为的基础上得到一个分数 `min_value(result(board, action))`，X 的当前最优行为就是在这些 action 对应的分数中，最大分数的那个 action `Actions[argmax(v)]`
    - 当前的 action 较多时，预测的速度会慢，如刚开始玩的前几步。可以通过 **Alpha-Beta Pruning 剪枝**。
- [knights](./Lecture-1-Knowledge/knights/) 根据不同人说的话，判断他们的角色
    - 实现起来很简单，**把人类的自然语言写成机器语言**，放入 knowledge 中即可
    - 最有意思的代码是 `model_check(knowledge, query)` 和其中的 `check_all(knowledge, query, symbols, model)`，证明了基于已有的 knowledge，这个 query 是否正确
    - model_check 中会生成所有的 symbols，check_all 每次会选择一个 symbol，基于这个 symbol 以类似回溯法的方式，在 model 中将这个 symbol 置为 true 或 false
    - 当 symbols 消耗完，递归也就结束了，结束时判断基于 knowledge，query 在这个 model 下是否成立
    - 本质上，**model_check 针对一条 query 生成了多个 symbols 的 true or false 的排列组合，也就是 model，在递归结束时，对 model 进行正确性判断**
- [minesweeper](./Lecture-1-Knowledge/minesweeper/) AI 玩扫雷
    - 主要是实现 `def add_knowledge(self, cell, count):` 方法，难道非常大；
    - **当我们做出行动后，需要基于此行动得出新的结论，将新的结论记录到我们的知识库中；而新的结论可能导致已有知识库的再次更新**，这就是这个 lab 学到的东西
    - 该方法会在 cell 已经执行后触发，且是 safe，count 为该 cell 上数字，即 cell 周围可能的 mine 数量
    - 会标记该 cell 已经走过；且是 safe 的；同时在 knowledge 中记录点击这个 cell 后，新增加的 sentence `Sentence(neighbors, count - neighbor_mines)`
    - `self.conclude()`: knowledge 更新后，是否有一些新的 cells 可以被推导出为 safe or mine
    - `self.infer()`: 根据已有的 knowledge，是否能添加一些新的 sentences 到 knowledge 中
    - python 中的 set 还是很好用的
- [pagerank](./Lecture-2-Uncertainty/pagerank/) 统计每个页面的重要程度，应用于 google 展示搜索结果
    - 实现两种算法，Random Surfer Model，Iterative Algorithm
    - Random Surfer Model: `sample_pagerank(corpus, damping_factor, n)`
        - 模拟从一个网页出发，按照已得出的概率往下去点击，重复 n 次，得出所有网页的 rank value
        - 每次选择下个网页的概率是通过 `transition_model(corpus, page, damping_factor)` 提前算好的，即选择下个网页的概率是已知且不变的
    - Iterative Algorithm: `iterate_pagerank(corpus, damping_factor)`
        - **当前网页的 pagerank 是由之前的 pagerank 推导来的**，初始时刻每个网页为 1/n
        - by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula.
        - 当所有新老 pagerank 的差距小于 0.001 时，跳出迭代
