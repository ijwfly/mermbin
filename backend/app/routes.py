from fastapi import APIRouter, HTTPException

from app.models import PasteCreate, PasteCreateResponse, PasteResponse
from app.services import create_paste, get_paste

router = APIRouter(prefix="/api")


@router.post("/pastes", response_model=PasteCreateResponse, status_code=201)
async def create(data: PasteCreate):
    result = await create_paste(
        content=data.content,
        content_type=data.content_type,
        language=data.language,
        ttl=data.ttl,
    )
    return result


@router.get("/pastes/{paste_id}", response_model=PasteResponse)
async def read(paste_id: str):
    paste = await get_paste(paste_id)
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found")
    return paste
