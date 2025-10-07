# Local Environment Setup

- Create a `.env` in the repo root with:

```
AWS_REGION=us-east-1
DDB_TABLE_NAME=quote-generator-prod
OPENAI_API_KEY=sk-xxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_SEED=0
```

- Run locally:

```
cd services/api-py
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```
