import nltk
import sys
import string
import math
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    dictionary = dict()
    
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if file[-4:] == ".txt":
            with open(path, 'r', encoding = "utf8") as f:
                dictionary[file] = f.read()
    
    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words_list = []
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    words = nltk.word_tokenize(document.lower())
    
    for i in words:
        if i not in stopwords and i not in punctuation:
            words_list.append(i)
            
    return words_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    word_count = dict()
    word_IDF = dict()
    
    for file in documents:
        words_used = []
        for word in documents[file]:
            if word not in words_used:
                words_used.append(word)
                try:
                    word_count[word] += 1
                except:
                    word_count[word] = 1
    
    for word in word_count:
        word_IDF[word] = math.log(len(documents)/word_count[word])
    
    return word_IDF


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    tf_idfs = dict()
    
    for f in files:
        tf_idfs[f] = 0
        for word in query:
            tf_idfs[f] += files[f].count(word) * idfs[word]
    
    keys, values = sorted(tf_idfs.items(), key = lambda item: item[1], reverse = True)
    
    return keys[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    ranked_sentences = []
    rank = []
    
    for s in sentences:
        score = [s, 0, 0]
        for word in query:
            if word in sentences[s]:
                score[1] += idfs[word]
                score[2] += sentences[s].count(word) / len(sentences[s])
        
        ranked_sentences.append(score)
    
    sort = sorted(ranked_sentences, key = lambda item: (item[1], item[2]), reverse = True)
    
    for sentence, mwm, qtd in sort:
        rank.append(sentence)
    
    return rank[:n]


if __name__ == "__main__":
    main()

















