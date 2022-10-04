import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    like: {A, B, C} = 2
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def conclude(self):
        """
        return the number of new clues that can be directly concluded 
        from the sentences in AI's knowledge base, i.e. the number of 
        cells in one sentence equals count or count == 0
        """
        # knowledge 更新后，是否有一些新的 cells 可以被推导出为 safe or mine
        new_clue = 0
        mine_cells = []  # 存储所有新得出的 mine cells
        safe_cells = []  # 存储所有新得出的 safe cells
        for sentence in self.knowledge:  # 检查 knowledge 中所有的 sentence
            if sentence.known_mines():  # 如果这个 sentence 中的所有 cells 都是 mine
                new_clue += 1
                mine_cells += list(sentence.known_mines())
            if sentence.known_safes():  # 如果这个 sentence 中的所有 cells 都是 safe
                new_clue += 1
                safe_cells += list(sentence.known_safes())
        if len(mine_cells) > 0:
            for cell in mine_cells:
                self.mark_mine(cell)  # 添加到已知的 mine 中
        if len(safe_cells) > 0:
            for cell in safe_cells:
                self.mark_safe(cell)  # 添加到已知的 safe 中
        return new_clue

    def infer(self):
        """
        return the number of new clues that can be inferred from 
        AI's knowledge base, i.e. if set1 is a subset of set2, 
        then we can construct the new sentence set2 - set1 = count2 - count1
        """
        # 根据已有的 knowledge，是否能添加一些新的 sentences 到 knowledge 中
        new_clue = 0
        new_knowledge = []  # 存储所有新得出的 sentences
        for i in range(len(self.knowledge)):  # 当前的 sentence
            for j in range(i + 1, len(self.knowledge)):  # 后面的 sentence
                # 当当前的 sentence 和后面的任意 sentence 不一样时，就可能有新的 sentence 出现
                if self.knowledge[i].cells < self.knowledge[j].cells:
                    # 后面的 sentence 包含了当前的 sentence
                    tmp = Sentence(self.knowledge[j].cells - self.knowledge[i].cells,
                                   self.knowledge[j].count - self.knowledge[i].count)
                    flag = True
                    for s in self.knowledge:
                        if tmp == s:  # 检查这个可能的 sentence 是否已知
                            flag = False
                            break
                    if not flag:  # 已知的话就跳过
                        continue
                    new_clue += 1
                    new_knowledge.append(tmp)  # 存储这个新的 sentence
                elif self.knowledge[j].cells < self.knowledge[i].cells:
                    # 如果当前的 sentence 包含了后面的 sentence
                    tmp = Sentence(self.knowledge[i].cells - self.knowledge[j].cells,
                                   self.knowledge[i].count - self.knowledge[j].count)
                    flag = True
                    for s in self.knowledge:
                        if tmp == s:
                            flag = False
                            break
                    if not flag:
                        continue
                    new_clue += 1
                    new_knowledge.append(tmp)
        self.knowledge += new_knowledge  # 将新得出的 sentences 添加到 knowledge 中
        return new_clue

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 该方法会在 cell 已经执行后触发，且是 safe
        self.moves_made.add(cell)  # 将 cell 添加至以走过的集合中
        self.mark_safe(cell)  # 在所有的 sentence 更新这个已经安全的 cell
        x, y = cell
        neighbors = set()  # 记录这个 cell 周围可能走的 neighbor cell
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if x+i < 0 or x+i >= self.height or y+j < 0 or y+j >= self.width or (i == j == 0):
                    continue
                neighbors.add((x + i, y + j))  # 先获取所有的 neighbors
        neighbors = neighbors - self.safes  # 更新 neighbors 为未知的和已知有地雷的
        neighbor_mines = len(neighbors & self.mines)  # 取 neighbors 中有地雷的 cells
        neighbors = neighbors - self.mines  # 更新 neighbors 为未知的
        # count 为该 cell 上数字，即 cell 周围可能的 mine 数量
        # count - neighbor_mines 就是 cell 周围未知 cells 中，mines 的确切数量
        # 在 knowledge 中记录点击这个 cell 后，新增加的 sentence
        self.knowledge.append(Sentence(neighbors, count - neighbor_mines))

        # 此时还需实现
        # self.conclude(): knowledge 更新后，是否有一些新的 cells 可以被推导出为 safe or mine
        # self.infer(): 根据已有的 knowledge，是否能添加一些新的 sentences 到 knowledge 中
        while 1:
            new_conclude = self.conclude()
            new_infer = self.infer()
            if new_conclude == new_infer == 0:
                # 直到没有新的 cells 并且没有新的 sentences时，终止循环推导
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) == 0:
            return None
        return list(safe_moves)[0]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.width):
            for j in range(self.height):
                possible_moves.add((i, j))
        possible_moves -= self.moves_made
        possible_moves -= self.mines
        if len(possible_moves) == 0:
            return None
        return list(possible_moves)[0]
