# American Revolution RAG Pipeline
**Author:** Nora Westol
**Course:** Topics in AI
**Date:** June 2026
**Collaborators:** LEP Tutor (Catherine Tifft)

## What It Does
The American Revolution RAG Pipeline is a retrieval-augmented generation (RAG) system that lets you ask questions about the American Revolution. It chunks and embeds source documents using OpenAI, stores them in a persistent ChromaDB vector store, and answers questions using `gpt-4o-mini`. Queries are safety-checked before processing, answers are grounded in the retrieved source chunks, and the app remembers your conversation so you can ask follow-up questions.
 
## How To Use It
*command line version just makes chunks, use streamlit to engage*
 
Run the Streamlit UI:
 
    streamlit run project3.py
 
Examples of viable requests:
- "What caused the American Revolution?"
- "Who were the major figures in the Revolutionary War?"
- "What happened at the Boston Tea Party?"
- "Tell me more about that" (follow-up using memory)

## Limitations

Some chunks don't seem to be loaded entirely, bot will answer certain questions but not others.
