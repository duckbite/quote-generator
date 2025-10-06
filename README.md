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
