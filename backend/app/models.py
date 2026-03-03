from pydantic import BaseModel, field_validator
from typing import Literal

from app.config import MAX_PASTE_SIZE


class PasteCreate(BaseModel):
    content: str
    content_type: Literal["code", "mermaid", "text"]
    language: str | None = None
    ttl: Literal["1h", "1d", "1w", "1m", "never"] = "1d"

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content must not be empty")
        if len(v.encode("utf-8")) > MAX_PASTE_SIZE:
            raise ValueError(f"Content exceeds maximum size of {MAX_PASTE_SIZE} bytes")
        return v

    @field_validator("language")
    @classmethod
    def language_required_for_code(cls, v: str | None, info) -> str | None:
        if info.data.get("content_type") == "code" and not v:
            raise ValueError("Language is required when content_type is 'code'")
        if info.data.get("content_type") != "code" and v:
            return None
        return v


class PasteCreateResponse(BaseModel):
    id: str
    url: str
    created_at: str
    expires_at: str | None


class PasteResponse(BaseModel):
    id: str
    content: str
    content_type: str
    language: str | None
    created_at: str
    expires_at: str | None
