# EcoScholar

EcoScholar is a full-stack sustainability learning prototype built with Next.js, FastAPI, PostgreSQL and scikit-learn. It combines learning modules, quiz scoring, learner progress, a transparent TF-IDF retrieval baseline and an illustrative carbon-footprint estimator.

## Features
- Four seeded modules: climate, clean energy, biodiversity and circular economy.
- Knowledge checks with server-side scoring and persisted quiz attempts.
- Progress summary endpoint.
- TF-IDF + cosine-similarity retrieval over an inspectable starter knowledge corpus.
- Topic recommendations using the same retrieval baseline.
- Carbon-footprint screening calculator with explicit placeholder-factor warnings.
- Docker Compose development environment.

## Architecture
```text
Next.js frontend -> FastAPI REST API -> PostgreSQL
                         |
                  scikit-learn TF-IDF
```

## Run locally
1. Install Docker Desktop / Docker Engine with Compose.
2. Copy `.env.example` to `.env`.
3. Run `docker compose up --build`.
4. Open http://localhost:3000 and API docs at http://localhost:8000/docs.

Frontend-only: `cd frontend && npm install && npm run dev`.
Backend-only: create a Python virtual environment, install `backend/requirements.txt`, then run `uvicorn app.main:app --reload --app-dir backend` from the repository root.

## API
- `GET /api/health`
- `GET /api/courses`
- `GET /api/recommendations?topic=climate`
- `POST /api/assistant/ask` — body: `{"question":"How does climate mitigation work?"}`
- `GET /api/quizzes/{course_slug}`
- `POST /api/quizzes/submit` — body: `{"course_slug":"climate-basics","answers":[1,0,2]}`
- `GET /api/progress`
- `POST /api/footprint/estimate`

## AI/ML approach
The assistant is a retrieval baseline, not a generative model. TF-IDF vectorization with unigram/bigram features ranks passages by cosine similarity. Retrieved excerpts and source notes are returned to the UI for inspection. This is a reproducible baseline for future comparison with embeddings, hybrid retrieval, reranking and citation-checked generation.

## Limitations and responsible use
- The knowledge corpus is a small editorial starter set. Source notes identify materials that must be verified; this is not a fully sourced environmental reference library.
- Footprint factors are illustrative placeholders, not region-specific verified emission factors or a formal greenhouse-gas inventory.
- Demo learner identity is static; authentication, authorization and per-user privacy controls are not implemented.
- Database schema creation is automatic for this MVP; add Alembic migrations before production.
- Automated test coverage, retrieval evaluation, rate limiting, observability and deployment hardening remain future work.
- Frontend production build was not verified as part of this publication.

## Roadmap
1. Add reviewed source ingestion with provenance, dates and licensing.
2. Build retrieval evaluation sets and compare TF-IDF, dense and hybrid retrieval.
3. Add authentication, learner profiles and privacy controls.
4. Replace placeholder carbon factors with localized authoritative datasets and uncertainty ranges.
5. Add migrations, automated tests, monitoring and deployment pipelines.

## License
MIT
