from fastapi import APIRouter, Query, HTTPException
from ..services.novel_service import novel_service
from fastapi.responses import StreamingResponse
from urllib.parse import quote
import io

router = APIRouter()

@router.get("/search")
def search_novels(
    keyword: str = Query(..., description="Search keyword"),
    page: int = Query(1, description="Page number")
):
    result = novel_service.search(keyword, page)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{novel_id}")
def get_novel_info(novel_id: str):
    result = novel_service.get_info(novel_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/{novel_id}/content")
def get_novel_content(novel_id: str):
    result = novel_service.get_content(novel_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/{novel_id}/download")
def download_novel(novel_id: str, format: str = "txt"):
    result = novel_service.download(novel_id, format)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    content = result["content"]
    if isinstance(content, str):
        content = content.encode("utf-8-sig")

    filename = result["filename"]
    ascii_filename = "novel.txt"          # 兜底名（必须 ASCII）
    quoted_filename = quote(filename)     # UTF-8 URL 编码

    headers = {
        "Content-Disposition": (
            f"attachment; "
            f"filename=\"{ascii_filename}\"; "
            f"filename*=UTF-8''{quoted_filename}"
        )
    }

    return StreamingResponse(
        io.BytesIO(content),
        media_type=result["type"],
        headers=headers
    )

