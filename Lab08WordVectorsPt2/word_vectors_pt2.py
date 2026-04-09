from gensim.models import KeyedVectors
from gensim.test.utils import datapath

import gensim.downloader as api
# load a bigger embedded model 
def load_embedding_model() -> KeyedVectors:
    """ Load GloVe Vectors
        Return:
            wv_from_bin: All 400000 embeddings, each lengh 200
    """
    wv_from_bin = api.load("glove-wiki-gigaword-200")
    print("Loaded vocab size %i" % len(list(wv_from_bin.index_to_key)))
    return wv_from_bin

def print_synonyms_and_antonyms(wv: KeyedVectors, w1: str, w2: str, w3: str) -> None:
    """
    Find 3 words such that w1 and w2 are synonyms and w1 and w3 are antonyms, but
    where the cosine difference is closer between w1 and w3 than w1 and w2.

    Print the cosine difference, which is 1 - cosine similarity between w1 and w2
    and w1 and w3. This is what the distance function of wv will give you. 

    Parameters:
    wv: word vectors loaded in your main function
    w1: a word
    w2: a synonym to w1
    w3: an antonym to w1
    """
    print(f'cosine distance between {w1} and {w2} = {wv.distance(w1, w2)}')
    print(f'cosine distance between {w1} and {w3} = {wv.distance(w1, w3)}')
    

def print_analogies(wv: KeyedVectors, w1: str, w2: str, w3: str) -> str:
    """
    Word vectors _sometimes_ show the ability to recognize analogies. This works
    by finding a word such that w1 and w2 are similar and then finding the word
    from that relation that is most similar to w3. How does this work? We can
    use the most_similar function and pass w1 and w2 as the parameter 'positive'
    and w3 and the parameter 'negative'.

    Call this function and print out the analogy of something else that makes sense.
    """
    word = wv.most_similar(positive=[w1, w2], negative=[w3])
    print(f"{w1}: {w2} :: {w3} : x = {wv.most_similar(positive=[w1, w2], negative=[w3])}") 

def main():
    """
    The main point of entry into our program. Run our code from here.
    """
    # load the embeddings--first check if it's been stored already locally
    wv = None

    try:
        print('checking word vector cache and loading...', end='')
        wv = KeyedVectors.load('glove_wvs.bin')
    except:
        print('cache not found, downloading word vectors...', end='')
        # and if it hasn't, load it
        if wv == None:
            wv = load_embedding_model()
            print(f'wv type: {type(wv)}')
            wv.save('glove_wvs.bin')
    print('done')

    # we can use the most_similar function to see which words are most similar to the one we give it
    print(f'find the most similar word to "over" in our word vectors:\n {wv.most_similar("over")}')

    print('Q1:')
    # Q1: complete the print_synonyms_and_antonyms function by passing in
    # your word vectors and 3 words such that w1 and w2 are synonyms 
    # while w1 and w3 are antonyms, but where the cosine distance between w1 and w3
    # is closer than the distance between w1 and w2
    print_synonyms_and_antonyms(wv, 'mother', 'maternal', 'father')

    print('Q2:')
    # Q2: complete the print_analogies function by passing in your word vectors
    # and your three words, and returning the result. Here's an example, but please note,
    # this is not a commentary on genders or gender identities or gender roles, etc (but we'll
    # go into more detail on this later). 
    #
    # The notation reads "man is to grandfather as woman is to x", and you're supposed to 
    # figure out what "x" is. 
    # print(f"man : grandfather :: woman : x = {wv.most_similar(positive=['woman', 'grandfather'], negative=['man'])}")

    # a) Explain what math might be going on to figure out the most similar word vectors. Giving
    # the letters x : y as w : z to our words and using only + and -, explain how we're finding analogies

    # We know that x,y, and w are all vectors, so we can treat them as we would points in a space. The computer first finds
    # the vector difference (y-x), which gives us the relationship of both magnitude and direction between x and y 
    # It then adds the vector to w, which is how we get point z. The computer finds whatever word has the closest vector
    # to z which gives us our analogous answer.
    
    # b) In addition, it's clear that grandmother is the solution here, but what is an intuitive reason for
    # why other close answers are granddaughter, daughter, or mother, or even father.
    # We can intuit that these words have a similar vector to that of grandmother, likely because they are all
    # related to the concept of family and have similar contexts in which they are used.
    
    # c) now call your print_analogies function with three words where the top result is the 'right' answer
    print_analogies(wv, 'mother', 'maternal', 'father')
    
    # Note that the following analogy doesn't work: 
    print(f" hand : glove :: foot : x = {wv.most_similar(positive=['foot', 'glove'], negative=['hand'])}")

    # d) Explain why this analogy doesn't work? what is it about the words being used?

    # In this instance, the "foot" parameter has the potential to mean many things, so the word vector doe not know to relate it to glove in 
    # the way that we want it to. The fact that it could be a measurement or a body part gives a much wider array of options for the
    # computer to return, and thus it might not return the answer we were looking for (depending on the input).

    # e) Find another analogy which fails like this
    print(f" peasant : poor :: ruler : x = {wv.most_similar(positive=['ruler', 'poor'], negative=['peasant'])}")


    print('Q3: ')
    # Q3: It's really important to recognize that when we train machine learning on human generated data,
    # that data is _going_ to be biased, e.g., gender, race, sexual orientation, and any number of other areas.
    # Please be aware that you will see this whenever working with text data and a huge amount of research is
    # being done to try to remove biases like these in NLP and LLMs in particular.
    print(f" woman : profession :: man : x = {wv.most_similar(positive=['man', 'profession'], negative=['woman'])})") # Line 1
    print()
    print(f" man : profession :: woman : x = {wv.most_similar(positive=['woman', 'profession'], negative=['man'])})") # Line 2
    print()

    # a) How are these two lists reflecting biases. Point out the differences and what they're implying. 
    # The difference in what the code returns differs depending on if it was correlated to a man or woman. While Line 1 
    # showed things such as "skill", "business", "work", "respected", Line 2 returns words such as "nursing", "teaching", 
    # "educator" which are traditionally percieved to be feminine-associated professions. This shows us the bias that exists 
    # in the data that these word vectors were trained on.
    
    # b) Using this same function to find analogies, find another example that exhibits biases from its word vectors.\

    # If you're using anything personal in your examples, such as your gender or race, please be careful, the results
    # may be very painful. 
    print(f" woman : hobbies :: man : x = {wv.most_similar(positive=['man', 'hobbies'], negative=['woman'])})") # Line 3
    print()
    print(f" man : hobbies :: woman : x = {wv.most_similar(positive=['woman', 'hobbies'], negative=['man'])})") # Line 4
    
    # c) After part b, how do you think bias is getting into these word vectors or may be inherent in LLMs/

    # We know that the corpus the code is referencing was made up of things written by humans. Bias exists in all of us, so even within such
    # a large corpus such as this one, bias can still be found (as we see with answers like "needlework" or "sunbathing" in Line 4).

if __name__ == '__main__':
    main()