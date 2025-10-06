# AI Quote Generator API

A simple API that returns a random inspirational quote generated or curated by AI.

## Features:

- User sends an HTTP request → API Gateway → Lambda → returns quote.
- Use OpenAI for generating quotes dynamically.
- Cache results in DynamoDB or S3 to avoid repeated API calls.
- Quote always has something to do with ducks

## Architecture & Deployment

- Runtime: API Gateway → AWS Lambda using Python with FastAPI.
- IaC: Serverless Framework.
- AWS Region: us-east-1.

## API Surface

- Endpoint: GET /quote
- Query parameters:
  - style: concise|poetic (optional)
  - length: short|medium|long (optional)
  - topic: string (optional; defaults to "ducks")
- Rate limit: throttle at 1 RPS.

## OpenAI Integration

- Model: gpt-4o-mini.
- Tuning: temperature and seed defined as module-level constants.
- Key management: OPENAI_API_KEY retrieved from AWS Secrets Manager at deploy time and injected into function environment.
  - Secret ARN: arn:aws:secretsmanager:us-east-1:052306545299:secret:prod/quote-generator/openai-key-MVrI4K

## Caching & Persistence

- Storage: DynamoDB (on-demand capacity).
- Table name: quote-generator-prod.
- Design: single-table best practices with partition/sort keys; cache key based on normalized (topic, style, length, model, version).
- TTL: 24 hours (1 day).

## Non-Functional Requirements

- Latency: P95 < 500ms when cached; < 3s when generated.
- Throughput: very low (testing only).
- Cost guardrails: daily cap of 1 USD.
- Logging/observability: none required initially.

## Security

- Auth: public endpoint.
- CORS: \* (all origins).
- PII: none.

## Testing & Quality

- Tests: unit (prompt builder, cache), integration (OpenAI mocked from latest Swagger), contract tests for API.
- Environments: prod only (for now).
