import pytest
from pydantic import ValidationError

from app.config import MAX_PASTE_SIZE
from app.models import PasteCreate


class TestPasteCreate:
    def test_valid_text_paste(self):
        p = PasteCreate(content="hello", content_type="text")
        assert p.content == "hello"
        assert p.content_type == "text"
        assert p.language is None
        assert p.ttl == "1d"

    def test_valid_code_paste(self):
        p = PasteCreate(content="print(1)", content_type="code", language="python")
        assert p.content_type == "code"
        assert p.language == "python"

    def test_valid_mermaid_paste(self):
        p = PasteCreate(content="graph TD; A-->B;", content_type="mermaid")
        assert p.content_type == "mermaid"
        assert p.language is None

    def test_empty_content_rejected(self):
        with pytest.raises(ValidationError, match="Content must not be empty"):
            PasteCreate(content="", content_type="text")

    def test_whitespace_content_rejected(self):
        with pytest.raises(ValidationError, match="Content must not be empty"):
            PasteCreate(content="   ", content_type="text")

    def test_oversized_content_rejected(self):
        big = "x" * (MAX_PASTE_SIZE + 1)
        with pytest.raises(ValidationError, match="exceeds maximum size"):
            PasteCreate(content=big, content_type="text")

    def test_content_at_boundary(self):
        content = "x" * MAX_PASTE_SIZE  # ASCII: 1 byte per char
        p = PasteCreate(content=content, content_type="text")
        assert len(p.content) == MAX_PASTE_SIZE

    def test_language_required_for_code(self):
        with pytest.raises(ValidationError, match="Language is required"):
            PasteCreate(content="x = 1", content_type="code", language=None)

    def test_language_stripped_for_non_code(self):
        p = PasteCreate(content="hello", content_type="text", language="python")
        assert p.language is None

    def test_invalid_content_type_rejected(self):
        with pytest.raises(ValidationError):
            PasteCreate(content="hello", content_type="html")

    def test_invalid_ttl_rejected(self):
        with pytest.raises(ValidationError):
            PasteCreate(content="hello", content_type="text", ttl="2h")

    def test_default_ttl_is_1d(self):
        p = PasteCreate(content="hello", content_type="text")
        assert p.ttl == "1d"
