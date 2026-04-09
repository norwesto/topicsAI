
import unittest
import numpy as np

# now import the testing file
import word_vectors as w

# build a test case for testing word vectors
class TestVocab(unittest.TestCase):
    def setUp(self):
        self.corpus = w.read_reuters_corpus()
        # self.vocab = w.get_vocabulary(self.corpus)
        # self.vocab_size = len(self.vocab)
        # self.vocab_indices = w.create_indexed_vocabulary(self.vocab)
        # self.co_matrix = w.get_co_occurrence_matrix(self.corpus, self.vocab_indices, self.vocab_size)

    def test_read_reuters(self):
        self.assertEqual(self.corpus[0][2], 'mining')
        self.assertEqual(self.corpus[10][5], 'hallmarked')
        self.assertEqual(self.corpus[25][3], 'margins')

    def test_vocab(self):
        self.assertEqual(self.vocab[1024], 'economies')
        self.assertEqual(len(self.vocab), 2830, 'check that size of vocab is okay')
        
    def test_vocab_indices(self):
        self.assertEqual(self.vocab_indices['economies'], 1024)
        self.assertEqual(self.vocab_indices['play'], 2017)
        self.assertEqual(self.vocab_indices['42'], 190)
        
    def test_co_matrix(self):
        """
        test the co-occurrence matrix
        """
        # idx = 0
        # for word in self.co_matrix[self.vocab_indices['mine']]:
        #     if word != 0.0:
        #         print(f'{idx}: {word}')
        #     idx += 1
        #self.assertEqual(self.co_matrix.shape, (self.vocab_size, self.vocab_size), 'matrix dimensions mismatch')
        #self.assertAlmostEqual(self.co_matrix[self.vocab_indices['gold']][2790], 17.0, 'incorrect count for word "gold"')
        #self.assertAlmostEqual(self.co_matrix[self.vocab_indices['mine']][2605], 30.0, 'incorrect count for word "mine"')

    def test_short_case(self):
        test_corpus = [f"{w.START_TOKEN} All that glitters isn't gold {w.END_TOKEN}".split(' '),
                       f"{w.START_TOKEN} All's well that ends well {w.END_TOKEN}".split(' ')]
        
        vocab = w.get_vocabulary(test_corpus)
        test_vocab = sorted([w.START_TOKEN, w.END_TOKEN, 'All', 'ends', 'that', 'gold', "All's", 'glitters', "isn't", 'well'])
        self.assertEqual(vocab, test_vocab, 'vocabulary mismatch')
        print(f'test_vocab: {test_vocab}')

        vocab_size = len(vocab)
        test_size = len(test_vocab)
        self.assertEqual(vocab_size, test_size, 'vocabular size mismatch, these should be equal')

        vocab_indices = w.create_indexed_vocabulary(vocab)
        # note we test with a window size of 1
        M_test = w.get_co_occurrence_matrix(test_corpus, vocab_indices, vocab_size, 1)
        print(f'vocab_indices: {vocab_indices}')

        M_test_ans = np.array( 
            [[0., 0., 0., 0., 0., 0., 1., 0., 0., 1.,],
            [0., 0., 1., 1., 0., 0., 0., 0., 0., 0.,],
            [0., 1., 0., 0., 0., 0., 0., 0., 1., 0.,],
            [0., 1., 0., 0., 0., 0., 0., 0., 0., 1.,],
            [0., 0., 0., 0., 0., 0., 0., 0., 1., 1.,],
            [0., 0., 0., 0., 0., 0., 0., 1., 1., 0.,],
            [1., 0., 0., 0., 0., 0., 0., 1., 0., 0.,],
            [0., 0., 0., 0., 0., 1., 1., 0., 0., 0.,],
            [0., 0., 1., 0., 1., 1., 0., 0., 0., 1.,],
            [1., 0., 0., 1., 1., 0., 0., 0., 1., 0.,]]
        )

        print(f'M_test: \n{M_test}\nM_test_ans:\n{M_test_ans}')

        self.assertIsNone(np.testing.assert_allclose(M_test, M_test_ans), 'the matrices do not match')

def suite():
    # create a test suite
    suite = unittest.TestSuite()
    # add individual tests
    #suite.addTest(TestVocab('test_read_reuters'))
    #suite.addTest(TestVocab('test_vocab'))
    #suite.addTest(TestVocab('test_vocab_indices'))
    #suite.addTest(TestVocab('test_co_matrix'))
    suite.addTest(TestVocab('test_short_case'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())