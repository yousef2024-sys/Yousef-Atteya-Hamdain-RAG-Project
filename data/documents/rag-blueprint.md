# RAG System Blueprint

## The retrieval-augmented loop

A RAG system first retrieves the passages most relevant to a question and then gives those passages to a language model as context. The model is instructed to answer from the supplied context rather than relying on memory. The answer should expose citations so a reader can inspect the evidence.

## Chunking strategy

Chunking balances enough context for an answer with small enough passages for precise retrieval. Start with section-aware chunks of roughly 250 to 500 words and a small overlap when sentences cross boundaries. Keep document id, title, section, and page metadata attached to every chunk so citations survive the pipeline.

## Grounding and refusal

Grounding is more than adding context to a prompt: the system should measure retrieval quality, constrain the answer to retrieved passages, and say when the library does not contain enough evidence. Useful safeguards include a similarity threshold, source citations, a no-answer response, and evaluation questions that test for hallucinations.
