from operator import ne
import os
from pydoc import pager
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus: {'4.html': {'2.html'}, '3.html': {'4.html', '2.html'}, '2.html': {'3.html', '1.html'}, '1.html': {'2.html'}}

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if len(corpus[page]) == 0:
        prob_distribution = dict.fromkeys(corpus.keys(), 1/len(corpus))
    else:
        prob_distribution = dict.fromkeys(
            corpus.keys(), (1-damping_factor)/len(corpus))
        for p in corpus[page]:
            prob_distribution[p] += damping_factor/len(corpus[page])
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # 模拟从一个网页出发，按照已得出的概率往下去点击，重复 n 次，得出所有网页的 rank value
    # 通过 transition_model，其实选择下个网页的概率是已知且不变的
    pagerank = dict.fromkeys(corpus, 0)
    nextpage = random.choice(list(corpus.keys()))
    pagerank[nextpage] += 1

    for _ in range(n-1):
        pro_distri = transition_model(corpus, nextpage, damping_factor)
        # 根据概率取抽样
        x = random.uniform(0, 1)
        cumu_p = 0
        for page, p in pro_distri.items():
            cumu_p += p
            if cumu_p > x:
                break
        nextpage = page  # page 为被抽中的
        pagerank[nextpage] += 1
    for page in pagerank.keys():
        pagerank[page] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # 当前网页的 pagerank 是由之前的 pagerank 推导来的，初始时刻每个网页为 1/n
    # by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula.
    # 当所有新老 pagerank 的差距小于 0.001 时，跳出迭代

    # Assign initial values for pagerank
    pages_number = len(corpus)
    old_dict = {}
    new_dict = {}

    # assigning each page a rank of 1/n, where n is total number of pages in the corpus
    for page in corpus:
        old_dict[page] = 1 / pages_number

    # repeatedly calculating new rank values basing on all of the current rank values
    while True:
        for page in corpus:
            temp = 0
            for linking_page in corpus:
                # check if page links to our page
                if page in corpus[linking_page]:
                    temp += (old_dict[linking_page] /
                             len(corpus[linking_page]))
                # if page has no links, interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    temp += (old_dict[linking_page]) / len(corpus)
            temp *= damping_factor
            temp += (1 - damping_factor) / pages_number

            new_dict[page] = temp

        # This process should repeat until no PageRank value changes by more than 0.001
        # between the current rank values and the new rank values.
        difference = max([abs(new_dict[x] - old_dict[x]) for x in old_dict])
        if difference < 0.001:
            break
        else:
            old_dict = new_dict.copy()

    return old_dict


if __name__ == "__main__":
    main()
