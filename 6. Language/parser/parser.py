import nltk
from nltk import Tree
import sys
nltk.download('punkt_tab')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> O | O Conj O
O -> NP VP | VP | NP Adv VP
NP -> N | NA N
NA -> Det | Adj | NA NA
VP -> V | V Mod
Mod -> NP | P | Adv | Mod Mod | Mod Mod Mod
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(preprocess(s))
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    frases = nltk.word_tokenize(sentence)
    sentences = []
    for palavra in frases:
            if palavra.isalpha():
                sentences.append(palavra.lower())
    return sentences


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np = []
    flag = True
    for subtree in tree.subtrees():
        flag = True
        if subtree.label() == 'NP':
            for subsubtree in subtree.subtrees():
                if subsubtree == subtree: continue
                if subsubtree.label() == 'NP':
                    flag = False
            if flag:
                np.append(subtree)

    return np

if __name__ == "__main__":
    main()


t = Tree('S', [
    Tree('NP', [Tree('DT', ['The']), Tree('N', ['Holmes'])]),
    Tree('VP', [
        Tree('VBZ', ['drinks']),
        Tree('NP', [Tree('NN', ['tea'])]),
        Tree('PP', [Tree('IN', ['at']), Tree('NP', [Tree('CD', ['five'])])])
    ])
])
print(np_chunk(t))