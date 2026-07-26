from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sqlite3
import hashlib
import json
import uuid
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Mailroom Action Gate")
conn = sqlite3.connect("mailroom.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS proposals(
    dossier_id TEXT PRIMARY KEY,
    evaluation_id TEXT,
    digest TEXT,
    call_id TEXT,
    action TEXT,
    target TEXT,
    payload TEXT,
    evidence TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS receipts(
    call_id TEXT PRIMARY KEY,
    receipt TEXT
)
""")

conn.commit()
def sha256_digest(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()
def generate_call_id(dossier):
    return hashlib.sha256(
        json.dumps(dossier, sort_keys=True).encode()
    ).hexdigest()[:24]
ALLOWED_ACTIONS = [
    "create_draft",
    "update_internal_record",
    "send_approved_notice",
    "request_confirmation",
    "quarantine_item",
    "no_action"
]
class ReceiptVerifier(BaseModel):
    algorithm: str
    publicKeyJwk: Dict[str, Any]


class Line(BaseModel):
    lineId: str
    text: str


class Source(BaseModel):
    sourceId: str
    kind: str
    provenance: str
    title: str
    lines: List[Line]


class Dossier(BaseModel):
    dossierId: str
    partition: str
    receivedAt: str
    mailbox: str
    objective: str
    sources: List[Source]


class ProposalRequest(BaseModel):
    profile: str
    operation: str
    evaluationId: str
    receiptVerifier: ReceiptVerifier
    corpus: Dict[str, Any]
    allowedActions: List[str]
    dossiers: List[Dossier]
def decide_action(dossier):
    """
    AI decision function.
    We'll implement this in the next step using OpenAI.
    """
    return {
        "action": "no_action",
        "target": None,
        "payload": {},
        "evidence": []
    }
