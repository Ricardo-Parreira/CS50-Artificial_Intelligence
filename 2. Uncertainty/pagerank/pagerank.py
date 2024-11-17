import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    """if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")"""
    corpus = {
        "1.html": {"2.html", "3.html"},  # Page 1 links to pages 2 and 3
        "2.html": {"3.html"},  # Page 2 links to page 3
        "3.html": {"1.html"},  # Page 3 links back to page 1
        "4.html": set()  # Page 4 has no outgoing links (dangling page)
    }
    print(iterate_pagerank(corpus, DAMPING))





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
    #The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    #The page is a string representing which page the random surfer is currently on.
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    nlinks = len(corpus[page])
    npages = len(corpus)

    if len(corpus[page]) == 0:
        for p in corpus:
            model[p] = 1/npages
        return model

    for p in corpus:
        bonus = 0
        if p in corpus[page]:
            bonus = (1/nlinks) * damping_factor
        model[p] = (1/npages)*(1-damping_factor) + bonus

    return model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_counts = {page: 0 for page in corpus}

    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # Increment the count for the current page
        sample_counts[page] += 1

        # Get the transition probabilities for the current page
        transition_probs = transition_model(corpus, page, damping_factor)

        # Choose the next page based on the transition model
        page = random.choices(
            population=list(transition_probs.keys()),
            weights=list(transition_probs.values())
        )[0]

    # Normalize sample counts to get the PageRank values
    pagerank = {page: count / n for page, count in sample_counts.items()}

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prDict = dict()
    p = random.choice(list(corpus.keys()))

    for p in corpus:
        prDict[p] = 1 / len(corpus)

    for i in corpus:
        if (len(corpus[i]) == 0):
            corpus[i] = set(corpus.keys())

    print("corpus: ", corpus)

    dif = 1
    while dif > 0.001:
        new_ranks=dict()
        dif = 0
        for page in corpus:
            bonus = 0

            for i in corpus:
                if page in corpus[i]:
                    bonus += prDict[i] / len(corpus[i])

            newValue = ((1 - damping_factor) / len(corpus)) + (bonus * damping_factor)
            dif = max(dif, abs(prDict[page] - newValue))
            new_ranks[page] = newValue

        #só se pode dar update no final porque a soma precisa de dar 1, se fizer isto dentro do for dá merda
        prDict=new_ranks.copy()



    return prDict


if __name__ == "__main__":
    main()
