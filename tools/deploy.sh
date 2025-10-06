#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_DIR="$ROOT_DIR/services/api-py"

export AWS_REGION="us-east-1"

cd "$SERVICE_DIR"

# Fetch OPENAI_API_KEY from Secrets Manager if not set
: "${OPENAI_SECRET_ARN:=arn:aws:secretsmanager:us-east-1:052306545299:secret:prod/quote-generator/openai-key-MVrI4K}"
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  if command -v aws >/dev/null 2>&1; then
    echo "Fetching OPENAI_API_KEY from Secrets Manager..."
    SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id "$OPENAI_SECRET_ARN" --region "$AWS_REGION" --query SecretString --output text || echo "")
    if [[ -n "$SECRET_JSON" ]]; then
      # If secret is a raw key, use it; if JSON, try OPENAI_API_KEY field
      if [[ "$SECRET_JSON" == \{*\} ]]; then
        OPENAI_API_KEY=$(python3 - <<'PY'
import json, os
s=os.environ.get('SECRET_JSON','')
try:
  d=json.loads(s)
  print(d.get('OPENAI_API_KEY') or d.get('openai_api_key') or d.get('key') or '')
except Exception:
  print('')
PY
)
      else
        OPENAI_API_KEY="$SECRET_JSON"
      fi
      export OPENAI_API_KEY
    fi
  fi
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "WARNING: OPENAI_API_KEY is not set. Deployment will proceed but runtime will fail without it." >&2
fi

pip install -r requirements.txt --target .python_packages

npx --yes serverless deploy --stage prod --region "$AWS_REGION"

