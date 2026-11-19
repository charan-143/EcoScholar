# EcoScholar

EcoScholar is a sustainability learning platform built with Next.js, FastAPI, PostgreSQL and scikit-learn. It includes learning modules, quizzes, JWT accounts, role-based access control, hybrid retrieval, optional LLM synthesis, authoritative-source metadata and offline retrieval evaluation.

## Capabilities
- Four learning modules: climate, clean energy, biodiversity and circular economy.
- Quiz scoring and progress tracking.
- Email/password registration and login with Argon2 password hashing and signed 12-hour JWTs.
- Learner, educator and admin roles. Self-registration always creates a learner; only admins can change roles.
- Hybrid retrieval combining TF-IDF similarity and lexical matching.
- Optional server-side OpenAI chat completion synthesis constrained to retrieved passages; retrieval-only fallback when no key is configured.
- Curated metadata linking to IPCC, UNEP, IEA, IPBES, FAO, World Bank and Our World in Data.
- Transparent personalized recommendations based on declared interests and recent quiz mastery.
- Offline Recall@k, MRR and nDCG evaluation.
- Illustrative footprint estimator (not a verified inventory).

## Local setup
1. Copy .env.example to .env and set a long random JWT_SECRET_KEY.
2. Run docker compose up --build.
3. Frontend: http://localhost:3000; API docs: http://localhost:8000/docs.
4. Backend tests: PYTHONPATH=backend pytest -q backend/tests.
5. Retrieval metrics: PYTHONPATH=backend python backend/evaluation/metrics.py.
6. Frontend smoke tests: cd frontend && npm test.

## Authentication API
- POST /api/auth/register: email, display_name, password (minimum 10 characters).
- POST /api/auth/login: email and password.
- GET /api/auth/me requires Authorization: Bearer token.
- GET /api/auth/users and PATCH /api/auth/users/{id}/role require admin.
- GET /api/recommendations/me?interests=biodiversity,nature requires authentication.
- Authenticated quiz submissions and progress are scoped to the signed-in learner; the legacy demo path remains available without a token.

## Evidence API
- GET /api/health, /api/courses, /api/sources.
- POST /api/assistant/ask with a question.
- GET /api/quizzes/{course_slug}; POST /api/quizzes/submit; GET /api/progress.
- POST /api/footprint/estimate.

## Retrieval evaluation and genuine metrics
The fixed query set is backend/evaluation/rag_queries.json. Run the evaluator to compute Recall@5, MRR and nDCG@5. These are reproducible offline ranking metrics on a small hand-labelled benchmark, not production user outcomes. The CI workflow runs this evaluation and prints the current metrics. Expand and independently review the benchmark and hold out test queries before making broad quality claims.

## Data provenance
backend/app/data/environmental_sources.json records publisher, report title, topics and authoritative URLs. The retrieval corpus contains concise editorial summaries linked to primary reports and data portals; it does not yet ingest full report tables or raw indicator downloads. Verify original report tables, definitions, dates, units, geography and scenario assumptions before citing numerical values.

## Deployment
The public repository is configured for two Vercel projects:
- Frontend root: frontend; set NEXT_PUBLIC_API_URL to the API origin.
- API root: backend; set DATABASE_URL, JWT_SECRET_KEY, API_ALLOWED_ORIGINS and optionally OPENAI_API_KEY / OPENAI_MODEL.
- Use managed PostgreSQL and allow the production frontend origin in API_ALLOWED_ORIGINS.
- GitHub Actions runs backend compilation, backend tests, retrieval evaluation, frontend smoke tests and a Next.js production build.

## Security and limitations
- Rotate the development secret and configure a high-entropy JWT_SECRET_KEY before deployment.
- Email verification, password reset, refresh-token rotation, rate limiting, audit logs, account deletion and abuse monitoring are not implemented.
- The frontend sign-in page stores a bearer token in localStorage; production should move to secure, HttpOnly, SameSite cookies and add CSRF protection.
- The existing main learning UI has not yet been fully wired to attach bearer tokens to all API calls.
- Database schema creation still uses create_all; introduce Alembic migrations and connection-pool tuning before production.
- The footprint estimator uses illustrative constants, not localized authoritative emission factors.
- LLM answers are optional; provider failures fall back to retrieved evidence.

## Performance reporting
Do not claim synthetic latency, user growth, learning gains or emissions savings as measured project outcomes. The retrieval evaluator provides actual reproducible ranking metrics. Benchmark latency/load on a named deployment and representative hardware before publishing performance numbers.

## License
MIT
