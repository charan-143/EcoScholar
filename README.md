# EcoScholar

EcoScholar is a sustainability learning platform built with Next.js, FastAPI, PostgreSQL and scikit-learn. It includes learning modules, quizzes, JWT accounts, role-based access control, hybrid retrieval, optional LLM synthesis, environmental dataset discovery and offline retrieval evaluation.

## Capabilities
- Four learning modules: climate, clean energy, biodiversity and circular economy.
- Quiz scoring and learner-specific progress when signed in.
- Email/password accounts with Argon2 hashing and 12-hour signed JWTs.
- Learner, educator and admin roles. Public registration always creates a learner; only admins can change roles.
- Hybrid retrieval combining TF-IDF and BM25 with reciprocal-rank fusion.
- Optional server-side OpenAI LLM synthesis with source-label validation and evidence-only fallback.
- Curated primary-source references: IPCC, UNEP, IEA, IPBES, FAO, World Bank and Our World in Data.
- Dataset catalogue for emissions, electricity mix, primary energy, forests, freshwater and protected areas.
- Personalized learning recommendations based on interests and recent quiz mastery.
- Offline Recall@k, MRR and nDCG evaluation plus local retrieval latency benchmarking.

## Local setup
1. Copy .env.example to .env and set a high-entropy JWT_SECRET_KEY.
2. Run docker compose up --build.
3. Frontend: http://localhost:3000; API docs: http://localhost:8000/docs.
4. Apply schema: DATABASE_URL=postgresql+psycopg://... alembic upgrade head.
5. Seed courses: PYTHONPATH=backend python backend/scripts/seed_courses.py.
6. Backend tests: PYTHONPATH=backend pytest -q backend/tests.
5. Retrieval quality: PYTHONPATH=backend python backend/evaluation/metrics.py.
6. Local latency: PYTHONPATH=backend python backend/evaluation/benchmark.py.
7. Frontend tests: cd frontend && npm test.

## Bootstrap the first administrator
Run this from a trusted local shell after configuring DATABASE_URL: python backend/scripts/create_admin.py --email admin@example.org. The script prompts for a password and promotes an existing account or creates the first admin. Do not expose the admin password in source control or CI logs.

## API
- POST /api/auth/register and POST /api/auth/login.
- GET /api/auth/me; GET /api/auth/users and PATCH /api/auth/users/{id}/role require admin.
- GET /api/recommendations/me?interests=climate,biodiversity requires a bearer token.
- GET /api/health, /api/courses, /api/sources, /api/datasets; GET /api/datasets/{dataset_id}/preview?limit=10 fetches a bounded live sample from an allowlisted provider.
- POST /api/assistant/ask.
- GET /api/quizzes/{course_slug}; POST /api/quizzes/submit; GET /api/progress.
- POST /api/footprint/estimate.

## Retrieval evaluation and measured metrics
The fixed, hand-labelled query set is backend/evaluation/rag_queries.json. CI currently reports Recall@5 = 0.9375, MRR = 0.7812 and nDCG@5 = 0.8061 over 8 queries for the hybrid retriever. These are reproducible offline ranking metrics on a small benchmark, not production user outcomes. The CI benchmark also measured 80 in-process retrieval calls on a GitHub Actions runner: median 2.490 ms, p95 2.592 ms and mean 2.519 ms in the recorded run. These are runner-specific and exclude network, database and LLM time.

## Environmental data provenance
backend/app/data/environmental_sources.json records publishers and reports. backend/app/data/environmental_datasets.json lists eight environmental indicators with source pages, CSV/API download endpoints, units, coverage and interpretation caveats. It is a discovery registry: raw datasets are not downloaded, cached or normalized into the application database yet. Before publishing analyses, fetch the underlying data, pin a version/date, retain source metadata and validate indicator definitions and licenses.

## Deployment
The public GitHub repository is configured for separate Vercel projects:
- Frontend root: frontend; set NEXT_PUBLIC_API_URL to the API origin.
- API root: backend; set DATABASE_URL, JWT_SECRET_KEY, API_ALLOWED_ORIGINS and optionally OPENAI_API_KEY / OPENAI_MODEL.
- Use a managed PostgreSQL database and allow the frontend production origin in API_ALLOWED_ORIGINS. Run alembic upgrade head and the course seed script once against the production DATABASE_URL before enabling traffic.
- GitHub Actions runs backend compilation, backend tests, retrieval metrics, latency benchmarking, frontend smoke tests and a Next.js production build.

## Security and limitations
- Frontend sign-in is implemented; the current browser stores the bearer token in localStorage. For production, move to secure HttpOnly SameSite cookies and add CSRF protection.
- Email verification, password reset, refresh-token rotation, rate limiting, audit logs, account deletion and abuse monitoring remain to be implemented.
- The existing demo learning flow remains usable without signing in; authenticated quiz submissions are associated with the learner.
- Database schema creation still uses create_all; introduce Alembic migrations and connection-pool tuning before production.
- The LLM is optional until an OPENAI_API_KEY is configured. Provider failure or invalid citation labels cause evidence-only fallback.
- The footprint estimator uses illustrative constants, not localized authoritative emission factors.
- Environmental dataset links are registered, not yet ingested or independently quality-checked.

## License
MIT
