from pydantic import BaseModel, HttpUrl
from typing import Optional, List
class Source(BaseModel):
    id: str
    type: str
    url: HttpUrl
    title: str
    publisher: str
    date: Optional[str] = None
    license: Optional[str] = None
    checksum_sha256: Optional[str] = None
    retrieved_at: Optional[str] = None
class Claim(BaseModel):
    claim_id: str
    text: str
    source_id: str
    source_quote: str
    page_or_section: str
    evidence_type: str
    risk_level: Optional[str] = None
class Verification(BaseModel):
    claim_id: str
    status: str
    verifier: str
    method: str
    notes: Optional[str] = None
    links: Optional[List[str]] = None
    timestamp: str