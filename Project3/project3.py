import json
import re
import tiktoken
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions as embedding_functions
import streamlit as st

SYSTEM_PROMPT = """
You are a knowledgeable assistant that answers questions about the 
American Revolution and the American Revolutionary War. You answer ONLY using the 
context provided. If the context does not contain enough information to answer, say so.
Do not answer questions unrelated to the American Revolution or American Revolutionary War.
Be concise and cite the sources provided in the context.
"""

DOCUMENTS = [
    {
        "type": "txt",
        "filepath": "/Users/norawestol/Documents/school/topics/Project3/bostonTeaParty.txt",
        "title": "American Revolution",
        "source_url": "https://www.bostonteapartyship.com/american-revolution",
    },
    {
        "type": "txt",
        "filepath": "/Users/norawestol/Documents/school/topics/Project3/americanBattelfieldTrust.txt",
        "title": "Overview of the American Revolutionary War",
        "source_url": "https://www.battlefields.org/learn/articles/overview-american-revolutionary-war",
    },
    {
        "type": "txt",
        "filepath": "/Users/norawestol/Documents/school/topics/Project3/historyDOTcom.txt",
        "title": "Overview of the American Revolutionary War",
        "source_url": "https://www.history.com/articles/american-revolution-history",
    },
]

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str):
    """
    Returns the number of tokens in a string using the cl100k_base tokenizer.
    """

    return len(enc.encode(text))

MAX_TOKENS = 600
OVERLAP_TOKENS = 100

def split_into_sentences(text: str):
    """
    Sentence splitter that preserves whitespace.
    Returns: Formatted sentence
    """

    return re.split(r'(?<=[.!?])\s+', text.strip())

def sub_chunk(section_title: str, section_text: str, doc_title: str, source_url: str):
    """
    Splits section's text into overlapping chunks when exceeds MAX_TOKENS.
    Returns: List of sub-chunk dicts with id, text, and metadata
    """

    sentences = split_into_sentences(section_text)
    chunks = []
    chunk_sentences = []
    current_tokens = 0
    chunk_index = 0

    for sentence in sentences:
        s_tokens = count_tokens(sentence)

        if current_tokens + s_tokens > MAX_TOKENS and chunk_sentences:
            chunk_text = " ".join(chunk_sentences)
            chunks.append({
                "id": f"{doc_title}::{section_title}::{chunk_index}",
                "text": chunk_text,
                "metadata": {
                    "doc_title": doc_title,
                    "section": section_title,
                    "chunk_index": chunk_index,
                    "source": source_url,
                    "token_count": count_tokens(chunk_text),
                },
            })
            chunk_index += 1

            overlap_sentences = []
            overlap_tokens = 0
            for s in reversed(chunk_sentences):
                t = count_tokens(s)
                if overlap_tokens + t <= OVERLAP_TOKENS:
                    overlap_sentences.insert(0, s)
                    overlap_tokens += t
                else:
                    break
            chunk_sentences = overlap_sentences
            current_tokens = overlap_tokens

        chunk_sentences.append(sentence)
        current_tokens += s_tokens

    if chunk_sentences:
        chunk_text = " ".join(chunk_sentences)
        chunks.append({
            "id": f"{doc_title}::{section_title}::{chunk_index}",
            "text": chunk_text,
            "metadata": {
                "doc_title": doc_title,
                "section": section_title,
                "chunk_index": chunk_index,
                "source": source_url,
                "token_count": count_tokens(chunk_text),
            },
        })
    return chunks

def chunk_sections(sections: list[dict], doc_title: str, source_url: str):
    """
    Converts a list of sections into ChromaDB chunks. Sections in
    MAX_TOKENS kept as a single chunk and larger sections are split using
    sub_chunk with overlap.
    Returns: List of chunk dicts with id, text, and metadata
    """

    all_chunks = []
    for sec in sections:
        heading = sec["heading"]
        text = sec["text"].strip()
        if not text:
            continue

        if count_tokens(text) <= MAX_TOKENS:
            all_chunks.append({
                "id": f"{doc_title}::{heading}::0",
                "text": text,
                "metadata": {
                    "doc_title": doc_title,
                    "section": heading,
                    "chunk_index": 0,
                    "source": source_url,
                    "token_count": count_tokens(text),
                },
            })
        else:
            all_chunks.extend(sub_chunk(heading, text, doc_title, source_url))

    return all_chunks

def load_txt_file(filepath: str, doc_title: str, source_url: str = ""):
    """
    Loads a plain-text file and chunks it. Lines starting with '#' treated as section 
    headers.
    Returns: All chunk sections
    """

    print(f"Loading file: {filepath}")
    with open(filepath, "r", encoding = "utf-8") as f:
        content = f.read()

    sections = []
    current_heading = doc_title
    current_text_parts = []

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_text_parts:
                sections.append({
                    "heading": current_heading,
                    "text": " ".join(current_text_parts),
                })
            current_heading = stripped.lstrip("#").strip()
            current_text_parts = []
        elif stripped:
            current_text_parts.append(stripped)

    if current_text_parts:
        sections.append({
            "heading": current_heading,
            "text": " ".join(current_text_parts)
        })

    if not sections:
        sections = [{"heading": doc_title, "text": content}]

    return chunk_sections(sections, doc_title, source_url or filepath)

def build_chunks():
    """
    Iterates over all documents in DOCUMENTS, loads and chunks
    each one, returns a list of all chunks.

    Returns: List of all chunk dicts across all documents
    """

    all_chunks = []
    for doc in DOCUMENTS:
        print(f"\nProcessing: {doc['title']}")
        if doc["type"] == "txt":
            chunks = load_txt_file(
                doc["filepath"],
                doc["title"],
                source_url = doc.get("source_url", "")
            )
        else:
            print(f"Unknown type: {doc['type']}, skipping.")
            continue

        print(f"{len(chunks)} chunks created")
        all_chunks.extend(chunks)

    return all_chunks

def add_content_to_collection():
    """
    Builds chunks from documents and adds them to ChromaDB collection.
    """

    print("Building document chunks")
    chunks = build_chunks()

    if not chunks:
        print("No chunks to add.")
        return

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    print(f"Adding {len(chunks)} chunks to collection...")
    collection.add(
        ids = ids,
        documents = documents,
        metadatas = metadatas
    )
    print(f"Done! {len(chunks)} chunks added to collection.")

@st.cache_resource
def init_clients():
    ai_client = OpenAI()
    chroma_client = chromadb.PersistentClient(path = ".chroma_persistent_db")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key = ai_client.api_key,
        model_name = "text-embedding-3-small",
        dimensions = 512,
    )
    try:
        collection = chroma_client.get_collection(
            name = "my_document_collection", embedding_function = openai_ef
        )
    except Exception:
        collection = chroma_client.create_collection(
            name = "my_document_collection", embedding_function = openai_ef
        )
        add_content_to_collection()
    return ai_client, collection
 
def is_safe_query(query: str, ai_client: OpenAI):
    """
    Uses gpt-4o-mini to check if the query is safe/on-topic
    Returns: is_safe, reason
    """
    check_response = ai_client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a content safety filter. Determine whether the following user query is: "
                    "1: safe (no harmful, offensive, or dangerous content), and "
                    "2: related to the American Revolution or American Revolutionary War. "
                    "Reply with ONLY valid JSON in this format: "
                    '{"safe": true/false, "on_topic": true/false, "reason": "short explanation"}'
                ),
            },
            {"role": "user", "content": query},
        ],
        max_tokens = 100,
    )
    raw = check_response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
        allowed = result.get("safe", False) and result.get("on_topic", False)
        return allowed, result.get("reason", "")
    except json.JSONDecodeError:
        return False, "Could not evaluate query safety."
  
def query_rag(user_query: str, chat_history: list, ai_client: OpenAI, collection):
    """
    Gets relevant chunks, builds a new prompt with memory.
    Returns: answer, source_chunks
    """

    # retrieves top 4 relevant chunks
    results = collection.query(query_texts = [user_query], n_results = 4)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
 
    # builds context block
    context_parts = []
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        context_parts.append(
            f"[Source {i+1}: {meta['doc_title']} — {meta['section']}]\n{doc}"
        )
    context = "\n\n".join(context_parts)
 
    # builds messages with full memory + new user message
    new_user_message = (
        f"Context:\n{context}\n\n"
        f"Question: {user_query}"
    )
 
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": new_user_message})
 
    response = ai_client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
        max_tokens = 600,
    )
    answer = response.choices[0].message.content.strip()
 
    # returns source chunk metadata for display
    source_chunks = [
        {"text": doc, "meta": meta} for doc, meta in zip(docs, metas)
    ]
    return answer, source_chunks

# STREAMLIT UI
st.set_page_config( page_title = "American Revolution RAG", page_icon = "🇺🇸", layout = "wide")
# st.write("test")
st.title("American Revolution Q&A")
st.caption("Ask questions about the American Revolution and Revolutionary War.")
 
ai_client, collection = init_clients()
# st.write("Collection count:", collection.count())

# initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []     
if "display_messages" not in st.session_state:
    st.session_state.display_messages = [] 
 
# display previous messages
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("View source chunks"):
                for i, chunk in enumerate(msg["sources"]):
                    st.markdown(f"Source {i+1}: {chunk['meta']['doc_title']} — {chunk['meta']['section']}**")
                    st.markdown(f"> {chunk['text']}")
                    st.markdown(f"[Original source]({chunk['meta']['source']})")
                    if i < len(msg["sources"]) - 1:
                        st.divider()
 
# chat input
if user_input := st.chat_input("Ask a question about the American Revolution..."):
    # show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
 
    # safety check
    safe, reason = is_safe_query(user_input, ai_client)
    if not safe:
        refusal = (
            f"Sorry, I can't process that query. "
            f"This assistant only answers questions about the American Revolution and Revolutionary War. "
            f"({reason})"
        )
        with st.chat_message("assistant"):
            st.warning(refusal)
        st.session_state.display_messages.append({"role": "user", "content": user_input, "sources": None})
        st.session_state.display_messages.append({"role": "assistant", "content": refusal, "sources": None})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                answer, source_chunks = query_rag(
                    user_input, st.session_state.chat_history, ai_client, collection
                )
            st.markdown(answer)
            with st.expander("View source chunks"):
                for i, chunk in enumerate(source_chunks):
                    st.markdown(f"Source {i+1}: {chunk['meta']['doc_title']} — {chunk['meta']['section']}**")
                    st.markdown(f"> {chunk['text']}")
                    st.markdown(f"[Original source]({chunk['meta']['source']})")
                    if i < len(source_chunks) - 1:
                        st.divider()
 
        #  only store plain query/answer (not the full prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
 
        # update display log
        st.session_state.display_messages.append({"role": "user", "content": user_input, "sources": None})
        st.session_state.display_messages.append({"role": "assistant", "content": answer, "sources": source_chunks})

def main():
    """
    Builds document chunks from the DOCUMENTS registry, saves them to
    chunks.json, and prints a sample chunk for verification.
    """

    print("Building document chunks")
    chunks = build_chunks()

    output_path = "chunks.json"
    with open(output_path, "w", encoding = "utf-8") as f:
        json.dump(chunks, f, indent = 2, ensure_ascii = False)

    print(f"\nDone! {len(chunks)} total chunks saved to {output_path}")
    print("\nSample chunk:")
    if chunks:
        sample = chunks[0]
        print(f"ID: {sample['id']}")
        print(f"Section: {sample['metadata']['section']}")
        print(f"Tokens: {sample['metadata']['token_count']}")
        print(f"Text preview: {sample['text'][:200]}...")

if __name__ == "__main__":
    main()