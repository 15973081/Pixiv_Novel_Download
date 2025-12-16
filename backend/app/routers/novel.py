from fastapi import APIRouter, Query, HTTPException, Response
from ..services.novel_service import novel_service

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
    try:
        result = novel_service.download(novel_id, format)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Check if content needs encoding handling
        content = result["content"]
        if isinstance(content, str):
            # Encode string content to bytes for safe transmission
            # UTF-8 with BOM helps Excel/Windows open it correctly
            content = content.encode("utf-8-sig")
            
        # Sanitize filename to prevent header injection
        filename = result["filename"].replace('"', '').replace('\n', '').replace('\r', '')
        
        # Return as file download
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return Response(
            content=content,
            media_type=result["type"],
            headers=headers
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
