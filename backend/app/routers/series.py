from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import quote

from ..services.series_service import series_service

router = APIRouter(tags=["Series"])


@router.get("/{series_id}")
def get_series_info(series_id: str):
    result = series_service.get_series_info(series_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/{series_id}/content")
def get_series_content(series_id: str):
    ids = series_service.get_series_novel_ids(series_id)
    if isinstance(ids, dict) and "error" in ids:
        raise HTTPException(status_code=404, detail=ids["error"])

    return {
        "series_id": series_id,
        "novel_ids": ids
    }


@router.get("/{series_id}/download")
def download_series(
    series_id: str,
    mode: str = Query("split", enum=["split", "merge"])
):
    result = series_service.download_series(series_id, mode)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    headers = {
        "Content-Disposition": (
            f'attachment; filename="series"; '
            f"filename*=UTF-8''{quote(result['filename'])}"
        )
    }

    return StreamingResponse(
        result["content"],
        media_type=result["type"],
        headers=headers
    )
