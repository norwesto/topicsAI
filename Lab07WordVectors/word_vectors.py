"""File: word_vectors.py
Author: Nora Westol
Date: 03/20/2026"""
# now some imports for toolkits: numpy gives us fast
# vector and matrix operations;
import numpy as np

# now for nltk
import nltk
import os

nltk.data.path = ['/Users/norawestol/nltk_data']
nltk.download('reuters')

# this is the reuters data set
from nltk.corpus import reuters

from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plot

# many data sets use start and end delimiters
START_TOKEN = '<START>'
END_TOKEN = '<END>'

def read_reuters_corpus(category : str ="gold", debug=False) -> list[list[str]]:
    """ Reads and parses the files from the specified Reuter's category.

        Params:
            category (str): category name from reuters/cats.txt
        Return: 
            list of lists with words from each processed file
    """
    # get the list of files associated with a given category, which 
    # will let us put start and end tokens on the words in that category
    files = reuters.fileids(category)

    # TODO: now build a list of words for each file as a list
    # walk through the documents and add the START_TOKEN and END_TOKEN to each document
    # so you end up with a list of words for each document preceded by START_TOKEN and ended by END_TOKEN

    file_words = []
    with open("/Users/norawestol/topicsAI/nltk_data/corpora/reuters/cats.txt", "r") as file:
        for doc_id in files:
            words = reuters.words(doc_id)
            processed_words = [START_TOKEN] + list(words) + [END_TOKEN]
            file_words.append(processed_words)
    
    return file_words
    # DONE: uncomment if you want to pass the debug flag
    # if debug:
    #     print(f'first 3 examples: {file_words[:3]}')
    # return file_words

def get_vocabulary(word_lists : list[list[str]]) -> list[str]:
    """
    From the list of lists of words, create a sorted list of words

    Parameters:
        word_lists: list of list of words from the text

    Returns:
        A sorted list of unique words in the vocabulary 
    """
    # TODO: return a sorted list of all the unique words in all the documents
    words = set()
    for word_list in word_lists:
        words.update(word_list)
    return sorted(words)
    
def create_indexed_vocabulary(vocab : list[str]) -> dict[str, int]:
    """
    Creates a dictionary of vocabulary words to indices.

    Parameters:
        vocab: a sorted list of unique words in the corpus

    Returns:
        A dictionary that maps word to index in vocabulary list
    """
    # TODO: return a dictionary of vocab to indices (assuming the vocab is already sorted)
    vocab_indices = {word: index for index, word in enumerate(vocab)}
    return vocab_indices

def get_co_occurrence_matrix(corpus : list[list[str]], vocab_indices: dict[str, int], vocab_size, window_size = 4, debug = False) -> np.ndarray[np.float64]:
    """
    Create the co-occurrence matrix. 
    
    Parameters:
        corpus: a list of each document, where each document is a list of words in that document
        and includes the start and end tokens (see read_reuters_corpus)

        vocab_indices: a dictionary of word to index mappings

        vocab_size: the number of words in the vocabulary

        window_size: the number of words + or - the center word

    """

    # create a matrix using numpy of vocab_size x vocab_size dimensions, and fill it with zeros
    M = np.zeros((vocab_size, vocab_size))

    # TODO: walk through all the documents and then walk through each word as a center word
    # updating the matrix M with the count of the number of times a word was seen as a neighbor word
    # for a given center word
    for document in corpus:
        for i, center_word in enumerate(document):
            center_index = vocab_indices[center_word]
            # Determine the context window boundaries
            start = max(0, i - window_size)
            end = min(len(document), i + window_size + 1)
            # Update co-occurrence counts for neighboring words
            for j in range(start, end):
                if j != i:  # Skip the center word itself
                    neighbor_word = document[j]
                    neighbor_index = vocab_indices[neighbor_word]
                    M[center_index][neighbor_index] += 1
    
    # and return the matrix
    if debug: 
        print(f'matrix shape: {M.shape}')
    return M

def reduce_to_k_dim(M : np.ndarray[np.float64], k : int = 2, iterations : int = 10) -> np.ndarray[np.float64]:
    """
    Reduce a co-occurrence matrix of dimensionality (vocab_size, vocab_size) to k dimensions
    using singular value decomposition (SVD). You will use TruncatedSVD.

    Parameters:
        M (numpy matrix of shape (vocab_size, vocab_size)): created from your sample
        k (int): the number of dimensions to reduce to, 2 by default
        
    Return:
        M_reduced: (numpy matrix of shape (vocab_size, k)). If you took 
        linear algebra, this is actually U * S.
    """
    # set up a matrix you'll return
    M_reduced = None
    print(f"Running Truncated SVD over {M.shape[0]} words")
    np.set_printoptions(precision=3, suppress=True)

    # TODO: call TruncatedSVD with k components and the given number of iterations, 
    # as this will perform a singular value decomposition of the matrix and reduce its dimensionality
    svd = TruncatedSVD(n_components=k, n_iter=iterations)


    # TODO: then call fit_transform to have it reduce the shape properly
    M_reduced = svd.fit_transform(M)

    # now print out the work here
    print(f'reduced shape: {M_reduced.shape}')
    print(f'matrix:\n {M_reduced}')

    return M_reduced


def plot_embeddings(M_reduced : np.ndarray[np.float64], word_indices : dict[str, int], vocab : list[str], filename: str) -> None:
    """
    Scatter plot the embeddings on a 2D graph of the embeddings of the
    words specified in "words". Be sure to label each point.
    """
    for word in vocab:
        x = M_reduced[word_indices[word]][0]
        y = M_reduced[word_indices[word]][1]
        plot.scatter(x, y, marker='.', color='red')
        plot.text(x, y, word, fontsize=9)

    plot.savefig(filename)
    plot.close()

def main():
    # set up the figure size for plotting
    plot.rcParams['figure.figsize'] = [10, 5]

    # download 'reuters' dataset if you don't have it
    # nltk.data.path = ['.'].append(nltk.data.path)
    # nltk.download('reuters')

    # TODO: Uncomment the following as you complete each step 
    # Step 1: read the corpus
    corpus = read_reuters_corpus(category="gold", debug=True)

    # Step 2: then get the vocabular
    vocab = get_vocabulary(corpus)
    # print(vocab[:20])

    # Step 3: get the vocabular size
    vocab_size = len(vocab)

    # Step 4: get the vocabulary indices
    vocab_indices = create_indexed_vocabulary(vocab)

    # Step 5: get the co-occurrence matrix
    co_matrix = get_co_occurrence_matrix(corpus, vocab_indices, vocab_size)
    print(f'co-matrix: {co_matrix}')

    # Step 6: now reduce the matrix so we can plot it
    co_matrix_reduced = reduce_to_k_dim(co_matrix)

    
    # TODO: uncomment the following for a simple test plot
    # print ("-" * 80)
    # test_plotname = 'test-plot.png'
    # print (f'Outputted Plot...{test_plotname}')
    # M_reduced_plot_test = np.array([[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 0]])
    # word2ind_plot_test = {'test1': 0, 'test2': 1, 'test3': 2, 'test4': 3, 'test5': 4}
    # words = ['test1', 'test2', 'test3', 'test4', 'test5']
    # plot_embeddings(M_reduced_plot_test, word2ind_plot_test, words, test_plotname)

    # TODO: now test the result of all of this work with a subset of words!
    # TODO: Step 7
    print ("-" * 80)
    M_lengths = np.linalg.norm(co_matrix_reduced, axis=1)
    # this uses broadcasting from numpy to create a new matrix
    normalized_mat = co_matrix_reduced / M_lengths[:, np.newaxis]
    words = ['value', 'gold', 'platinum', 'reserves', 'silver', 'metals', 'copper', "trade"]
    plot_embeddings(normalized_mat, vocab_indices, words, 'sample_plot.png')
    
if __name__ == '__main__':
    main()