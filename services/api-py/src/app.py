import os
import json
import time
import hashlib
from typing import Optional

import boto3
from fastapi import FastAPI, Query, HTTPException
from mangum import Mangum
from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_SEED = int(os.getenv("OPENAI_SEED", "0"))
DDB_TABLE_NAME = os.getenv("DDB_TABLE_NAME", "quote-generator-prod")


app = FastAPI(title="AI Quote Generator API")
ddb = boto3.resource("dynamodb")
table = ddb.Table(DDB_TABLE_NAME)
openai_client = None


def build_cache_key(topic: str, style: Optional[str], length: Optional[str], model: str) -> str:
    normalized = json.dumps({
        "topic": (topic or "").strip().lower(),
        "style": (style or "").strip().lower(),
        "length": (length or "").strip().lower(),
        "model": model,
        "version": 1,
    }, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_cache(pk: str, sk: str):
    resp = table.get_item(Key={"pk": pk, "sk": sk})
    return resp.get("Item")


def put_cache(pk: str, sk: str, quote: str, attribution: Optional[str], ttl_seconds: int):
    now = int(time.time())
    item = {
        "pk": pk,
        "sk": sk,
        "quote": quote,
        "attribution": attribution or None,
        "source": "generated",
        "ttl": now + ttl_seconds,
        "createdAt": now,
    }
    table.put_item(Item=item)


def generate_quote_with_openai(topic: str, style: Optional[str], length: Optional[str]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

    global openai_client
    if openai_client is None:
        openai_client = OpenAI(api_key=api_key)

    system_prompt = (
        "You generate concise, original inspirational quotes. The quote must reference ducks."
    )
    user_prompt = (
        f"Style: {style or 'concise'}; Length: {length or 'short'}; Topic: {topic or 'ducks'}. "
        "Return only the quote text without attribution."
    )

    completion = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        seed=OPENAI_SEED if OPENAI_SEED > 0 else None,
    )

    quote_text = completion.choices[0].message.content.strip()
    return {"quote": quote_text, "attribution": None, "source": "generated"}


@app.get("/quote")
def get_quote(
    style: Optional[str] = Query(default=None, pattern="^(concise|poetic)$"),
    length: Optional[str] = Query(default=None, pattern="^(short|medium|long)$"),
    topic: Optional[str] = Query(default="ducks"),
):
    model = OPENAI_MODEL
    cache_key = build_cache_key(topic or "ducks", style, length, model)
    pk = "QUOTE"
    sk = cache_key

    cached = get_cache(pk, sk)
    if cached:
        return {
            "quote": cached.get("quote"),
            "attribution": cached.get("attribution"),
            "source": "cached",
            "cached": True,
        }

    generated = generate_quote_with_openai(topic or "ducks", style, length)
    put_cache(pk, sk, generated["quote"], generated.get("attribution"), ttl_seconds=24 * 3600)
    return {
        "quote": generated["quote"],
        "attribution": generated.get("attribution"),
        "source": generated.get("source", "generated"),
        "cached": False,
    }


handler = Mangum(app)


