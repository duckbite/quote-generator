# AI Quote Generator API

A simple API that returns a random inspirational quote generated or curated by AI.

## Features:

- User sends an HTTP request → API Gateway → Lambda → returns quote.
- Use OpenAI for generating quotes dynamically.
- Cache results in DynamoDB or S3 to avoid repeated API calls.
- Quote always has something to do with ducks
