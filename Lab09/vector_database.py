import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import json
import os
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Setup--this will create a file in './chroma' that stores the data
chroma_client = chromadb.PersistentClient()

# Also, set up your OpenAI client
ai_client = OpenAI()

# set up embedding function before creating the collection
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key = ai_client.api_key,
                                                        model_name = "text-embedding-3-small",
                                                        dimensions = 512)
JSON_FILE = "/Users/norawestol/Documents/school/topics/Lab09/courses.JSON"
COLLECTION_NAME = "cs_courses"

def load_courses(filepath: str):

    """
    Loads course info from json file.
    """

    with open(filepath, "r") as f:
        courses = json.load(f)

    print(f"Loaded {len(courses)} course records from '{filepath}'")
    return courses

def create_collection(courses: list[dict]):

    """
    Makes ChromaDB collection with memory, course description as documents, +
    stores everything else as metadata. Returns the completed collection.
    """

    chroma_client = chromadb.Client()
 
    ef = embedding_functions.DefaultEmbeddingFunction()
 
    collection = chroma_client.create_collection( name = COLLECTION_NAME, embedding_function = ef)
 
    # Makes 3 fields for ChromaDB
    ids = [course["id"] for course in courses]
    documents = [course["description"] for course in courses]
    metadatas = [{
            "title":         course["title"],
            "prerequisites": course["prerequisites"],
            "credits":       course["credits"],
            "level":         course["level"], }
        for course in courses
    ]
 
    collection.add( ids = ids, documents = documents, metadatas = metadatas, )
 
    print(f"Collection '{COLLECTION_NAME}' created with {collection.count()} documents.\n")
    return collection

def print_results(query: str, results: dict):
    """
    Prints formatted results.
    """
    print(f"\nQUERY: {query}")
    for doc_id, meta in zip(results["ids"][0], results["metadatas"][0]):
        print(f"  - {doc_id}: {meta['title']} ({meta['level']})")
    print()

def run_searches(collection: chromadb.Collection):

    """
    Runs 5 searches in file. Returns subsets of data for each search to test results.
    """
 
    # Search 1:
    # Expected top results: CS2350 (Computer Organization), CS3100 (OS)
    q1 = "How do computers work at the hardware level?"
    r1 = collection.query(query_texts=[q1], n_results=3)
    print_results(q1, r1)
 
    # Search 2:
    # Expected top results: CS4200 (AI), CS4210 (ML), CS4220 (NLP)
    q2 = "Building intelligent agents that can reason and make decisions."
    r2 = collection.query(query_texts=[q2], n_results=3)
    print_results(q2, r2)
 
    # Search 3:
    # Expected top results: CS4400 (Cybersecurity), CS3600 (Networks)
    q3 = "Protecting systems from hackers and network attacks."
    r3 = collection.query(query_texts=[q3], n_results=3)
    print_results(q3, r3)
 
    # Search 4:
    # Expected top results: CS4220 (NLP), CS4200 (AI), CS4210 (ML)
    q4 = "Processing and understanding human language and text."
    r4 = collection.query(query_texts=[q4], n_results=3)
    print_results(q4, r4)
 
    # Search 5: Testing Metadata
    # Expected: only CS1010, CS1310, CS1410 can appear
    q5 = "Learning to write programs for the first time."
    r5 = collection.query(
        query_texts = [q5],
        n_results = 3,
        where = {"level": {"$eq": "introductory"}}   # metadata filter
    )
    print("(filter for introductory)")
    print_results(q5, r5)

def main():

    print("CS COURSE VECTOR SEARCH") 
    print()
    courses = load_courses(JSON_FILE)
    collection = create_collection(courses)
    run_searches(collection)

if __name__ == "__main__":
    main()