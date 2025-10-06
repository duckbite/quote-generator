# Build Plan

## Scope

- Serverless FastAPI Lambda (`services/api-py`) with `GET /quote`.
- DynamoDB cache table with TTL.
- OpenAI integration (model and tuning as constants; key via env var).

## Steps

1. Scaffold service and Serverless config (done).
2. Implement endpoint with cache and placeholder generator (done; replace with OpenAI SDK later).
3. Configure DynamoDB table (done in Serverless resources).
4. Wire OpenAI key injection at deploy (CI/export of `OPENAI_API_KEY`).
5. Add tests (unit for cache key, integration with mocked OpenAI).
6. Deploy to prod stage in `us-east-1`.

## Notes

- Rate limit via API Gateway usage plan or WAF; basic throttling set to 1 RPS.
- CORS: `*`.
