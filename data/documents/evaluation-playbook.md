# Evaluation Playbook

## Question matrix

Build an evaluation matrix that includes direct fact questions, comparison questions, workflow questions, and one or two out-of-scope questions. For every row, record the expected source, retrieved source, answer quality, and whether the response made an unsupported claim. This makes failure analysis concrete.

## Failure analysis

Common failures include chunks that are too broad, synonyms that the retriever misses, and confident answers when no source is relevant. Mitigate them with better metadata, section-aware chunking, query expansion, a similarity threshold, and a clear insufficient-evidence response. Record the mitigation in the project report.

## Useful metrics

Track retrieval hit rate, citation precision, grounded answer rate, and average response latency. A high retrieval hit rate with low groundedness usually means the generation prompt is not strict enough. A low hit rate points to chunking, embeddings, or query formulation rather than the language model.
