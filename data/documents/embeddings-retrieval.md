# Embeddings and Retrieval

## What embeddings represent

An embedding maps text into a numerical vector so semantically related passages can be compared in the same space. A vector store indexes those representations and returns nearest neighbors for a query. The embedding model and document preprocessing must stay consistent between indexing and retrieval.

## Similarity and top-k

Cosine similarity compares the angle between a query vector and a chunk vector, which makes it useful when text length varies. Top-k retrieval returns a small set of the highest-scoring chunks; increasing k can improve recall but also adds noise to the prompt. Scores should be logged so weak retrieval can be diagnosed.

## Evaluation

Evaluate retrieval separately from generation. For each test question, record whether a relevant source was retrieved, whether the final answer is supported by that source, and whether the response contains a useful citation. Ten carefully chosen questions reveal more than a single happy-path demo.
