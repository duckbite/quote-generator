# Build Plan

## Local-first development

- Python runtime: 3.12
- Package manager: uv
- Local server: Uvicorn running FastAPI app with hot-reload
- Env: `.env` file containing OPENAI_API_KEY for local use
- Run targets:
  - `uv venv && uv sync`
  - `uv run uvicorn app.main:app --reload --port 8000`

## API contract

- Endpoint: `GET /quote`
- Query parameters:
  - `style`: `concise|poetic` (optional)
  - `length`: `short|medium|long` (optional)
  - `topic`: string (optional; default: `ducks`)
- Response body (200):
  - `quote`: string
  - `model`: string (e.g., `gpt-4o-mini`)
  - `metadata` (optional): object with generation details

## OpenAI integration

- Model: `gpt-4o-mini`
- Config constants: `TEMPERATURE`, `SEED`, `MAX_TOKENS`, `REQUEST_TIMEOUT_S`
- Error handling: timeouts, limited retries with exponential backoff; return 503 if generation fails

## Rate limiting

- Prod: API Gateway throttle 1 RPS (confirm burst: 1)
- Local: simple in-process limiter (IP-based) for parity

## Security & CORS

- Public endpoint
- CORS: `*`

## Testing strategy

- Unit tests: prompt builder, parameter validation
- Integration tests: OpenAI client mocked from latest Swagger; network calls blocked
- Contract tests: OpenAPI schema for `GET /quote`

## Deployment (AWS)

- Framework: Serverless Framework
- Runtime: Python 3.12, FastAPI on Lambda via API Gateway
- Env: `prod` stage
- Secrets: `OPENAI_API_KEY` via AWS Secrets Manager (provided ARN)
- IAM: permission to read secret only
- Memory/timeout: start 512 MB, 10s timeout (tune for P95 < 3s)
- Region: `us-east-1`

## CI/CD

- GitHub Actions: build, test, deploy on main
- OIDC to assume deploy role defined in `infra/cfn/github-actions-deploy-role.yml`

## Observability

- Structured logs (JSON) with request IDs

## Next steps checklist

- [ ] Scaffold FastAPI app structure (`app/main.py`, `app/routers/quote.py`)
- [ ] Implement OpenAI client and prompt builder
- [ ] Add rate limiting (local) and API Gateway throttling (prod)
- [ ] Define OpenAPI schema and contract tests
- [ ] Add unit/integration tests (pytest)
- [ ] Serverless config with Lambda + API Gateway + Secrets Manager
- [ ] GitHub Actions workflow for CI/CD
