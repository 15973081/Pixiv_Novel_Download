import io
import zipfile
from typing import List

from ..utils.http import http_client
from .novel_service import novel_service


class SeriesService:
    """
    系列服务：
    - 负责分页
    - 负责批量
    - 不负责单篇小说的业务细节
    """

    PAGE_SIZE = 30
    BASE_URL = "https://www.pixiv.net/ajax"

    # =====================
    # Series Info
    # =====================
    def get_series_info(self, series_id: str) -> dict:
        """
        获取系列元信息
        """
        url = f"{self.BASE_URL}/novel/series/{series_id}"
        try:
            resp = http_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("error"):
                return {"error": data.get("message")}

            body = data["body"]

            return {
                "id": body["id"],
                "title": body["title"],
                "userId": body["userId"],
                "userName": body["userName"],
                "caption": body.get("caption", ""),
                "tags": body.get("tags", []),
                "isConcluded": body.get("isConcluded"),
                "displaySeriesContentCount": body.get("displaySeriesContentCount", 0),
                "cover": body.get("cover", {}).get("urls", {}).get("original"),
                "createDate": body.get("createDate"),
                "updateDate": body.get("updateDate"),
            }
        except Exception as e:
            return {"error": str(e)}

    # =====================
    # Series Content (分页)
    # =====================
    def get_series_content(
            self,
            series_id: str,
            offset: int = 0,
            limit: int = 30
    ) -> dict:
        """
        返回单页 series 内容（不做循环）
        """
        url = (
            f"{self.BASE_URL}/novel/series_content/"
            f"{series_id}"
            f"?limit={limit}&last_order={offset}&order_by=asc"
        )

        try:
            resp = http_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("error"):
                return {"error": data.get("message")}

            page = data["body"]["page"]

            return {
                "seriesContents": page.get("seriesContents", []),
                "isLastPage": page.get("isLastPage", False),
            }
        except Exception as e:
            return {"error": str(e)}

    # =====================
    # Series Content
    # =====================
    def get_series_novel_ids(self, series_id: str) -> List[str]:
        """
        获取系列下所有小说 ID（自动分页）
        """
        info = self.get_series_info(series_id)
        if "error" in info:
            return info

        total = info.get("displaySeriesContentCount", 0)
        if total <= 0:
            return []

        ids: List[str] = []
        offset = 0

        while len(ids) < total:
            page = self.get_series_content(
                series_id=series_id,
                offset=offset,
                limit=self.PAGE_SIZE
            )
            if "error" in page:
                break

            contents = page.get("seriesContents", [])
            for item in contents:
                ids.append(str(item["id"]))

            offset += self.PAGE_SIZE

        return ids

    # =====================
    # Download
    # =====================
    def download_series(self, series_id: str, mode: str = "split") -> dict:
        """
        批量下载系列

        mode:
          - split: 每章一个 txt，zip
          - merge: 合并成一个 txt
        """
        novel_ids = self.get_series_novel_ids(series_id)
        if isinstance(novel_ids, dict) and "error" in novel_ids:
            return novel_ids

        if not novel_ids:
            return {"error": "series is empty"}

        info = self.get_series_info(series_id)
        title = info.get("title", series_id)

        if mode == "merge":
            return self._download_merge(series_id, title, novel_ids)

        return self._download_split(series_id, title, novel_ids)

    # =====================
    # Split (ZIP)
    # =====================
    def _download_split(self, series_id: str, title: str, novel_ids: List[str]) -> dict:
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for index, novel_id in enumerate(novel_ids, start=1):
                novel = novel_service.download(novel_id, format="txt")
                if "error" in novel:
                    continue

                filename = f"{index:03d}_{novel['filename']}"
                zf.writestr(filename, novel["content"])

        zip_buffer.seek(0)

        return {
            "filename": f"{series_id}_{title}.zip",
            "content": zip_buffer,
            "type": "application/zip"
        }

    # =====================
    # Merge (TXT)
    # =====================
    def _download_merge(self, series_id: str, title: str, novel_ids: List[str]) -> dict:
        buffer = io.StringIO()

        for index, novel_id in enumerate(novel_ids, start=1):
            result = novel_service.download(novel_id, format="txt")
            if "error" in result:
                continue

            buffer.write(f"\n\n--- #{index} ---\n\n")
            buffer.write(result["content"])

        content = buffer.getvalue().encode("utf-8-sig")

        return {
            "filename": f"{series_id}_{title}.txt",
            "content": io.BytesIO(content),
            "type": "text/plain"
        }


# 全局单例
series_service = SeriesService()
