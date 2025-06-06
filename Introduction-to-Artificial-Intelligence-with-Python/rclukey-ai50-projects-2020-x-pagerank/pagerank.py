import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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
    
    prob_dist = dict()
    
    if len(corpus[page]) > 0:
        for website in corpus:
            prob_dist[website] = (1-damping_factor) / len(corpus)
            if website in corpus[page]:
                prob_dist[website] += damping_factor / len(corpus[page])
    
    else:
        prob = 1/len(corpus)
        for website in corpus:
            prob_dist[website] = prob
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    PageRank = dict()
    sample = random.choices(list(corpus.keys()))[0]
    
    for website in corpus:
        PageRank[website] = 0
    
    PageRank[sample] += (1/n)
    
    for i in range(n):
        dist_model = transition_model(corpus, sample, damping_factor)
        websites, probability = zip(*dist_model.items())
        sample = random.choices(websites, weights = probability)[0]
        
        PageRank[sample] += (1/n)
    
    return PageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    PageRank = dict()
    NextPageRank = dict()
    
    opposite_factor = 1-damping_factor
    
    for website in corpus:
        PageRank[website] = 1/len(corpus)
    
    while True:
        counter = 0
        
        for website in PageRank:
            total = 0
            
            for page in corpus:
                if website in corpus[page]:
                    total += PageRank[page] / len(corpus[page])
                if corpus[page] is None:
                    total += PageRank[page] / len(corpus)
            
            NextPageRank[website] = opposite_factor / len(corpus)
            NextPageRank[website] += total * damping_factor
            
        for website in PageRank:
            if abs(PageRank[website] - NextPageRank[website]) > 0.001:
                counter += 1
            PageRank[website] = NextPageRank[website]
        
        if counter == 0:
            break
    
    return PageRank
    

if __name__ == "__main__":
    main()



















