# StudyMate source library

This small, curated corpus is the source of truth for the demo assistant. It is intentionally narrow so retrieval behavior is easy to inspect during a presentation. The notebook reads the Markdown files, creates section-aware chunks, builds a local TF-IDF vector index, and writes the persisted index to `data/vector_store/`.

The runtime API includes the same curated chunks in its bundle so the preview works immediately. Running the notebook is still the canonical way to regenerate and evaluate the index.
