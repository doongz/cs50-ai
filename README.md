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

