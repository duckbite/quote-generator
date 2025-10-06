# AI Quote Generator API

## Endpoint

GET /quote

### Query Parameters

- style: concise|poetic (optional)
- length: short|medium|long (optional)
- topic: string (optional; defaults to "ducks")

### Response

```json
{
  "quote": "string",
  "attribution": "string|null",
  "source": "generated|curated",
  "cached": true
}
```

### Rate Limits

- Throttle at 1 RPS.

## Deploy

Prereqs: AWS credentials for `us-east-1`, Serverless Framework (`npx serverless --version`), and `OPENAI_API_KEY` exported by CI (fetched from Secrets Manager).

```bash
bash tools/deploy.sh
```

### CI/CD

- Push to `main` triggers `.github/workflows/deploy.yml`.
- The workflow fetches `OPENAI_API_KEY` from Secrets Manager and deploys to `us-east-1`.
- After deploy, find the API URL in the Serverless output or CloudFormation stack outputs. The output key is `HttpApiUrl`.
