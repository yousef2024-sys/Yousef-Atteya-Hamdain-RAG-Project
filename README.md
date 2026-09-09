# StudyMate RAG Assistant

StudyMate is a grounded study assistant for Python, FastAPI, retrieval, evaluation, and project delivery. It retrieves relevant passages from a curated learning library, returns a concise answer with citations, and exposes the retrieval metadata so the full RAG flow is visible during a demo.

## What is included

- `notebooks/rag_pipeline.ipynb` — load, inspect, section-chunk, embed, persist, retrieve, and evaluate the corpus.
- `data/documents/` — six source documents covering 18 sections.
- `data/vector_store/` — persisted-index manifest and generated index location.
- `backend/` — a standalone FastAPI implementation of `/health` and `/query` with pytest coverage, matching the graduation guide's expected backend shape.
- `artifacts/api-server/` — Express API runtime with the generated OpenAPI contract, retrieval service, health check, library endpoint, stats endpoint, and grounded query endpoint.
- `artifacts/studymate/` — React + Vite chat application with library and about routes.
- `lib/api-spec/openapi.yaml` — source of truth for API request and response contracts.

The project uses a local TF-IDF retriever and an extractive answerer by default so it runs without an external key or a running model server. The response contract is ready for a local Ollama generation step: set the generation implementation behind the same `QueryResponse` shape when Ollama is available.

## Run the app

Prerequisites: Node.js 20+, pnpm, and Python 3.10+ for the notebook.

```bash
pnpm install
pnpm --filter @workspace/api-spec run codegen
```

Start the two managed services from the Replit workflow panel:

- API server: `/api/healthz`, `/api/query`, `/api/library`, `/api/stats`
- StudyMate web app: `/`

The web app calls the API through the proxied `/api` path and does not hard-code a localhost URL.

To run the assignment-shaped FastAPI backend locally instead:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

Its Swagger UI is available at `http://localhost:8000/docs`, and the tests run with:

```bash
PYTHONPATH=backend pytest -q backend/tests
```

## Regenerate and evaluate the index

Run `notebooks/rag_pipeline.ipynb` from the repository root. It writes:

- `data/vector_store/index.json`
- `data/vector_store/manifest.json`
- `data/vector_store/evaluation.json`

The notebook is dependency-light and uses a deterministic TF-IDF baseline. This keeps the evaluation reproducible and makes the retrieval behavior easy to explain. A production embedding model can replace the `embed` function while keeping the chunk metadata and citation fields unchanged.

## API examples

Health:

```bash
curl /api/healthz
```

Ask a question:

```bash
curl -X POST /api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Why should expensive resources load during application lifespan?","top_k":3}'
```

The response contains `answer`, `sources`, `related_questions`, and `retrieval`. The `grounded` flag is false when no relevant source passes the retrieval threshold, and the assistant explains that it does not have enough evidence instead of inventing an answer.

## Evaluation notes

The notebook evaluates ten questions: direct facts, comparisons, workflows, and one out-of-scope question. The score tracks whether the expected source appears in the top three results and whether the out-of-scope question correctly follows the insufficient-evidence path. The runtime stats expose the resulting score as a UI-ready value.

## Project structure

```text
data/
  documents/              # curated source corpus
  vector_store/           # persisted index and evaluation artifacts
notebooks/
  rag_pipeline.ipynb      # reproducible RAG pipeline
artifacts/
  api-server/             # API and retrieval runtime
  studymate/              # React web client
backend/
  app/                    # FastAPI reference backend required by the guide
  tests/                  # pytest health, happy-path, and validation tests
lib/
  api-spec/               # OpenAPI source of truth
  api-client-react/       # generated React Query hooks
  api-zod/                # generated Zod schemas
```

## Environment and Git hygiene

Copy `.env.example` to `.env` only when adding local configuration. Never commit `.env`, model credentials, virtual environments, Python caches, logs, or large generated indexes. The sample corpus is intentionally small and safe to inspect; larger corpora should stay outside Git and be regenerated from the notebook.
